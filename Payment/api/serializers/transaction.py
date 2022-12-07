from rest_framework import serializers
from Payment.models.transaction import *
from Auth.api.serializers import *
from Artisans.api.serializers.profile import *

 #transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('id')
        response['transaction_user'] = UserSerializer(instance.transaction_user).data
        
        if instance.transaction_status == '1':
            response['transaction_status'] = {'id':1,'transaction_status_name':'Failed'}
        elif instance.transaction_status == '2':
            response['transaction_status'] = {'id':2,'transaction_status_name':'Success'}
        elif instance.transaction_status == '3':
            response['transaction_status'] = {'id':3,'transaction_status_name':'Processing'}
        else:
            response['transaction_status'] = {'id':1,'transaction_status_name':'Processing'}
    
        response['transaction_artisan'] = ArtisanSerializer(instance.transaction_artisan).data

        if instance.transaction_type == "1":
           response['transaction_type'] =  {"id":1,"name":"Wallet Funding"}
        elif instance.transaction_type =="2":
           response['transaction_type'] = {"id":2,"name":"Debit"}
        elif instance.transaction_type =="3":
               response['transaction_type'] = {"id":3,"name":"Payment Recieved"}

        return response