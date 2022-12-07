from django.db import transaction,IntegrityError,DatabaseError
from  django.core.exceptions import ObjectDoesNotExist
from Payment.models import TransactionModel
from Artisans.models import ArtisanModel
from datetime import datetime
import uuid
from paystackapi.verification import Verification
from paystackapi.trecipient import TransferRecipient
from paystackapi.transfer import Transfer
from paystackapi.transaction import Transaction
from paystackapi.paystack import Paystack
from django.conf import settings

paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)
 

class WithdrawAction(object):
    """
        Paystack Fund widthdrawal for merchant action
    """

    @transaction.atomic
    def withdraw(name,account_no,amount,bank_code):

        response = TransferRecipient.create(
            type="nuban",
            name=name,
            description=name+ " withdrawal",
            account_number=account_no,
            bank_code=bank_code,
        )
        # if paystack call is successful
        if response['status'] == True:
            transfer_response = Transfer.initiate(
                source="balance",
                reason=name+ " withdrawal",
                amount=amount * 100,
                recipient=response['data']['recipient_code'],
            )
            if transfer_response['status'] == True and transfer_response['data']['status']=='otp':
                return  {
                        'status':True,
                        'message':'Withdrawal is being processed'
                    }
            else:
                return {
                    "status":False,
                    "message":"Withdrawal not successfull"
                    }
        else:
            return {
                "status":False,
                "message":"Could not initiate Withdrawal"
            }

          

       
 

