from email.policy import default
from Artisans.api.utils import unique_otp_generator
from django.db import models
from Auth.models import User
import uuid
from Job.models.professions import ProfessionModel
from django.dispatch import receiver
from django.db.models.signals import post_save



class ArtisanModel(models.Model):
    """
        Artisan model
    """
    CURRENCY = [
        ('NGN','NGN'),
        ('USD','USD')
    ]

    COUNTRIES = [
        ('NG','Nigeria')
    ]

    TYPES = [
        ('1','PARTNEER'),
        ('2','INTEGRATIONS')
    ]

    STATUS = [
        ("AVAILABLE","Available"),
        ("BUSY","Busy"),
        ("CLOSED","Closed")
    ]

    RANK = [
        ("5", "Gold"),
        ("4", "Silver"),
        ("3", "Bronze"),
        ("2", "Standard"),
        ("1", "Basic")

    ]

    artisan_id = models.CharField(max_length=100, blank=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255,unique=True)
    code = models.CharField(max_length=255,unique=True,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=100,default="")
    state_code = models.CharField(max_length=100, default="",blank=True,null=True)
    country = models.CharField(choices=COUNTRIES,max_length=100,default="",blank=True,null=True)   
    description = models.CharField(max_length=255,default="",blank=True,null=True)
    long_description = models.TextField(default="",blank=True,null=True)
    tagline = models.CharField(max_length=255,default="",blank=True,null=True)
    website = models.CharField(max_length=255,default="",blank=True,null=True)
    logo = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=255,default="",blank=True,null=True)
    email = models.CharField(max_length=255,default="")
    artisan_type = models.CharField(choices=TYPES,max_length=255,default="1")
    latitude = models.CharField(max_length=25,default="",blank=True,null=True)
    longitude = models.CharField(max_length=25,default="",blank=True,null=True) 
    working_time_from = models.TimeField(null=True)
    working_time_to = models.TimeField(null=True)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2,default=0.0)
    pending_wallet_balance = models.DecimalField(max_digits=12, decimal_places=2,default=0.0)
    profession = models.ManyToManyField(ProfessionModel)
    public_key = models.CharField(max_length=255,null=True,unique=True,blank=True)
    secret_key = models.CharField(max_length=255,null=True,unique=True,blank=True)
    currency = models.CharField(choices=CURRENCY,default='NGN',max_length=100)
    email_activated = models.BooleanField(default=False)
    cancelled_order = models.IntegerField(null=True,blank=True)
    is_visible = models.BooleanField(default=True)
    rc_number = models.CharField(max_length=100,null=True,blank=True)
    email_activation_token = models.CharField(max_length=255,null=True,unique=True,blank=True)
    rating = models.IntegerField(default=5)
    rank = models.CharField(choices=RANK, max_length=50, default="1")
    has_set_rate = models.BooleanField(default=False,blank=True)
    has_set_profile = models.BooleanField(default=False) 
    has_added_asset = models.BooleanField(default=False)
    has_added_team = models.BooleanField(default=False)
    agent = models.CharField(max_length=200, null=True, blank=True)
    business_url = models.CharField(null=True,unique=True,max_length=255,blank=True)
    twitter_username = models.CharField(max_length=255,null=True, blank=True)
    instagram_username = models.CharField(max_length=255,null=True, blank=True)
    facebook_username = models.CharField(max_length=255,null=True, blank=True)
    tiktok_username = models.CharField(max_length=255,null=True, blank=True)
    status = models.CharField(choices=STATUS,default='AVAILABLE',max_length=100)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    joined_on = models.DateField(auto_now_add=True)

        
    class Meta:
        db_table = 'artisans'
        managed = True
        verbose_name = 'Artisan'
        verbose_name_plural = 'Artisans'
    

 
    def __str__(self):
        return self.name


class AgentModel(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'agents'
        managed = True
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def __str__(self):
        return self.name


@receiver(post_save, sender=ArtisanModel)
def send_welcome_and_activation_email(sender, instance, created, **kwargs):
    if created:
        #generate email token
        instance.email_activation_token = unique_otp_generator(instance)
        instance.save()

        #send email here
