from django.db import models
from Auth.models import User

# Create your models here.


class ReferralModel(models.Model):
    """
      Referral Model
    """
    referred_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referred_me")
    referred_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_referrals")
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.referred_by.first_name

    class Meta:
        db_table = 'referrals'
        managed = True
        verbose_name = 'Referral'
        verbose_name_plural = 'Referrals'
