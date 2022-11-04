from Auth.models.user import User
from rest_framework.fields import ChoiceField
from Artisans.models import ArtisanModel
from rest_framework import serializers


class ArtisanRegisterationSerializer(serializers.ModelSerializer):
    """
       Artisan registration serializer
    """

    class Meta: 
        model = ArtisanModel
        fields = ("name","country","state","state_code","rc_number","email","address","working_time_from","working_time_to")

    def create(self, validated_data):
        # data = validated_data.pop('transport_types')
        # data = validated_data.pop('pref_pickup_locs')
        print(validated_data)
        return ArtisanModel.objects.create(**validated_data)

