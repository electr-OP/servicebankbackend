from django.db import models
from django.contrib.auth.models import (
     AbstractBaseUser
)
import uuid
from Auth.api.utils import generate_referral_id
from Auth.mixins.user import CustomUserManager



class User(AbstractBaseUser):


    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    COUNTRIES = [
        ('Nigeria','Nigeria')
    ]

    CURRENCY = [
        ('NGN','NGN'),
        ('USD','USD')
    ]

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    phone = models.CharField(help_text='Contact phone number',unique=True, max_length=20, null=True,blank=True)
    password = models.CharField(max_length=255, null=False)
    uid = models.UUIDField(default=uuid.uuid4, editable=False,null=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name =  models.CharField(max_length=255,null=False)
    middle_name = models.CharField(max_length=255, null=True,blank=True)
    address = models.CharField(max_length=255, null=True,blank=True)
    latitude = models.CharField(max_length=255, null=True,blank=True)
    longitude = models.CharField(max_length=255, null=True,blank=True)
    city = models.CharField(max_length=255, null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to='user/profile/',blank=True,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True,blank=True)
    wallet_balance = models.DecimalField(max_digits=20,decimal_places=2,default=0, null=True,blank=True)
    country = models.CharField(choices=COUNTRIES,max_length=20, null=True,blank=True)
    country_code = models.CharField(max_length=20,null=True,blank=True)
    public_key = models.CharField(max_length=255,null=True,blank=True)
    secret_key = models.CharField(max_length=255,null=True,blank=True)
    currency = models.CharField(choices=CURRENCY,max_length=20,null=True,blank=True)
    has_updated_profile = models.BooleanField(default=False)
    has_updated_bank_info = models.BooleanField(default=False)
    has_added_card = models.BooleanField(default=False)
    registration_token = models.CharField(max_length=20,null=True,blank=True)
    referral_code= models.CharField(max_length=20,default=generate_referral_id,unique=True,null=True,blank=True)
    token = models.CharField(max_length=20,null=True,blank=True)
    email_activated = models.BooleanField(default=False)
    is_artisan = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def __str__(self):
        return str(self.first_name) +" " + str(self.last_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_all_permissions(user=None):
        if user.is_admin:
            
            return set()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
