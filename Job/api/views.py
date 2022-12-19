from turtle import back
import uuid
from Auth.api.permissions import HasAPIKey, ExternalAPIKEYPermission
# from Notification.models.push import PushNotificationModel
import re
# from Payment.models.transactions import TransactionModel
# from Transporter.models.promo import PromoModel
from Auth.api.serializers import UserSerializer
from Artisans.api.serializers.profile import ArtisanSerializer
from Job.models.professions import ProfessionModel
from Artisans.models import ArtisanModel
from Artisans.models import ArtisanEnquiry
from Artisans.models import ArtisanProfession
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


class GetPricingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        artisan_id = request.data.get('artisan_id')
        artisan = ArtisanModel.objects.get(artisan_id=artisan_id)
        pricings = ArtisanProfession.objects.filter(artisan=artisan)
        # print(pricings)
        data = ArtisanProfessionSerializer(pricings, many=True).data
        return Response({"success":True, "detail":data}, status=status.HTTP_200_OK)


class UpdatePricingView(LoggingMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        artisan_id = request.data.get('artisan_id')
        list_of_data = request.data.get('list_of_data')

        artisan = ArtisanModel.objects.get(artisan_id=artisan_id)

        # list_objects = [ArtisanProfession(artisan=artisan,name=ProfessionModel.objects.get(name=rec['name']),min_price=rec['min_price'],max_price=rec['max_price']) for rec in list_of_data]
        for rec in list_of_data:
            try:
                artisan_profession = ArtisanProfession.objects.get(artisan=artisan, name__name=rec['name'])
                artisan_profession.min_price = rec['min_price']
                artisan_profession.max_price = rec['max_price']
                artisan_profession.save()
            except ArtisanProfession.DoesNotExist:
                artisan_profession = ArtisanProfession.objects.create(artisan=artisan,name=ProfessionModel.objects.get(name=rec['name']),min_price=rec['min_price'],max_price=rec['max_price'])
            artisan_profession = ArtisanProfession.objects.filter(artisan=artisan)
            data = ArtisanProfessionSerializer(artisan_profession, many=True).data
        # ArtisanProfession.objects.bulk_create(list_objects, update_conflicts=True, update_fields=['min_price', 'max_price'], unique_fields=['artisan','name'])
        return Response({"success":True, "detail":data}, status=status.HTTP_200_OK)



class GetAnArtisanView(LoggingMixin,APIView):
    """
        Get an artisan detail
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        artisan_id = request.data['artisan_id']
        try:
            artisan = ArtisanModel.objects.get(artisan_id=artisan_id)
        except ArtisanModel.DoesNotExist:
            return Response({"success":False ,"detail":"Artisan Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(phone=artisan.phone, email=artisan.email)
        except User.DoesNotExist:
            return Response({"success":False ,"detail":"Artisan Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ArtisanSerializer(artisan)
        user_serializer = UserSerializer(user).data
        data = serializer.data
        data['user'] = user_serializer
        professions_data = data.pop("profession")
        professions = []
        for item in professions_data:
            inst = ProfessionModel.objects.get(id=item)
            professions.append(inst.name)
        data["profession"] = professions
        return Response({"success":True ,"detail":data}, status=status.HTTP_200_OK)
        

class Search(LoggingMixin,APIView):
    """
        Get a professional
    """

    permission_classes = [AllowAny]

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


class CreateEnquiryView(LoggingMixin, APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        artisan = request.data.get('artisan')
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        message = request.data.get('message')
        address = request.data.get('address')
        date = request.data.get('date')
        time = request.data.get('time')

        artisan_obj = ArtisanModel.objects.get(artisan_id=artisan)

        enquiry = ArtisanEnquiry.objects.create(
            artisan = artisan_obj,
            name = name,
            email = email,
            phone = phone,
            message = message,
            address = address,
            date = date,
            time = time

        )

        return Response({"success":True, "detail":"Enquiry Created"}, status=status.HTTP_201_CREATED)
