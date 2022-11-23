from django.urls import include, path
from Job.api.views import *


urlpatterns = [
    path("search/professionals",Search.as_view(),name="search"),
    path("get/professions",GetProfessions.as_view(),name="professions"),


]