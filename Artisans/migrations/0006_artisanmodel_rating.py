# Generated by Django 4.1.2 on 2022-11-23 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Artisans', '0005_alter_artisanmodel_facebook_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artisanmodel',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]