from rest_framework import serializers
from Artisans.models import ArtisanModel
from Auth.api.serializers import UserSerializer
from ..models.professions import ProfessionModel
from django.contrib.auth import get_user_model

User = get_user_model()


class SearchSerializer(serializers.Serializer):
    """
       search serializer
    """

    location = serializers.CharField(required=True, allow_blank=False)
    profession = serializers.CharField(required=True, allow_blank=False)
    status = serializers.CharField(required=False, allow_blank=True)


class JobArtisanSerializer(serializers.ModelSerializer):


    class Meta:
        model = ArtisanModel
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = User.objects.get(email=instance.email, phone=instance.phone)
        rep['user'] = UserSerializer(user).data

        return rep



class ProfessionSerializer(serializers.ModelSerializer):

    """
        Transport type serializer
    """
    class Meta:
        model = ProfessionModel

        # Tuple of serialized custom model fields
        fields = "__all__"
