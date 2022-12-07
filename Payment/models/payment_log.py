from django.db import models

class PaymentLogModel(models.Model):
    """
        Payment log model

        Currently used for paystack initialized payments
    """

    transaction_ref = models.CharField(max_length=255,null=True)
    payment_date = models.DateTimeField(auto_now=True)
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_request_endpoint =models.CharField(max_length=50)
    payment_request_response =models.TextField(null=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        self.transaction_ref

    class Meta:
        db_table = 'payment_log'
        managed = True
        verbose_name = 'Payment Requests Log'
        verbose_name_plural = 'Payment Requests Log'