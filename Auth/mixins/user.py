from django.db import models
from django.contrib.auth.models import (
    BaseUserManager
)
from django.db.models.signals import post_save

class CustomUserManager(BaseUserManager):
    def create_user(self,email, password=None):
        """
        Creates and saves a User with the given phone,email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
          email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password,
       
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
