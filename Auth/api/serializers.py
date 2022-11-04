from Auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
        Login serializer
    """
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=True, allow_blank=False)


class UserRegisterationSerializer(serializers.ModelSerializer):
    """
       user registration serializer
    """

    # reference = serializers.CharField(required=True,allow_blank=False)
    # phone = serializers.CharField(required=False)
    # email= serializers.CharField(required=False)

    class Meta: 
        model = User
        fields = ("email","first_name","last_name","password")
    
    def create(self, validated_data):
        # validated_data.pop('reference', None)
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
      Main user model serializer
    """

    class Meta: 
        model = User
        fields = ("first_name","last_name","address","longitude","latitude","email","city","gender","country","wallet_balance","referral_code","has_updated_profile","email_activated",
        "has_added_card","date_of_birth","is_active","currency","image","uid","public_key","secret_key")
    
    def to_representation(self, instance):
        result = super(UserSerializer, self).to_representation(instance)
 
        #append complete url to image
        image_url = None
        if instance.image:
            image_url =instance.image.url
        result['image'] = image_url

        return result