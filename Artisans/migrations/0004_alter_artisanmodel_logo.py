# Generated by Django 4.1.2 on 2022-11-23 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Artisans', '0003_remove_artisanmodel_available_artisanmodel_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artisanmodel',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
