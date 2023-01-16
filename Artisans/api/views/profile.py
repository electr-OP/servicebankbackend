# from Merchant.models.merchant import PrefPickupLocations
# from Transporter.models.transport_type import TransportTypeModel
# from Merchant.models.rate import MerchantTransportChannelModel
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from Artisans.api.serializers.profile import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from Artisans.models import ArtisanModel, AgentModel
from Artisans.models import ArtisanEnquiry
from Job.models import ProfessionModel
# from Merchant.permissions import IsMerchantUserPermission
from rest_framework_tracking.mixins import LoggingMixin
# from Merchant.helper import get_geometry


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
            return Response({"success":False ,"detail":"Arisan Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ArtisanSerializer(artisan)
        data = serializer.data
        # pref_pickup_locs_data = data.pop("pref_pickup_locs")
        # pref_pickup_locs = []
        # for item in pref_pickup_locs_data:
        #     inst = PrefPickupLocations.objects.get(id=item)
        #     pref_pickup_locs.append(inst.location)
        # data["pref_pickup_locs"] = pref_pickup_locs
        return Response({"success":True ,"detail":data}, status=status.HTTP_200_OK)
        

class GetAgentsView(APIView):

    permission_classes = [AllowAny,]

    def get(self, request):

        agents = AgentModel.objects.all()

        data = AgentSerializer(agents, many=True)

        return Response({"success":True, "detail":data}, status=status.HTTP_200_OK)



# class GetAllUsersMerchantView(LoggingMixin,APIView):
#     """
#         Get all merchant user belong too
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         merchant = MerchantUserModel.objects.filter(user=request.user)
#         serializer = UsersMerchantPermissionSerializer(merchant, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)



# class GetAllMerchantTransportTypeView(LoggingMixin,APIView):
#     """
#         Get all transport types of merchant
#     """
#     permission_classes = [IsAuthenticated & IsMerchantUserPermission]

#     def post(self, request):
#         merchant_id = request.data['merchant_id']
#         transport_types = MerchantTransportChannelModel.objects.filter(merchant__merchant_id=merchant_id)
#         serializer = MerchantTransportTypesSerializer(transport_types, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)



class UpdateArtisanProfileView(LoggingMixin,APIView):
    """
        Update artisan profile
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ArtisanUpdateSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data)
            artisan_id = request.data['artisan_id']
            artisan = ArtisanModel.objects.get(artisan_id=artisan_id)
            request.POST._mutable = True

            professions_name = request.data.pop('profession')
            professions_id = []
            for profession in professions_name:
                obj = ProfessionModel.objects.get(name=profession)
                professions_id.append(obj.id)

            # print(request.data)
            # pref_pickup_locs_data = request.data.pop("pref_pickup_locs")
            # pref_pickup_locs_data = pref_pickup_locs_data[0].split(',')
            # pref_pickup_locs = []
            # for item in pref_pickup_locs_data:
            #     try:
            #         inst = PrefPickupLocations.objects.get(location=item)
            #     except PrefPickupLocations.DoesNotExist:
            #         try:
            #             loc = f'{item}, Lagos, Nigeria'
            #             details = get_geometry(loc)
            #         except:
            #             return Response({"detail": "Invalid Location Request"}, status=status.HTTP_400_BAD_REQUEST)
            #         if details['candidates'] != []:
            #             gp_address = details['candidates'][0]['formatted_address']
            #             latlng = details['candidates'][0]['geometry']['location']
            #             lat = str(latlng.get("lat"))
            #             lng = str(latlng.get("lng"))
            #             print(lat, lng, gp_address)
            #         else:
            #             return Response({"detail": "No Location returned"})
            #         inst = PrefPickupLocations(location=item, latitude=lat, longitude=lng)
            #         inst.save()
            #     pref_pickup_locs.append(inst.id)
            # request.data["pref_pickup_locs"] = pref_pickup_locs
            request.data['profession'] = professions_id
            print(request.data)
            request.POST._mutable = False
            serializer.update(instance=artisan,validated_data=request.data)

            artisan.has_set_profile = True
            artisan.save()

            return Response({"detail":"Artisan Updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdateMerchantAvailabilityView(LoggingMixin,APIView):
#     """
#         Update merchant availability
#     """
#     permission_classes = [IsAuthenticated & IsMerchantUserPermission]

#     def post(self, request):
#         merchant_id = request.data.get('merchant_id')
#         available = request.data.get('status')
#         merchant = MerchantModel.objects.get(merchant_id=merchant_id)
#         merchant.available = available
#         merchant.save()
#         return Response({"success":"true", "message":"status set"}, status=status.HTTP_200_OK)


# class MerchantUpdateTransportRateView(LoggingMixin,APIView):
#     """
#         update transport rates of merchant
#     """
#     permission_classes = [IsAuthenticated & IsMerchantUserPermission]

#     def post(self, request):
#         serializer = MerchantTransportRateUpdateSerializer(data=request.data)
#         if serializer.is_valid():
#             merchant_id = request.data['merchant_id']
#             merchant = MerchantModel.objects.get(merchant_id=merchant_id)
#             rate = request.data['rate']
#             lowest_capped_amount = request.data.get('lowest_capped_amount')
#             is_active = request.data['is_active']
 
#             #verify transport code
#             try:
#                 transport_type = TransportTypeModel.objects.get(code=request.data['transport_type_code'])
#             except TransportTypeModel.DoesNotExist or Exception:
#                 return Response({"detail":"Invalid transport type"}, status=status.HTTP_400_BAD_REQUEST)
            

#             #create or update merchant 
#             try:
#                 transport_type_config = MerchantTransportChannelModel.objects.get(transport_type=transport_type.id,merchant=merchant.id)
#                 transport_type_config.rate = rate
#                 transport_type_config.is_active = is_active
#                 transport_type_config.lowest_capped_amount = lowest_capped_amount
#                 transport_type_config.save()
#             except MerchantTransportChannelModel.DoesNotExist:
#                 try:
#                     MerchantTransportChannelModel.objects.create(transport_type=transport_type,rate=rate,merchant=merchant)
#                 except Exception:
#                     pass
            
#             merchant.has_set_rate = True
#             merchant.save(0)

#             #TODO notify admin here of a configuration change for approval and investigation

#             return Response({"detail":"Rate Updated"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetEnquiriesView(LoggingMixin, APIView):

    """
        Update artisan profile
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        artisan_id = request.data.get('artisan_id')
        artisan = ArtisanModel.objects.get(artisan_id=artisan_id)
        enquiry = ArtisanEnquiry.objects.filter(artisan=artisan)
        enquiry_pending = ArtisanEnquiry.objects.filter(artisan=artisan, response='PENDING')
        enquiry_accept = ArtisanEnquiry.objects.filter(artisan=artisan, response='ACCEPT')

        enquiry_data = EnquirySerializer(enquiry, many=True).data
        enquiry_pending_data = EnquirySerializer(enquiry_pending, many=True).data
        enquiry_accept_data = EnquirySerializer(enquiry_accept, many=True).data


        return Response({'success':True, 'detail':{'all': enquiry_data, 'pending': enquiry_pending_data,
                            'accept': enquiry_accept_data}}, status=status.HTTP_200_OK)

                
class UpdateEnquiryView(LoggingMixin, APIView):

     permission_classes = [IsAuthenticated]

     def post(self, request):
        response = request.data.get('response')
        enquiry_id = request.data.get('enquiry_id')

        enquiry = ArtisanEnquiry.objects.get(id=enquiry_id)
        enquiry.response = response
        enquiry.save()

        return Response({'success':True, 'detail':'Enquiry Updated'})