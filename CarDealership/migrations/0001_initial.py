# Generated by Django 5.0.6 on 2024-05-20 19:45

import base_model
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarDealership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Car dealership name')),
                ('location', models.CharField(max_length=200, verbose_name='Car dealership address')),
                ('description_cars', models.JSONField(default=base_model.default_car, verbose_name='Description future cars to sale')),
            ],
            options={
                'verbose_name': 'CarDealership',
                'db_table': 'car_dealership',
            },
        ),
    ]