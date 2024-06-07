from celery import shared_task
from CarDealership.models import CarDealership
from Dealer.models import CarModel, DealerCars, DealersSalesHistory, Dealer
from Customer.models import Offer, Customer, CustomerPurchaseHistory
from decimal import Decimal


@shared_task
def look_for_cars_for_dealership_by_model():
    print('Таска началась')
    for dealership in CarDealership.objects.all():
        look_model = dealership.description_cars.get('car_model')
        model = CarModel.objects.get(id=look_model)
        count = 0
        for available_car in DealerCars.objects.filter(is_booked=False).order_by('price'):
            if available_car.car.car_model == model and count == 0:
                available_car.is_booked = True
                available_car.save()
                DealersSalesHistory.objects.create(id_dealer_car=available_car, car_dealership=dealership, is_active=False)
                update_count = Dealer.objects.get(id=available_car.dealer.id)
                count_uniqe_dealership = DealersSalesHistory.objects.filter(id_dealer_car__dealer__name=update_count.name).values('car_dealership').distinct().count()
                if update_count.customers_count != count_uniqe_dealership:
                    update_count.customers_count = count_uniqe_dealership
                    update_count.save()
                count += 1
                print('Таска изменила')
            else:
                continue
    print('Таска закончилась')


@shared_task
def look_for_cars_for_customer_by_model():
    print('Таска началась')
    for offer in Offer.objects.filter(is_active=True):
        user = Customer.objects.get(id=offer.customer)
        for available_car in DealersSalesHistory.objects.filter(is_booked=False, is_bought=False, is_active=True,
                                                                id_dealer_car__car__car_model=offer.interested_in_car.get('car_model'),
                                                                id_dealer_car__car__body_type=offer.interested_in_car.get('body_type'),
                                                                id_dealer_car__car__type_drive=offer.interested_in_car.get('type_drive'),
                                                                id_dealer_car__car__car_class=offer.interested_in_car.get('car_class'),
                                                                id_dealer_car__car__transmission=offer.interested_in_car.get('transmission'),
                                                                id_dealer_car__car__type_fuel=offer.interested_in_car.get('type_fuel'),
                                                                id_dealer_car__car__car_year__gte=offer.interested_in_car.get('car_year'),
                                                                ):
            new_price = available_car.id_dealer_car.price.amount * Decimal('1.2')
            print(new_price, offer.max_price.amount)
            if new_price <= offer.max_price.amount:
                available_car.is_booked = True
                available_car.save()
                CustomerPurchaseHistory.objects.create(customer=user, cost=new_price, id_dealership_car=available_car, is_active=False)
                offer.is_active = False
                print('Таска изменила')
            else:
                continue
    print('Таска закончилась')
