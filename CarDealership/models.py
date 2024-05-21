from django.db import models
from base_model import BaseModel, default_car
from typing import Any


class CarDealership(BaseModel):
    """Модель автосалона, содержащая:
    название, адрес, характеристики авто, список машин на продажу"""
    name = models.CharField(max_length=255, verbose_name="Car dealership name")
    location = models.CharField(
        max_length=200,
        verbose_name="Car dealership address"
    )
    description_cars = models.JSONField(
        encoder=None, decoder=None, verbose_name="Description future cars to sale", default=default_car
    )
    dealership_cars = models.ManyToManyField(
        "Dealer.DealerCars",
        through="Dealer.DealersSalesHistory",
        verbose_name="Dealership cars to sale",
        related_name="dealerships",
    )

    class Meta:
        db_table = "car_dealership"
        verbose_name = "CarDealership"
