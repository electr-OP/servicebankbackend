from django.urls import include, path
from Job.api.views import *


urlpatterns = [
    path("search/professionals",Search.as_view(),name="search"),
    path("get/professions",GetProfessions.as_view(),name="professions"),
    path("get/artisan",GetAnArtisanView.as_view(),name="get-artisans"),
    path("create/enquiry",CreateEnquiryView.as_view(),name="enquiry"),
    path("get/pricing",GetPricingView.as_view(),name="get_pricing"),
    path("update/pricing",UpdatePricingView.as_view(),name="update_pricing"),


]