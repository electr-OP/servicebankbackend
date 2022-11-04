#API KEY CUSTOMIATION
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey,BaseAPIKeyManager
# from Merchant.models import MerchantModel
from Auth.models import User



class ApiKey(AbstractAPIKey):
    """
        Added merchant and user model as a foreign key to API KEY model
    """
    # merchant = models.ForeignKey(
    #     MerchantModel,
    #     on_delete=models.CASCADE,
    #     related_name="api_keys",
    #     blank=True,
    #     null=True
    # )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_keys",
        blank=True,
        null=True
    )
    is_agent = models.BooleanField(default=False)
    is_artisan = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)



    class Meta(AbstractAPIKey.Meta):
        db_table = 'api_keys'
        managed = True
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"


class APIKeyManager(BaseAPIKeyManager):
    def get_usable_keys(self):
        api_keys = super().get_usable_keys()
        return api_keys
    def get_from_key(self,key):
        api_key = super().get_from_key(key)
        return ApiKey.objects.get(name=api_key)