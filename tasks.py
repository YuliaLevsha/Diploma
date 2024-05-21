from celery import shared_task
from Dealer.models import DealersSalesHistory, DealerCars, CarModel
from CarDealership.models import CarDealership
from Customer.models import Offer, CustomerPurchaseHistory
from django.utils import timezone
import random
from moneyed import Money
from typing import Any


@shared_task
def search_cars_to_dealership() -> None:
    dealerships = CarDealership.objects.all()
    for dealership in dealerships:
        search_model = dealership.description_cars.get('car_model')
        car_model = CarModel.objects.get(pk=search_model)
        car = DealerCars.objects.filter(is_active=True, car__car_model__name=car_model).order_by('price').first()
        if not DealersSalesHistory.objects.get(is_active=False, id_dealer_car=car, car_dealership=dealership).exists():
            DealersSalesHistory.objects.create(is_active=False, id_dealer_car=car, car_dealership=dealership)
