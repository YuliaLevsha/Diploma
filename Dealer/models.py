from django.db import models
from base_model import *
from djmoney.models.fields import MoneyField
from typing import Any
from simple_history.models import HistoricalRecords


class Dealer(BaseModel):
    """Модель поставщика, которая содержит:
    название, год основания, число покупателей, список машин для продажи"""
    name = models.CharField(max_length=255, verbose_name="Название")
    foundation_year = models.PositiveIntegerField(
        verbose_name="Год основания"
    )
    customers_count = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во клиентов"
    )
    dealer_cars = models.ManyToManyField(
        "Car",
        through="DealerCars",
        verbose_name="Машины",
        related_name="dealers",
    )
    history = HistoricalRecords()

    class Meta:
        db_table = "dealer"
        verbose_name = "Dealer"
    
    def __str__(self) -> str:
        return self.name


class CarModel(BaseModel):
    """Модель марка машины с названием"""
    name = models.CharField(max_length=255, verbose_name="Название")
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "car_model"
        verbose_name = "CarModel"


class Car(BaseModel):
    """Модель машина с полями:
    id на модель, название, год создания, цвет, количество дверей, тип кузова, тип привода, 
    страна производитель, изображение, коробка передачи, тип топлива"""
    name = models.CharField(max_length=100, verbose_name='Полное название', default=None)
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        verbose_name="Марка",
        related_name="cars",
    )
    car_year = models.PositiveIntegerField(
        blank=False, verbose_name="Год создания"
    )
    car_color = models.CharField(max_length=255, choices=Colors.choices, verbose_name="Цвет", default=None)
    number_of_doors = models.PositiveIntegerField(
        default=2, blank=True, verbose_name="Кол-во дверей"
    )    
    body_type = models.CharField(
        max_length=255, choices=BodyTypes.choices, verbose_name="Кузов", default=None
    )    
    type_drive = models.CharField(
        max_length=255, choices=DriveTypes.choices, verbose_name="Привод", default=None
    )
    country = models.CharField(
        max_length=255, choices=Countries.choices, verbose_name="Производитель", default=None
    )
    car_number = models.CharField(max_length=20, verbose_name='Номер', default=None)
    transmission = models.CharField(
        max_length=20, choices=Transmission.choices, default=None, verbose_name='КПП'
    )
    car_class = models.CharField(
        max_length=10, choices=ConfigurationType.choices, default=None, verbose_name='Комплектация'
    )
    type_fuel = models.CharField(
        max_length=20, choices=FuelType.choices, default=None, verbose_name='Топливо'
    )
    car_image = models.ImageField(upload_to='cars/', null=True, max_length=255, default=None)
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return self.name
    
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
        verbose_name="Поставщик",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=True,
        related_name="list_dealers",
        verbose_name="Машина",
    )
    price = MoneyField(
        max_digits=7,
        decimal_places=2,
        default_currency="BYN",
        verbose_name="Цена",
    )
    is_booked = models.BooleanField(default=False, verbose_name='Забронировано')
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.dealer) + " " + str(self.car)

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
        verbose_name="Машина и поставщик"
    )
    car_dealership = models.ForeignKey(
        "CarDealership.CarDealership",
        on_delete=models.CASCADE,
        null=True,
        related_name="list_cars",
        verbose_name="Автосалон"
    )
    is_booked = models.BooleanField(default=False, verbose_name='Забронировано клиентом')
    is_bought = models.BooleanField(default=False, verbose_name='Куплено клиентом')
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.id_dealer_car) + " " + str(self.car_dealership)

    class Meta:
        db_table = "dealers_history"
        verbose_name = "DealersSalesHistory"
