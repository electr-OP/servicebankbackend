# from Notification.lib.africaistalking import AfricaIsTalkingClass
# from Notification.lib.aws_sns import AWSsmsClass
# from Notification.lib.sendchamp import SendChampSmsClass
# from Notification.lib.aws import AWS
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from Notification.utils.termii import TermiiSmsClass

# from Notification.lib.termii import TermiiSmsClass

class SMSNotificationModel(models.Model):
    """
        SMS notificaton model
        it logs sms notifications and send an sms automatically on create of a record 
        failed sms will be tagged
    """
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    phone_number = models.CharField(max_length=30)
    country = models.CharField(max_length=255,null=True)
    message = models.TextField(null=True)
    time = models.DateTimeField(auto_now=True)
    sent = models.BooleanField(default=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'sms_notifications'
        managed = True
        verbose_name = 'SMS Notifications'
        verbose_name_plural = 'SMS Notifications'


def send_sms_notification(sender, instance, created, **kwargs):
    """
       send sms notification on post save of notification record
    """
    if created:

        #send sms notification here
        phone_number = instance.phone_number
        message =instance.message

        try:

            # handle handle sms sending here
        #     #AWS
        #     sms_response = AWSsmsClass.send_sms(phone_number,message)
        #     if not sms_response['status']:
        #         instance.sent = False
        #         instance.save()

        #TERMII
            termii = TermiiSmsClass.send_sms(phone_number,message)
            # if not termii['status'] and not sms_response['status']:
            if not termii['status']:
                instance.sent = False
                instance.save()

        except Exception as error: 
            #TERMII
            termii = TermiiSmsClass.send_sms(phone_number,message)
             
        #     print(error)
        #     instance.sent = False
        #     instance.save()

post_save.connect(send_sms_notification, sender=SMSNotificationModel)

