from django.core.exceptions import ValidationError
from Payment.models.transaction import TransactionModel
from Payment.api.serializers import TransactionSerializer
from rest_framework import status
from rest_framework.decorators import api_view,action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Artisans.api.serializers import *
from django.conf import settings
from rest_framework_tracking.mixins import LoggingMixin




class PaymentHistoryUserView(LoggingMixin,APIView):
    """
        User payment history

    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
         transactions = TransactionModel.objects.filter(transaction_user=request.user.id)
         serializer = TransactionSerializer(transactions,many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
