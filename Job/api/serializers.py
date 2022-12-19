from rest_framework import serializers
from Artisans.models import ArtisanModel, ArtisanProfession
from Artisans.models import ArtisanEnquiry
from Artisans.api.serializers.profile import EnquirySerializer
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
        enquiries = ArtisanEnquiry.objects.filter(artisan=instance.id)
        # print(enquiries)
        rep['user'] = UserSerializer(user).data
        rep['enquiries'] = EnquirySerializer(enquiries, many=True).data

        return rep



class ProfessionSerializer(serializers.ModelSerializer):

    """
        Profession serializer
    """
    class Meta:
        model = ProfessionModel

        # Tuple of serialized custom model fields
        fields = "__all__"


class ArtisanProfessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisanProfession
        fields = "__all__"

    def to_representation(self, instance):

        result = super(ArtisanProfessionSerializer, self).to_representation(instance)

        name = ProfessionModel.objects.get(name=instance.name)
        result['name'] = name.name

        return result