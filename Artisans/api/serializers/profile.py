from rest_framework import serializers
from Artisans.models import ArtisanModel


class ArtisanSerializer(serializers.ModelSerializer):
    
    """
        Merchant serializer
    """
    class Meta:
        model = ArtisanModel

        # Tuple of serialized custom model fields
        fields = "__all__"

    
class ArtisanUpdateSerializer(serializers.ModelSerializer):
    
    """
        Merchant update data serializer
    """
    artisan_id = serializers.CharField(read_only=True)
    profession = serializers.ListField()
    class Meta:
        model = ArtisanModel

        # Tuple of serialized custom model fields
        fields = ('artisan_id',"address","latitude","longitude","website","description","logo", "country", "state", "state_code", "city", "profession", "has_set_profile")