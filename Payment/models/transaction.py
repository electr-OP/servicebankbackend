from django.db import models
# from Payment.models import CardModel
from Auth.models import User
from Artisans.models import ArtisanModel
from django.db.models.signals import post_save


class TransactionModel(models.Model):
    """
        Transaction model
    """

    TRANSACTION_TYPE = [
        (1, 'Wallet Funding'),
        (2, 'Debit'),
        (3, 'Payment Recieved'),
    ]

    TRANSACTION_STATUS = [
        (1, 'Failed'),
        (2, 'Success'),
        (3, 'Processing'),
    ]

    PAYMENT_CHANNELS = [
      ('Card','Card'),
      ('Transfer','Transfer'),
      ('Wallet','Wallet'),
      ('Ussd','Ussd'),
      ('Paystack','Paystack'),
      ('Flutterwave','Flutterwave'),
      ('Cash','Cash'),

    ]

    transaction_user = models.ForeignKey(User,  on_delete=models.SET_NULL,null=True)
    transaction_artisan = models.ForeignKey(ArtisanModel,  on_delete=models.SET_NULL,null=True)
    transaction_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    # transaction_card = models.ForeignKey(CardModel,on_delete=models.SET_NULL,null=True)
    transaction_type =  models.CharField(choices=TRANSACTION_TYPE,max_length=10)
    payment_channel = models.CharField(choices=PAYMENT_CHANNELS,max_length=255)
    transaction_reference = models.CharField(max_length=100)
    transaction_description = models.CharField(max_length=255)
    transaction_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_status = models.CharField(choices=TRANSACTION_STATUS,null=True,max_length=255)
    is_artisan = models.BooleanField(default=False)
    

    def __str__(self):
        return self.transaction_reference
        
    class Meta:
        db_table = 'transactions'
        managed = True
        verbose_name = 'Transactions'
        verbose_name_plural = 'Transactions'
