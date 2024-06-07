from django.db import models
from base_model import BaseModel, default_car
from typing import Any
from simple_history.models import HistoricalRecords


class CarDealership(BaseModel):
    """Модель автосалона, содержащая:
    название, адрес, характеристики авто, список машин на продажу"""
    name = models.CharField(max_length=255, verbose_name="Название")
    location = models.CharField(
        max_length=200,
        verbose_name="Адрес"
    )
    description_cars = models.JSONField(
        encoder=None, decoder=None, verbose_name="Марка специализации", default=default_car
    )
    dealership_cars = models.ManyToManyField(
        "Dealer.DealerCars",
        through="Dealer.DealersSalesHistory",
        verbose_name="Машины",
        related_name="dealerships",
    )
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "car_dealership"
        verbose_name = "CarDealership"
