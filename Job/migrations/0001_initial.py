# Generated by Django 4.1.2 on 2022-11-19 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=25)),
                ('skills', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Profession',
                'verbose_name_plural': 'Professions',
                'db_table': 'profession',
                'managed': True,
            },
        ),
    ]
