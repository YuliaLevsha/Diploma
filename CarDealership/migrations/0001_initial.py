# Generated by Django 5.0.6 on 2024-06-06 09:15

import base_model
import simple_history.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CarDealership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("location", models.CharField(max_length=200, verbose_name="Адрес")),
                (
                    "description_cars",
                    models.JSONField(
                        default=base_model.default_car,
                        verbose_name="Марка специализации",
                    ),
                ),
            ],
            options={
                "verbose_name": "CarDealership",
                "db_table": "car_dealership",
            },
        ),
        migrations.CreateModel(
            name="HistoricalCarDealership",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(blank=True, editable=False)),
                ("updated_at", models.DateTimeField(blank=True, editable=False)),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("location", models.CharField(max_length=200, verbose_name="Адрес")),
                (
                    "description_cars",
                    models.JSONField(
                        default=base_model.default_car,
                        verbose_name="Марка специализации",
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical CarDealership",
                "verbose_name_plural": "historical CarDealerships",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
