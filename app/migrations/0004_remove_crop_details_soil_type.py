# Generated by Django 4.1.5 on 2023-04-06 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_crop_details_fertilizer_crop_details_soil_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop_details',
            name='soil_type',
        ),
    ]