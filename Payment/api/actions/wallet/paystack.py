from Payment.models.payment_log import PaymentLogModel
from django.db import transaction,IntegrityError,DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from Payment.models import TransactionModel
from Artisans.models import ArtisanModel
import uuid
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from django.db.models import F
from django.conf import settings
# from rave_python import Rave,RaveExceptions

paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)

class FundWallet(object):

    @transaction.atomic
    def paystackDirect(amount,reference,user,transaction_ref):
        """
            Paystack Direct credit of merchant after verifying a transaction reference
        """
    
        verify_response = Transaction.verify(reference=reference)    
        print(verify_response)
        
        # if paystack call is successful
        if verify_response['status'] == True:

            initial_save_point = transaction.savepoint()

            try:
                with transaction.atomic():
                    
                        #create credit transaction record
                        credit_transaction_id = TransactionModel(transaction_reference=transaction_ref,
                        transaction_amount=amount,transaction_status=2,transaction_user =user,
                        transaction_type='1',transaction_description="Wallet Topup",payment_channel="Paystack")
                        credit_transaction_id.save()

                        #credit user wallet
                        user.wallet_balance = float(user.wallet_balance) + float(amount)
                        user.save()

                        return {'status':True,'message':'Wallet Funded'}
                

            except (IntegrityError,DatabaseError,ObjectDoesNotExist,ValueError) as a:    
                #TODO log error here 

                transaction.savepoint_rollback(initial_save_point)

                #generate failed transaction  record
                transaction_id = TransactionModel(transaction_reference=transaction_ref,
                        transaction_amount=amount,transaction_status=3,transaction_user =user,
                        transaction_type='1',transaction_description="Wallet Topup",payment_channel="Paystack")
                transaction_id.save()

                return {'status':False,'message':'Transation failed....please contact admin'}
        else:
            #TODO log error here
            return {'status':False,'message':verify_response['message']}



    # @transaction.atomic
    # def paystackDirectMerchant(amount,reference,merchant,transaction_ref):
    #     """
    #         Merhant Paystack Direct credit of merchant after verifying a transaction reference
    #     """
    
    #     verify_response = Transaction.verify(reference=reference)    
    #     print(verify_response)
        
    #     # if paystack call is successful
    #     if verify_response['status'] == True:

    #         initial_save_point = transaction.savepoint()

    #         try:
    #             with transaction.atomic():
                    
    #                     #create credit transaction record
    #                     credit_transaction_id = TransactionModel(transaction_reference=transaction_ref,
    #                     transaction_amount=amount,transaction_status=2,transaction_merchant =merchant,
    #                     transaction_type='1',transaction_description="Wallet Topup",payment_channel="Paystack",is_merchant=True)
    #                     credit_transaction_id.save()

    #                     #credit user wallet
    #                     merchant.wallet_balance = float(merchant.wallet_balance) + float(amount)
    #                     merchant.save()

    #                     return {'status':True,'message':'Wallet Funded'}
                

    #         except (IntegrityError,DatabaseError,ObjectDoesNotExist,ValueError) as a:    
    #             #TODO log error here

    #             transaction.savepoint_rollback(initial_save_point)

    #             #generate failed transaction  record
    #             transaction_id = TransactionModel(transaction_reference=transaction_ref,
    #                     transaction_amount=amount,transaction_status=3,transaction_merchant =merchant,
    #                     transaction_type='1',transaction_description="Wallet Topup",payment_channel="Paystack",is_merchant=True)
    #             transaction_id.save()

    #             return {'status':False,'message':'Transation failed....please contact admin'}
    #     else:
    #         #TODO log error here
    #         return {'status':False,'message':verify_response['message']}

