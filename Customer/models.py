from django.db import models
from base_model import BaseModel, default_car, PeriodCredit
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from typing import Dict
from Dealer.models import Car


class Customer(AbstractUser):
    """Модель пользователя, содержащая: дату рождения, паспорт, номер телефона"""
    date_birth = models.DateField(
        default=None, null=True, blank=False, verbose_name="Customer date birth"
    )
    passport = models.CharField(
        default=None, null=True, max_length=10, verbose_name="Customer passport"
    )
    phone = models.CharField(
        default=None, null=True, max_length=15, verbose_name="Customer phone"
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
        default_currency="USD",
        verbose_name="Max price of car to buy",
    )
    interested_in_car =  models.JSONField(
        encoder=None, decoder=None, verbose_name="Description cars to buy", default=default_car
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Customer who create offer",
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
        verbose_name="Customer who buy car",
        related_name="list_cars",
    )
    id_dealership_car = models.ForeignKey(
        "Dealer.DealersSalesHistory",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Car which was bought",
        related_name="customers",
    )
    cost = MoneyField(
        max_digits=7,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car price for customer",
    )

    class Meta:
        db_table = "customer_history"
        verbose_name = "CustomerPurchaseHistory"


class TradeCar(Car):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Customer car to change",
        related_name="trade_in_cars",
    )
    result_car = models.ManyToManyField(
        "Dealer.DealersSalesHistory",
        through="Customer.ResultTrade",
        verbose_name="Trade car result",
        related_name="result",
    )

    class Meta:
        db_table = "trade_car"
        verbose_name = "TradeCar"


class ResultTrade(BaseModel):
    customer_car = models.ForeignKey(
        TradeCar,
        on_delete=models.CASCADE,
        verbose_name="Customer car to change",
        related_name="customer_cars",
    )
    dealership_car = models.ForeignKey(
        "Dealer.DealersSalesHistory",
        on_delete=models.CASCADE,
        verbose_name="Dealership car to change",
        related_name="dealership_car",
    )
    
    class Meta:
        db_table = "result_trade"
        verbose_name = "ResultTrade"


class Credit(BaseModel):
    sum_credit = MoneyField(
        max_digits=7,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Sum of credit",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Customer who create credit",
        related_name="credits",
    )
    period_time = models.CharField(
        max_length=255, choices=PeriodCredit.choices, verbose_name="Period of credit", default=None
    )  
    
    class Meta:
        db_table = "credit"
        verbose_name = "Credit"
