# Generated by Django 4.1.2 on 2022-12-26 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0003_categorymodel_professionmodel_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]