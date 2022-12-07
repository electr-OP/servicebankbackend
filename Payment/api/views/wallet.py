from Payment.api.serializers.paystack import PaystackPaymentVerifySerializer
from Payment.api.serializers.withdrawal import *
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import api_view,action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Payment.api.actions.wallet.paystack import FundWallet
from Payment.api.actions.bank_account.verify_account import VerifyBankAccountAction
from Payment.api.actions.bank_account.withdrawal import WithdrawAction
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.http import HttpResponse
from rest_framework_tracking.mixins import LoggingMixin


class PaystackPaymentVerifyView(LoggingMixin,APIView):
    """
        User fund wallet with paystack verification view
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        serializer = PaystackPaymentVerifySerializer(data=request.data)
        if serializer.is_valid():

            amount=request.data.get('amount')
            token = request.data.get('token')
            transaction_reference = "CR" + uuid.uuid4().hex[:8]
            
            fund_wallet = FundWallet.paystackDirect(amount,token,request.user,transaction_reference)
            if fund_wallet['status']:
                return Response(fund_wallet)
            else:
                return Response({"detail":fund_wallet['message']},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserWithdrawalView(LoggingMixin,APIView):

    """
       User fund widthdrawal view
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WidthdrawalSerializer(data=request.data)
        if serializer.is_valid():
            account_no = request.data['account_no']
            bank_code = request.data['bank_code']
            amount = float(request.data['amount'])
            user = request.user
            response = VerifyBankAccountAction.verify(account_no,bank_code)
            if response['status'] == True:
                # return Response({"data":response['data']}, status=status.HTTP_200_OK)
                user_balance = user.wallet_balance

                if user_balance < amount:
                    return Response({"detail":"Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)
                #perform withdrawal
                response = WithdrawAction.withdraw((user.first_name+' '+user.last_name),account_no,amount,bank_code)
                if response['status'] == True:
                    user.wallet_balance = float(user.wallet_balance) - float(amount)
                    user.save()
                    return Response({"data":response['message']}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail":response['message']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail":response['message']}, status=status.HTTP_400_BAD_REQUEST)
               
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)