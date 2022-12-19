# Generated by Django 4.1.2 on 2022-12-08 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0002_remove_professionmodel_skills'),
        ('Artisans', '0010_artisanenquiry_response'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtisanProfession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills', models.CharField(max_length=255, null=True)),
                ('min_price', models.CharField(max_length=255, null=True)),
                ('max_price', models.CharField(max_length=255, null=True)),
                ('is_verified', models.BooleanField(default=True)),
                ('artisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artisans.artisanmodel')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Job.professionmodel')),
            ],
        ),
    ]