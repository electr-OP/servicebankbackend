from django.db import models

class CategoryModel(models.Model):
   """
      Category model
   """

   name = models.CharField(max_length=50)
   image = models.ImageField(null=True, blank=True)
   is_active = models.BooleanField(default=True)

   def __str__(self):
      return self.name

   class Meta:
      db_table = 'category'
      managed = True
      verbose_name = 'Category'
      verbose_name_plural = 'Categories'

class ProfessionModel(models.Model):
   """
      Profession model
   """

   category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True)
   name = models.CharField(max_length=50)
   description = models.CharField(max_length=255)
   code = models.CharField(max_length=25)
   image = models.ImageField(null=True, blank=True)
   is_active = models.BooleanField(default=True)

   def __str__(self):
      return self.name

   class Meta:
      db_table = 'profession'
      managed = True
      verbose_name = 'Profession'
      verbose_name_plural = 'Professions'

