import email
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from Auth.models import User

class EmailNotificationModel(models.Model):
    """
        Email notificaton model
        it logs email notifications and send an email automatically on create of a record 
        failed emails will be tagged

    """

    EMAIL_TYPE = (
        ('1', 'User Registration Welcome'),
        ('2', 'Email Verification'),
        ('3', 'Merchant Team Invite'),
     )

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    email_address = models.EmailField()
    country = models.CharField(max_length=255,null=True)
    subject = models.CharField(max_length=50,null=True)
    message = models.CharField(max_length=255,null=True)
    html_message = models.CharField(max_length=255,null=True)
    email_type = models.CharField(choices=EMAIL_TYPE,max_length=255)
    extra_data = models.CharField(max_length=1000, null=True)
    time = models.DateTimeField(auto_now=True)
    sent = models.BooleanField(default=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'email_notifications'
        managed = True
        verbose_name = 'Email Notifications'
        verbose_name_plural = 'Email Notifications'

def send_email_notification(sender, instance, created, **kwargs):
    """
       send email notification on post save of notification record
    """
    if created:

        #send email notification here
        email_list = [instance.email_address,]
        subject = instance.subject
        message =instance.message
        html_message = instance.html_message
        

        try:

            #handle email sending here
            email_response = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=email_list, html_message=html_message)
            # email_from = settings.EMAIL_HOST_USER
            # email_response = send_mail(from_email=email_from,recipient_list=[email,],subject=subject,message=message)
            print(email_response)
            if not email_response:
                instance.sent = False
                instance.save()

        except Exception as error:  
            print(error)
            instance.sent = False
            instance.save()
try:
    post_save.connect(send_email_notification, sender=EmailNotificationModel)
except Exception as e:
    print(e)
