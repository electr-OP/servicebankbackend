from django.db import models
from Artisans.models import ArtisanModel


class ArtisanEnquiry(models.Model):

    RESPONSE = [
        ("ACCEPT","Accept"),
        ("PENDING","Pending"),
        ("REJECT","Reject")
    ]

    artisan = models.ForeignKey(ArtisanModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    date = models.DateField(max_length=255, null=True)
    time = models.TimeField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True, null=True)
    response = models.CharField(choices=RESPONSE, max_length=255, default='PENDING')

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'artisan_enquiry'
        managed = True
        verbose_name = 'Artisan Enquiry'
        verbose_name_plural = 'Artisan Enquiries'
