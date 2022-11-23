from turtle import back
import uuid
from Auth.api.permissions import HasAPIKey, ExternalAPIKEYPermission
# from Notification.models.push import PushNotificationModel
import re
# from Payment.models.transactions import TransactionModel
# from Transporter.models.promo import PromoModel
from Auth.api.serializers import UserSerializer
from Job.models.professions import ProfessionModel
from Artisans.models import ArtisanModel
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
# from haversine import Unit
# import haversine as hs
from Notification.models.sms import SMSNotificationModel
from .serializers import *
from rest_framework_tracking.mixins import LoggingMixin
from django.db import transaction as db_transaction
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()

class GetProfessions(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        professions = ProfessionModel.objects.filter(is_active=True)
        serializer = ProfessionSerializer(professions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Search(LoggingMixin,APIView):
    """
        Get a professional
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            location = request.data['location']
            profession = request.data['profession']
            artisan_status = request.data.get('status')

            try:
                profession = ProfessionModel.objects.get(name=profession)
            except:
                return Response({"detail":"Invalid Category"}, status=status.HTTP_400_BAD_REQUEST)


            artisans = ArtisanModel.objects.filter(wallet_balance__gte=-6000,city=location,profession__name=profession.name,is_verified=True,is_active=True)
            if artisan_status:
                artisans = artisans.filter(status=artisan_status)            
            data = JobArtisanSerializer(artisans, many=True).data
            return Response({"success":True, "detail":data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

