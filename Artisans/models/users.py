from ast import Mod
from lib2to3.pgen2 import driver
from django.db import models
from Auth.models import User
from Artisans.models import ArtisanModel
import uuid


class ArtisanUserModel(models.Model):
    """
        Artisan Permission model
        Shows users and their permission on an Artisan account
    """

    PERMISSIONS = (
        ('1', 'Business Owner'),
        ('2', 'Admin'),
        ('3', 'Staff'),
        ('4', 'Customer Support'),
    )

    artisan = models.ForeignKey(ArtisanModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    email_address = models.EmailField(null=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    permission = models.CharField(choices=PERMISSIONS,max_length=50)
    invitation_accepted = models.BooleanField(default=True, blank=True)
    invite_token =models.CharField(max_length=300,unique=False, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    
 
    def __str__(self):
        return self.artisan.name

    class Meta:
        db_table = 'artisans_users'
        managed = True
        verbose_name = 'Artisan User'
        verbose_name_plural = 'Artisan Users'


# class UserDetails(models.Model):
#     """
#     Adding extra Merchant User details
#     """

#     merchant_user = models.ForeignKey(MerchantUserModel, on_delete=models.CASCADE)
#     riders_permit = models.FileField()
#     drivers_license = models.FileField()
#     next_of_kin = models.CharField(max_length=255)
#     guarantor = models.CharField(max_length=255)


#     class Meta:
#         db_table = 'merchantuser_details'
#         managed = True
#         verbose_name = 'Merchant User Detail'
#         verbose_name_plural = 'Merchant User Details'