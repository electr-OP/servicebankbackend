from django.db import models

class ProfessionModel(models.Model):
   """
      Profession model
   """

   name = models.CharField(max_length=50)
   description = models.CharField(max_length=255)
   code = models.CharField(max_length=25)
   skills = models.CharField(max_length=255,null=True)
   is_active = models.BooleanField(default=True)

   def __str__(self):
      return self.name

   class Meta:
      db_table = 'profession'
      managed = True
      verbose_name = 'Profession'
      verbose_name_plural = 'Professions'

