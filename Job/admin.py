from django.contrib import admin
from Job.models.professions import ProfessionModel,CategoryModel

# Register your models here.

admin.site.register(CategoryModel)
admin.site.register(ProfessionModel)
