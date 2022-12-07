from tkinter import Y
from django.urls import include, path
from Artisans.api.views.auth import *
from Artisans.api.views.profile import *


urlpatterns = [
    # path("artisan/login",LoginView.as_view(),name="login"),
    path("register", ArtisanRegisterView.as_view()),
    path("profile/update", UpdateArtisanProfileView.as_view(), name=""),
    path("get/enquiries", GetEnquiriesView.as_view(), name=""),
    path("update/enquiry", UpdateEnquiryView.as_view(), name=""),
    # path("artisan/email-verify", ValidateEmailView.as_view()),
]