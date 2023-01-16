# from Auth.models.device import DevicesModel
# from Merchant.models.rate import MerchantTransportChannelModel
# from Transporter.models.transport_type import TransportTypeModel
from rest_framework import status
from Auth.models import User
from Artisans.models.users import ArtisanUserModel
from Artisans.api.serializers.auth import ArtisanRegisterationSerializer
from Auth.api.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated, AllowAny
from Auth.api.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# from Merchant.serializers import MerchantEmailActivationSerializer,MerchantLoginSerializer,UsersMerchantPermissionSerializer
from Artisans.models import ArtisanModel, AgentModel
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from Notification.models import EmailNotificationModel, SMSNotificationModel
from Auth.api.serializers import UserRegisterationSerializer
from rest_framework_tracking.mixins import LoggingMixin
from Artisans.api.helper import get_geometry
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class ArtisanRegisterView(LoggingMixin,APIView):
    """
        Merchant Registration View
    """
    permission_classes = [HasAPIKey]

    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data) #user registration serializer
        artisan_serializer = ArtisanRegisterationSerializer(data=request.data) #merchant serializer

        #validate data
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not artisan_serializer.is_valid():
            return Response(artisan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get Lat & Lng values
        region = request.data.get('region')
        region = f'{region}, Lagos, Nigeria'
        try:
            details = get_geometry(region)
        except:
            return Response({"detail": "Invalid Location Request"}, status=status.HTTP_400_BAD_REQUEST)
        if details['candidates'] != []:
            gp_address = details['candidates'][0]['formatted_address']
            latlng = details['candidates'][0]['geometry']['location']
            lat = str(latlng.get("lat"))
            lng = str(latlng.get("lng"))
            print(lat, lng, gp_address)
        else:
            return Response({"detail": "No Location returned"})
        #create user account
        password = make_password(request.data["password"])
        user = serializer.save(password=password)

        #get data for merchant createion
        email = request.data.get('email')
        phone = request.data.get('phone')
        rc_number = request.data.get('rc_number')
        from_time = request.data.get('from_time')
        to_time = request.data.get('to_time')

        #create merchant account
        artisan = artisan_serializer.save(email=email,phone=phone,rc_number=rc_number,latitude=lat,longitude=lng,working_time_from=from_time,working_time_to=to_time)
  
        #add merchant permission for user
        artisan_permission = ArtisanUserModel(
            artisan=artisan,
            user=user,
            email_address=user.email,
            permission=1, #business owner permission
            invitation_accepted=True
        )
        artisan_permission.save()


        # #create transport types
        # print(request.data['transport_types'])
        # for transport_type in request.data['transport_types']:
        #     try:
        #         MerchantTransportChannelModel.objects.create(
        #             merchant=merchant,
        #             transport_type=TransportTypeModel.objects.get(code=transport_type),
        #         )
        #     except TransportTypeModel.DoesNotExist:
        #         pass
            
        #send otp
        #send sms token to user
        if phone:
            SMSNotificationModel.objects.create(
                    country=request.data.get('country'),
                    phone_number=request.data.get('phone'),
                    message="Your One-Time-Password is "+str(artisan.email_activation_token)
                )
        #send email to the user with the email address
        # extra_data = {
        #     "merchant_id":merchant.id,
        #     "user_permission":merchant_permission.id
        #  }

        email_data = {'Brand': 'MyTransporter',
                        'otp': str(artisan.email_activation_token)}
        html_content = render_to_string(r'C:\Users\User\Desktop\Hayjay Programming\VS_Code_Projects\servicebankbackend\Notification\templates\otp_email.html', email_data)
        text_content = strip_tags(html_content) 
        email = EmailNotificationModel(
                user=user,
                email_address=user.email,
                subject="Welcome to MyTransporter",
                email_type=1, # merchant registration type
                message= html_content,
                html_message= text_content
            )
            
        email.save()

        return Response({"message":"Merchant Account created","merchant_id":artisan.artisan_id},status=status.HTTP_200_OK)


class ActivateArtisanAccountView(LoggingMixin,APIView):
    
    """
        Activate Artisan account
    """
    permission_classes = [HasAPIKey]

    def post(self, request):


        token = request.data['token']
        artisan_id = request.data['artisan_id']

        #update merchant account
        try:
            artisan = ArtisanModel.objects.get(email_activation_token=token,artisan_id=artisan_id)
        except ArtisanModel.DoesNotExist:
            return Response({"detail":"Invalid Token/Otp"}, status=status.HTTP_400_BAD_REQUEST)
        artisan.email_activated = True
        artisan.save()

        #update user account
        try:
            user  = User.objects.get(email=artisan.email)
            user.email_activated = True
            user.save()
        except User.DoesNotExist:
            pass

        return Response({"detail":"Artisan Activated"}, status=status.HTTP_200_OK)
