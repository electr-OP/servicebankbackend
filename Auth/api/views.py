
from email import message
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from Auth.api.permissions import ActivatedUserPermission, AdminAPIKEYAuthorizationPermission,HasAPIKey
from Auth.api.serializers import *
from Artisans.models import *
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.conf import settings
from Referral.models import ReferralModel
from Notification.models.email import EmailNotificationModel
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
                 
                tokens = RefreshToken.for_user(user)
                refresh = str(tokens)
                access = str(tokens.access_token)
                token_data = {
                  "refresh": refresh,
                  "access": access
                }

                #retreive user details
                try:
                    userdetails = UserSerializer(User.objects.get(id=user.id,is_active=True))
                except User.DoesNotExist:
                    return Response({"detail":"Account is not active, Please Contact Admin"}, status=status.HTTP_400_BAD_REQUEST)


                #register user device token if token was sent
                # fcm_token = request.data.get('fcm_token')
                # if fcm_token:
                #     DevicesModel.objects.create(user=user,fcm_token=fcm_token)

                return Response({
                 'detail':'Login Successfull',
                 'token': token_data,
                 'user_details':userdetails.data,

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
        serializer = UserRegisterationSerializer(data=n_data)
        if serializer.is_valid():
            initial_save_point = transaction.savepoint()
            try:
                with transaction.atomic():

                    #get password
                    password = make_password(request.data.get('password'))

                    email = request.data.get('email')
                    first_name = request.data.get('first_name')
                    last_name = request.data.get('last_name')
                    is_artisan = request.data.get('is_artisan')
                                        
                    #create user
                    user = serializer.save(email=email,first_name=first_name,last_name=last_name,password=password)
                    #get user details
                    user_details = UserSerializer(user)
                    print(user_details.data)
                    token = user_details.data.get('uid')
                    verify_link = settings.FRONTEND_URL + '/email-verify/' + token
                    html_content = render_to_string(r'C:\Users\User\Desktop\Hayjay Programming\VS_Code_Projects\servicebankbackend\Notification\templates\email_verification.html', {'Brand':"Service Bank", 'link': verify_link})
                    text_content = strip_tags(html_content) 
                    EmailNotificationModel.objects.create(
                        user=user,
                        email_address=user_details.data.get('email'),
                        email_type="2",
                        subject="EMAIL VERIFICATION",
                        message=text_content,
                        html_message=html_content
                    )

                    #check referral ID
                    referral_code = request.data.get('referral_code')
                    if referral_code:
                        try:
                            referred_by = User.objects.get(referral_code=referral_code)
                            ReferralModel.objects.create(referred_user=user,referred_by=referred_by)
                        except User.DoesNotExist:
                            pass

                    # register user device token if token was sent
                    # fcm_token = request.data.get('fcm_token')
                    # if fcm_token:
                    #     DevicesModel.objects.create(user=user,fcm_token=fcm_token)

                    if is_artisan:
                        user.is_artisan = True
                        user.save()

                    return Response(
                        {
                        "detail":"Registration succesful",
                        "token":token,
                        # "user_details":user_details.data
                        },status=status.HTTP_200_OK)

            except Exception as error:
                print(error)
                transaction.savepoint_rollback(initial_save_point)
                return Response({"detail":"Error Occurred, Please contact admin"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateEmailView(APIView):

    permission_classes = [
          AdminAPIKEYAuthorizationPermission & HasAPIKey
       ]
    def post(self, request):
        token = request.data.get('token')

        try:
            


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

            return Response({"success":"True", "tokens":data, "detail":user_details.data}, status=status.HTTP_200_OK)
        except:
            try:
                userExists = User.objects.filter(uid=token, email_activated=True)
                if userExists:
                    return Response({"success":"True", "detail":"Email Already Activated"}, status=status.HTTP_200_OK)
            except:
                pass
            return Response({"success":"False", "detail":"Token not Found"}, status=status.HTTP_400_BAD_REQUEST)

