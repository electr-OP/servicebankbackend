
from random import randint
from email import message
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from Auth.api.permissions import ActivatedUserPermission, AdminAPIKEYAuthorizationPermission,HasAPIKey
from Auth.api.serializers import *
from Artisans.models import *
from Artisans.api.serializers.profile import *
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.conf import settings
from Referral.models import ReferralModel
from Notification.models.email import EmailNotificationModel
from Notification.models.sms import SMSNotificationModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model, authenticate



class LoginView(LoggingMixin,APIView):
    """
        Login View

        Authenticated users using an email address and password
        params:
            email: an email address,
            password: a password
    """
    permission_classes = [
          AllowAny
        ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data['password']
            email = request.data.get('email')
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.email_activated == False:
                    return Response ({"success":False, "detail":"Account not activated"}, status=status.HTTP_400_BAD_REQUEST)
                tokens = RefreshToken.for_user(user)
                refresh = str(tokens)
                access = str(tokens.access_token)
                token_data = {
                  "refresh": refresh,
                  "access": access
                }

                #retreive user details
                try:
                    userdetails = UserSerializer(User.objects.get(id=user.id,is_active=True)).data
                except User.DoesNotExist:
                    return Response({"detail":"Account is not active, Please Contact Admin"}, status=status.HTTP_400_BAD_REQUEST)

                if userdetails.get('is_artisan'):
                    artisan_obj = ArtisanModel.objects.get(email=userdetails.get('email'),phone=userdetails.get('phone'))
                    artisan = ArtisanSerializer(artisan_obj).data
                    userdetails["artisan"] = artisan

                #register user device token if token was sent
                # fcm_token = request.data.get('fcm_token')
                # if fcm_token:
                #     DevicesModel.objects.create(user=user,fcm_token=fcm_token)

                return Response({
                 'detail':'Login Successfull',
                 'token': token_data,
                 'user_details':userdetails,

                },status=status.HTTP_200_OK)
            else:
                 return Response({"detail":"Incorrect Login details"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(LoggingMixin,APIView):
    """
        user Registration View
        params:
            :
    """
    permission_classes = [
          AdminAPIKEYAuthorizationPermission & HasAPIKey
       ]

    def post(self, request):
        n_data = request.data
        # serializer = UserRegisterationSerializer(data=n_data)
        # if serializer.is_valid():
        initial_save_point = transaction.savepoint()
        try:
            with transaction.atomic():

                #get password
                # password = make_password(request.data.get('password'))

                phone =request.data.get('phone')
                country=request.data.get('country')
                email = request.data.get('email')
                first_name = request.data.get('first_name')
                last_name = request.data.get('last_name')
                business_name = request.data.get('business_name')
                is_artisan = request.data.get('is_artisan')

                #check if email has been used
                try:
                    email_exists = User.objects.get(email=email,email_activated=True)
                    if email_exists:
                        return Response({"detail":"Email address has already been used"}, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    pass
                #check if phone has been used
                try:
                    phone_exists = User.objects.get(phone=phone,email_activated=True)
                    if phone_exists:
                        return Response({"detail":"Phone number has already been used"}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    pass      
                
                try:
                    initializer,created = User.objects.get_or_create(email=email, phone=phone, country=country)
                    initializer.first_name = first_name
                    initializer.last_name = last_name
                    initializer.token = randint(1000, 9999)
                    initializer.email_activated = False
                    initializer.set_password(request.data.get('password'))
                    initializer.save()  
                except IntegrityError as e:
                    
                    if str(e.__cause__) == 'UNIQUE constraint failed: users.phone':
                        return Response({"detail":"Phone number has already been used"}, status=status.HTTP_400_BAD_REQUEST)
                    elif str(e.__cause__) == "UNIQUE constraint failed: users.email":
                        return Response({"detail":"Email address has already been used"}, status=status.HTTP_400_BAD_REQUEST)
                 
                   
                #create user
                # user = serializer(initializer)
                #get user details
                user_details = UserSerializer(initializer).data
                print(user_details)
                # token = user_details.data.get('uid')
                # verify_link = settings.FRONTEND_URL + '/email-verify/' + token
                html_content = render_to_string(r'C:\Users\User\Desktop\Hayjay Programming\VS_Code_Projects\servicebankbackend\Notification\templates\otp_email.html', {'Brand':"Service Bank", 'token': initializer.token})
                text_content = strip_tags(html_content) 
                # EmailNotificationModel.objects.create(
                #     user=initializer,
                #     email_address=user_details.get('email'),
                #     email_type="2",
                #     subject="EMAIL VERIFICATION",
                #     message=text_content,
                #     html_message=html_content
                # )
                SMSNotificationModel.objects.create(
                    user=initializer,
                    phone_number=user_details.get('phone'),
                    message="Your Confirmation code is "+str(initializer.token),

                )

                #check referral ID
                referral_code = request.data.get('referral_code')
                if referral_code:
                    try:
                        referred_by = User.objects.get(referral_code=referral_code)
                        ReferralModel.objects.create(referred_user=initializer,referred_by=referred_by)
                    except User.DoesNotExist:
                        pass

                # register user device token if token was sent
                # fcm_token = request.data.get('fcm_token')
                # if fcm_token:
                #     DevicesModel.objects.create(user=user,fcm_token=fcm_token)

                if is_artisan:
                    initializer.is_artisan = True
                    initializer.save()
                    artisan = ArtisanModel.objects.create(
                        name=business_name,
                        email=email,
                        phone=phone
                    )

                return Response(
                    {
                    "detail":"Registration succesful",
                    "token":initializer.token,
                    # "user_details":user_details.data
                    },status=status.HTTP_200_OK)

        except Exception as error:
            print(error)
            transaction.savepoint_rollback(initial_save_point)
            return Response({"detail":"Error Occurred, Please contact admin"}, status=status.HTTP_400_BAD_REQUEST)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateEmailView(APIView):

    permission_classes = [
          AdminAPIKEYAuthorizationPermission & HasAPIKey
       ]
    def post(self, request):
        token = request.data.get('token')

        try:
            

            print(token)
            userExists = User.objects.get(uid=token, email_activated=False)
            userExists.email_activated = True
            userExists.save()

            user_details = UserSerializer(userExists)
            # print(user_details.data)

            #create access token for user
            tokens = RefreshToken.for_user(userExists)
            refresh = str(tokens)
            access = str(tokens.access_token)
            data = {
                    "refresh": refresh,
                    "access": access
                }

            return Response({"success":True, "tokens":data, "detail":user_details.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            try:
                userExists = User.objects.filter(uid=token, email_activated=True)
                if userExists:
                    return Response({"success":True, "detail":"Email Already Activated"}, status=status.HTTP_200_OK)
            except:
                pass
            return Response({"success":False, "detail":"Token not Found"}, status=status.HTTP_400_BAD_REQUEST)


class ValidateOTPView(APIView):

    permission_classes = [
          AdminAPIKEYAuthorizationPermission & HasAPIKey
       ]
    def post(self, request):
        token = request.data.get('token')
        phone = request.data.get('phone')
        email = request.data.get('email')

        try:
            

            print(token)
            userExists = User.objects.get(phone=phone, email=email, token=token, email_activated=False)
            userExists.email_activated = True
            userExists.save()

            user_details = UserSerializer(userExists).data
            # print(user_details.data)

            #create access token for user
            tokens = RefreshToken.for_user(userExists)
            refresh = str(tokens)
            access = str(tokens.access_token)
            data = {
                    "refresh": refresh,
                    "access": access
                }
            if user_details.get('is_artisan'):
                artisan_obj = ArtisanModel.objects.get(email=user_details.get('email'),phone=user_details.get('phone'))
                artisan = ArtisanSerializer(artisan_obj).data
                user_details["artisan"] = artisan
                nxtline = '\n'
                text_content = f"Dear {user_details.get('first_name')},{nxtline} {nxtline} Thank You for signing up as a Service Bank Artisan. \
                                {nxtline}{nxtline} First thing to do is to go to your profile and complete all details there, then you will be eligible for us to start matching you to clients.{nxtline} \
                                    We hope you enjoy your time as a Service Bank Artisan.{nxtline}{nxtline} Best Regards,{nxtline}Service Bank."
                EmailNotificationModel.objects.create(
                    user=userExists,
                    email_address=user_details.get('email'),
                    email_type="1",
                    subject="WELCOME TO SERVICE BANK",
                    message=text_content,
                    html_message=''
                )
            else:
                nxtline = '\n'
                text_content = f"Dear {user_details.get('first_name')},{nxtline} {nxtline} Thank You for signing up as a Service Bank User. \
                                {nxtline}{nxtline} Start searching for experts by going to https://app.servicehose.com/profiles.{nxtline} \
                                    We hope you enjoy your time as a Service Bank User.{nxtline}{nxtline} Best Regards,{nxtline}Service Bank."
                EmailNotificationModel.objects.create(
                    user=userExists,
                    email_address=user_details.get('email'),
                    email_type="1",
                    subject="WELCOME TO SERVICE BANK",
                    message=text_content,
                    html_message=''
                )

            return Response({"success":True, "tokens":data, "detail":user_details}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            try:
                userExists = User.objects.filter(phone=phone, email=email, token=token, email_activated=True)
                if userExists:
                    return Response({"success":True, "detail":"Email Already Activated"}, status=status.HTTP_200_OK)
            except:
                pass
            return Response({"success":False, "detail":"Token not Found"}, status=status.HTTP_400_BAD_REQUEST)


class GetUserDetailsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = UserSerializer(request.user).data

        return Response({"success":True, "detail":user}, status=status.HTTP_200_OK)