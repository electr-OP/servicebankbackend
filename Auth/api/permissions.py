#API KEY PERMISSION
from Auth.models import ApiKey
from rest_framework_api_key.permissions import BaseHasAPIKey
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.exceptions import APIException
from rest_framework import permissions


class HasAPIKey(BaseHasAPIKey):
    model = ApiKey


class IsMerchantUserPermission(permissions.BasePermission):
    """
    Global permission check if user is a valid merchant user and if merchant exist.
    """
    message = 'You are not allowed to do this'

    def has_permission(self, request, view):

        merchant_id = request.data['merchant_id'] if 'merchant_id' in request.data else None

        if not merchant_id or not request.user:
            raise _NotAllowedException()
        
        #check if merchant exist
        try:
            merchant = MerchantModel.objects.get(merchant_id=merchant_id)
        except MerchantModel.DoesNotExist:
            raise _MerchantDoesNotExistException
 
        #check if user is a merchant user
        try:
            user_confirmation = MerchantUserModel.objects.get(merchant=merchant.id,user=request.user)
        except MerchantUserModel.DoesNotExist:
            raise _NotAllowedException()  
        except MerchantUserModel.MultipleObjectsReturned:
            user_confirmation = MerchantUserModel.objects.filter(merchant=merchant.id,user=request.user).first()
        return True


class MerchantAuthorizationPermission(permissions.BasePermission):
    """
    Global permission check if merchant is authorized.
    """
    message = 'Please activate your email account to continue'

    def has_permission(self, request, view):

        #retrieve merchant details from key
        if "Access-Key" not in request.headers:
            raise _NoAPIKEYException()
            
        key = request.headers["Access-Key"]
        if not key:
            raise _NoAPIKEYException()

        try:
            merchant = ApiKey.objects.get_from_key(key).merchant
        except:
            raise _InvalidAPIKEYException()


        if merchant.email_activated and merchant.is_active:
            return True
        raise _MerchantAuthorizationException()


class AdminAPIKEYAuthorizationPermission(permissions.BasePermission):
    """
    Global permission check if admin is authorized using api key.
    """ 
    message = 'you cannot perform this action'

    def has_permission(self, request,view):

        #retrieve merchant details from key
        if "Access-Key" not in request.headers:
            raise _NoAPIKEYException()
            
        key = request.headers["Access-Key"]
        if not key:
            raise _NoAPIKEYException()

        try:
            api_key = ApiKey.objects.get_from_key(key)
            if api_key.is_admin:
                return True
            raise _NotAllowedException()
        except:
            raise _InvalidAPIKEYException()


class ExternalAPIKEYPermission(permissions.BasePermission):
    """
    Global permission check if external api connection is authorized using api key.
    """ 
    message = 'you cannot perform this action'
    def has_permission(self, request,view):

        #retrieve user details from key
        if "Access-Key" not in request.headers:
            raise _NoAPIKEYException()
            
        key = request.headers["Access-Key"]
        if not key:
            print('22222')
            raise _NoAPIKEYException()


        try:
            api_key = ApiKey.objects.get_from_key(key)
            if api_key.user:
                request.data['user'] = api_key.user

                return True
            # raise _NotAllowedException()
        except Exception as e:
            print('33333', e)
            raise _InvalidAPIKEYException()


class ActivatedUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        # if request.user.is_active and request.user.email_activated:
        if request.user.is_active and request.user.email_activated:
            return True
        return False






class _MerchantAuthorizationException(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = 'Please activate your email account to continue.'


class _NoAPIKEYException(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = 'Please add your api-key in the request header.'
 

class _InvalidAPIKEYException(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = 'Api-key is not valid'
 
class _NotAllowedException(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = 'You are not allowed to do this'

class _MerchantDoesNotExistException(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = 'Merchant does not exist or has been disabled'