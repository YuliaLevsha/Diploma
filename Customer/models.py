from django.db import models
from base_model import *
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from typing import Dict
from simple_history.models import HistoricalRecords


class Customer(AbstractUser):
    """Модель пользователя, содержащая: дату рождения, паспорт, номер телефона"""
    date_birth = models.DateField(
        default=None, null=True, blank=False, verbose_name="Дата рождения"
    )
    passport = models.CharField(
        default=None, null=True, max_length=10, verbose_name="Паспорт"
    )
    phone = models.CharField(
        default=None, null=True, max_length=15, verbose_name="Телефон"
    )

    class Meta:
        db_table = "customer"
        verbose_name = "Customer"


class Offer(BaseModel):
    """Модель запроса для бронирования машины содержит: максимальную стоимость,
    кто создал, характеристика машины, которую хочет купить"""
    max_price = MoneyField(
        max_digits=7,
        decimal_places=2,
        default_currency="BYN",
        verbose_name="Мах стоимость",
    )
    
    interested_in_car =  models.JSONField(
        encoder=None, decoder=None, verbose_name="Характеристики машины", default=default_car
    )
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Клиент",
        related_name="offers",
    )

    class Meta:
        db_table = "offer"
        verbose_name = "Offer"


class CustomerPurchaseHistory(
    BaseModel
):
    """История покупок пользователя / история продаж для автосалона"""
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Клиент",
        related_name="list_cars",
    )
    id_dealership_car = models.ForeignKey(
        "Dealer.DealersSalesHistory",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Машина и автосалон",
        related_name="customers",
    )
    cost = MoneyField(
        max_digits=7,
        decimal_places=2,
        default_currency="BYN",
        verbose_name="Цена",
    )
    
    type_payment = models.CharField(
        max_length=20, choices=Payment.choices, default=None, verbose_name='Способ оплаты', null=True
    )
    history = HistoricalRecords()

    class Meta:
        db_table = "customer_history"
        verbose_name = "CustomerPurchaseHistory"


class TradeCar(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Полное название', default=None)
    car_model = models.ForeignKey(
        'Dealer.CarModel',
        on_delete=models.CASCADE,
        verbose_name="Марка",
        related_name="trade_cars",
        default=None
    )
    car_year = models.PositiveIntegerField(
        blank=False, verbose_name="Год создания", default=None
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
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Клиент",
        related_name="trade_in_cars",
    )
    result_car = models.ManyToManyField(
        "Dealer.DealersSalesHistory",
        through="Customer.ResultTrade",
        verbose_name="Предложение",
        related_name="result",
    )

    class Meta:
        db_table = "trade_car"
        verbose_name = "TradeCar"


class ResultTrade(BaseModel):
    customer_car = models.ForeignKey(
        TradeCar,
        on_delete=models.CASCADE,
        verbose_name="Обмен",
        related_name="customer_cars",
    )
    dealership_car = models.ForeignKey(
        "Dealer.DealersSalesHistory",
        on_delete=models.CASCADE,
        verbose_name="Предложение",
        related_name="dealership_car",
    )
    history = HistoricalRecords()
    
    class Meta:
        db_table = "result_trade"
        verbose_name = "ResultTrade"


class Credit(BaseModel):
    sum_credit = MoneyField(
        max_digits=7,
        decimal_places=2,
        default_currency="BYN",
        verbose_name="Сумма",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        related_name="credits",
    )
    period_time = models.CharField(
        max_length=255, choices=PeriodCredit.choices, verbose_name="Период", default=None
    )  
    
    history = HistoricalRecords()
    
    class Meta:
        db_table = "credit"
        verbose_name = "Credit"
