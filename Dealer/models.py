from django.db import models
from django_countries.fields import CountryField
from base_model import BaseModel, G8Countries, Colors, BodyTypes, DriveTypes
from djmoney.models.fields import MoneyField
from typing import Any


class Dealer(BaseModel):
    """Модель поставщика, которая содержит:
    название, год основания, число покупателей, список машин для продажи"""
    name = models.CharField(max_length=255, verbose_name="Dealer name")
    foundation_year = models.PositiveIntegerField(
        verbose_name="Dealer foundation year"
    )
    customers_count = models.PositiveIntegerField(
        default=0, verbose_name="Dealer customers count"
    )
    dealer_cars = models.ManyToManyField(
        "Car",
        through="DealerCars",
        verbose_name="Dealers cars to sale",
        related_name="dealers",
    )

    class Meta:
        db_table = "dealer"
        verbose_name = "Dealer"
    
    def __str__(self) -> str:
        return self.name


class CarModel(BaseModel):
    """Модель марка машины с названием"""
    name = models.CharField(max_length=255, verbose_name="Name model")
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "car_model"
        verbose_name = "CarModel"


class Car(BaseModel):
    """Модель машина с полями:
    id на модель, год создания, цвет, количество дверей, тип кузова, тип привода, 
    страна производитель, объем топливного бака и изображение"""
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        verbose_name="Car model",
        related_name="cars",
    )
    car_year = models.PositiveIntegerField(
        blank=False, verbose_name="Car year"
    )
    car_color = models.CharField(max_length=255, choices=Colors.choices, verbose_name="Car color", default=None)
    number_of_doors = models.PositiveIntegerField(
        default=2, blank=True, verbose_name="Number of doors in car"
    )    
    body_type = models.CharField(
        max_length=255, choices=BodyTypes.choices, verbose_name="Car body type", default=None
    )    
    type_drive = models.CharField(
        max_length=255, choices=DriveTypes.choices, verbose_name="Car type drive", default=None
    )
    country = CountryField(
        countries=G8Countries,
        verbose_name="Car country",
        default=None
    )
    volume_fuel_tank = models.PositiveIntegerField(
        blank=False, verbose_name="Car volume of fuel tank"
    )
    car_image = models.ImageField(upload_to='cars/', null=True, max_length=255, default=None)

    class Meta:
        db_table = "car"
        verbose_name = "Car"


class DealerCars(BaseModel):
    """Список машин поставщика с ценами"""
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        null=True,
        related_name="list_cars",
        verbose_name="Dealer of car",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=True,
        related_name="list_dealers",
        verbose_name="Car to sale",
    )
    price = MoneyField(
        max_digits=7,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car price from dealer",
    )

    class Meta:
        db_table = "dealer_cars"
        verbose_name = "DealerCars"


class DealersSalesHistory(
    BaseModel
):
    """История продаж для поставщика и список машин, которые продает автосалон содержит:
    скидка, если есть подходящая, и финальная стоимость с учетом скидки"""
    id_dealer_car = models.ForeignKey(
        DealerCars,
        on_delete=models.CASCADE,
        null=True,
        related_name="sales_history",
        verbose_name="Dealer and car"
    )
    car_dealership = models.ForeignKey(
        "CarDealership.CarDealership",
        on_delete=models.CASCADE,
        null=True,
        related_name="list_cars",
        verbose_name="Car dealership who bought car"
    )
    is_booked = models.BooleanField(default=False, verbose_name='Car is booked by user or not')
    is_bought = models.BooleanField(default=False, verbose_name='Car is bought by user or not')

    class Meta:
        db_table = "dealers_history"
        verbose_name = "DealersSalesHistory"
