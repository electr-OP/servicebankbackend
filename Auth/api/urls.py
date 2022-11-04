from tkinter import Y
from django.urls import include, path
from Auth.api.views import *


urlpatterns = [
    path("user/login",LoginView.as_view(),name="login"),
    path("user/register", RegisterView.as_view()),
    path("user/email-verify", ValidateEmailView.as_view()),
]