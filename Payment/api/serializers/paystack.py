from rest_framework import serializers

class PaystackPaymentVerifySerializer(serializers.Serializer):
    amount = serializers.FloatField(required=True)
    token = serializers.CharField(required=True, allow_blank=False)
    currency = serializers.CharField(required=False, allow_blank=True)