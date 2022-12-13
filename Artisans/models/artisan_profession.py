from django.db import models
from Job.models import ProfessionModel
from Artisans.models import ArtisanModel


class ArtisanProfession(models.Model):

    artisan = models.ForeignKey(ArtisanModel, on_delete=models.CASCADE)
    name = models.ForeignKey(ProfessionModel, on_delete=models.CASCADE)
    skills = models.CharField(max_length=255,null=True)
    min_price = models.CharField(max_length=255, null=True)
    max_price = models.CharField(max_length=255, null=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return str(self.artisan) + " " + str(self.name)