from django.db import transaction,IntegrityError,DatabaseError
from  django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import uuid
from paystackapi.verification import Verification
from paystackapi.trecipient import TransferRecipient
from paystackapi.misc import Misc
from paystackapi.paystack import Paystack
from paystackapi.verification import Verification
from django.conf import settings


paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)
 

class VerifyBankAccountAction(object):

    @transaction.atomic
    def verify(account_number,bank_code):
    
        verify_response = Verification.verify_account(account_number=account_number,bank_code=bank_code)

        # if paystack call is successful
        if verify_response['status'] == True:
            return  {'status':True,
                     'data':verify_response['data']
               }
        else:
            return {
                "status":False,
                "message":"Account details not valid"
            }

    def getAllBanks():
        response = Misc.list_banks()
        return response['data']
