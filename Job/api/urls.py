from django.urls import include, path
from Job.api.views import *


urlpatterns = [
    path("search/professionals",Search.as_view(),name="search"),
    path("get/categories",GetCategories.as_view(),name="categories"),
    path("get/professions",GetProfessions.as_view(),name="professions"),
    path("get/category/professions",GetCategoryProfessions.as_view(),name="category-professions"),
    path("get/artisan",GetAnArtisanView.as_view(),name="get-artisans"),
    path("get/related/artisans",RelatedArtisans.as_view(),name="related-artisans"),
    path("create/enquiry",CreateEnquiryView.as_view(),name="enquiry"),
    path("get/pricing",GetPricingView.as_view(),name="get_pricing"),
    path("update/pricing",UpdatePricingView.as_view(),name="update_pricing"),


]