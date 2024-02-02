# Generated by Django 4.1.3 on 2022-12-26 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crop_Details',
            fields=[
                ('farmer_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('farmer_name', models.CharField(max_length=100)),
                ('contact_no', models.PositiveIntegerField()),
                ('n', models.PositiveIntegerField()),
                ('p', models.PositiveIntegerField()),
                ('k', models.PositiveIntegerField()),
                ('temperature', models.CharField(max_length=10)),
                ('humidity', models.CharField(max_length=10)),
                ('ph', models.CharField(max_length=10)),
                ('rainfall', models.CharField(max_length=10)),
                ('prediction', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
    ]
