from django.contrib import admin
from Auth.models import User,ApiKey
# Register your models here.

admin.site.register(User)
admin.site.register(ApiKey)