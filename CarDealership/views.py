from django.shortcuts import render, redirect
from Dealer.models import DealersSalesHistory
from django.contrib.auth.decorators import login_required
from CarDealership.forms import *
from django.contrib import messages
from Customer.views import is_manager_customer, check_user
from django.core.paginator import Paginator
from CarDealership.filters import DealershipCarsFilter
from django.db.models import F, Value
from djmoney.models.fields import MoneyField
from decimal import Decimal
from Customer.models import CustomerPurchaseHistory
from Customer.models import *
from django.db.models import Subquery


@login_required
def add_dealership(request):
    if request.method == 'POST':
        form = DealershipForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            car_model_name = form.cleaned_data['car_model']
            car_model = CarModel.objects.get(name=car_model_name)
            json_data = {
                'car_model': car_model.pk,
                'car_year': None,
                'car_color': None,
                'number_of_doors': None,
                'body_type': None,
                'type_drive': None,
                'country': None,
                'volume_fuel_tank': None
            }
            if CarDealership.objects.filter(name=name).exists():
                messages.error(request, 'Такой автосалон существует!')
                return render(request, 'CarDealership/create_dealership.html', {'context': form, 'is_customer': is_manager_customer(request)})  
            CarDealership.objects.create(name=name, location=location, description_cars=json_data)
            return redirect('get_dealerships')
        messages.error(request, 'Неверный ввод данных')
    form = DealershipForm()
    return render(request, 'CarDealership/create_dealership.html', {'context': form, 'is_customer': is_manager_customer(request)})


@login_required
def update_dealership(request, dealership):
    dealership_ = CarDealership.objects.get(name=dealership)
    if request.method == 'GET':
        form = DealershipForm(initial={
            'name': dealership_.name,
            'location': dealership_.location,
            'car_model': CarModel.objects.get(id=dealership_.description_cars.get('car_model'))
        })
        return render(request, 'CarDealership/edit_dealership.html', {'context': form, 'is_customer': is_manager_customer(request)})
    elif request.method == 'POST':
        form = DealershipForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            car_model_name = form.cleaned_data['car_model']
            car_model = CarModel.objects.get(name=car_model_name)
            json_data = {
                'car_model': car_model.pk,
                'car_year': None,
                'car_color': None,
                'number_of_doors': None,
                'body_type': None,
                'type_drive': None,
                'country': None,
                'volume_fuel_tank': None
            }
            if CarDealership.objects.filter(name=name).exists():
                messages.error(request, 'Такой автосалон существует!')
                return render(request, 'CarDealership/create_dealership.html', {'context': form, 'is_customer': is_manager_customer(request)})  
            dealership_.name = name
            dealership_.location = location
            dealership_.description_cars = json_data
            dealership_.save()
            
            return redirect('get_dealerships')
        messages.error(request, 'Неверный ввод данных')
        return render(request, 'CarDealership/edit_dealership.html', {'context': form, 'is_customer': is_manager_customer(request)})


def get_delaership_cars(request):
    if request.method == "GET":
        change_car = ResultTrade.objects.filter(is_active=True).values_list('dealership_car__id')
        dealership_cars = DealersSalesHistory.objects.filter(is_active=True, is_bought=False).exclude(id__in=Subquery(change_car))\
            .annotate(new_price=F('id_dealer_car__price') * Value(Decimal('1.2'), output_field=MoneyField())).order_by('id_dealer_car__car__name')
        dealership_car_filter = DealershipCarsFilter(request.GET, queryset=dealership_cars)
        dealership_cars = dealership_car_filter.qs
        paginator = Paginator(dealership_cars, per_page=15)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'CarDealership/cars.html', {'page_obj': page_object, 'dealership_filter': dealership_car_filter, 
                                                           'is_customer': is_manager_customer(request),
                                                            'user_authenticated': check_user(request)})


@login_required
def get_dealerships(request):
    dealers = CarDealership.objects.all().order_by('name')
    paginator = Paginator(dealers, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'CarDealership/all_dealerships.html', {'page_obj': page_object, 'is_customer': is_manager_customer(request)})


@login_required
def dealership_history(request):
    requests = CustomerPurchaseHistory.objects.filter(is_active=True)
    paginator = Paginator(requests, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'CarDealership/dealership_history.html', {'page_obj': page_object, 'is_customer': is_manager_customer(request)})


@login_required
def confirm_buy_by_customer(request):
    requests = CustomerPurchaseHistory.objects.filter(is_active=False)
    paginator = Paginator(requests, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'CarDealership/dealership_confirm.html', {'page_obj': page_object, 'is_customer': is_manager_customer(request)})


@login_required
def checked(request, request_id):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            payment = form.cleaned_data['type_payment']
            object = CustomerPurchaseHistory.objects.get(id=request_id)
            confirm = DealersSalesHistory.objects.get(id=object.id_dealership_car.id)
            object.is_active = True
            object.type_payment = payment
            object.save()
            
            confirm.is_bought = True
            confirm.save()
            return redirect('confirm_offer')
    form = ConfirmForm()
    return render(request, 'CarDealership/confirm.html', {'context': form, 'is_customer': is_manager_customer(request)})
    

@login_required
def deny(request, request_id):
    object = CustomerPurchaseHistory.objects.get(id=request_id)
    deny = DealersSalesHistory.objects.get(id=object.id_dealership_car.id)
    deny.is_booked = False
    deny.save()
    object.delete()
    return redirect('confirm_offer')


@login_required
def confirm_credit(request):
    requests = Credit.objects.filter(is_active=False)
    paginator = Paginator(requests, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'CarDealership/credit_confirm.html', {'page_obj': page_object, 'is_customer': is_manager_customer(request)})


@login_required
def checked_credit(request, request_id):
    object = Credit.objects.get(id=request_id)
    object.is_active = True
    object.save()
    return redirect('confirm_credit')
    

@login_required
def deny_credit(request, request_id):
    object = Credit.objects.get(id=request_id)
    object.delete()
    return redirect('confirm_credit')


@login_required
def get_cardealership_requests(request):
    cardealers_req = DealersSalesHistory.objects.filter(is_active=False).order_by('car_dealership__name')
    paginator = Paginator(cardealers_req, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'CarDealership/all_requests.html', {'page_obj': page_object, 'is_customer': is_manager_customer(request)})


@login_required
def confirm_trade_dealership(request):
    accept_car = ResultTrade.objects.all().values_list('customer_car')
    requests = TradeCar.objects.filter(is_active=True).exclude(id__in=Subquery(accept_car)).order_by('name')
    paginator = Paginator(requests, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'CarDealership/trade_confirm.html', {'page_obj': page_object, 'is_customer': is_manager_customer(request)})


@login_required
def confirm_trade(request, request_id):
    if request.method == 'POST':
        form = CarChooseForm(request.POST)
        if form.is_valid():
            car_choose = form.cleaned_data['car_choose']
            car = TradeCar.objects.get(id=request_id)
            ResultTrade.objects.create(is_active=False, dealership_car=car_choose, customer_car=car)
            return redirect('confirm_trade')
    form = CarChooseForm()
    return render(request, 'CarDealership/confirm_trade.html', {'context': form, 'is_customer': is_manager_customer(request)})


@login_required
def deny_trade(request, request_id):
    car = TradeCar.objects.get(id=request_id)
    car.is_active = False
    car.save()
    return redirect('confirm_trade')
