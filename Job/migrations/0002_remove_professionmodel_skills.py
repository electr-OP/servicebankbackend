# Generated by Django 4.1.2 on 2022-12-08 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professionmodel',
            name='skills',
        ),
    ]
