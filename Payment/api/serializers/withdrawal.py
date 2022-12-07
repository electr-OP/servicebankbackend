from rest_framework import serializers


class WidthdrawalSerializer(serializers.Serializer):

    account_no = serializers.CharField(required=True, allow_blank=False)
    bank_code = serializers.CharField(required=True, allow_blank=False)
    amount = serializers.CharField(required=True, allow_blank=False)