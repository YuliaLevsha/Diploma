from django.shortcuts import render, redirect
from Dealer.models import *
from django.contrib.auth.decorators import login_required
from Dealer.forms import *
from django.contrib import messages
from Customer.views import is_manager_buy, is_manager_customer, check_user
from django.core.paginator import Paginator
from Dealer.filters import DealerCarsFilter
from django.db.models import Subquery
from django.db.models import Sum
from Customer.models import TradeCar


@login_required
def add_dealer(request):
    if request.method == 'POST':
        form = DealerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('get_dealers')
        else:
            messages.error(request, 'Неверный ввод данных')
    form = DealerForm()
    return render(request, 'Dealer/add_dealer.html', {'context': form, 'is_buy': is_manager_buy(request)})


@login_required
def add_car(request):
    if request.method == 'POST':
        form_car = CarForm(request.POST, request.FILES)
        form_add_to_dealer = DealerCarsForm(request.POST)
        if form_car.is_valid() and form_add_to_dealer.is_valid():
            
            name = form_car.cleaned_data['name']
            car_model_name = form_car.cleaned_data['car_model']
            car_model = CarModel.objects.get(name=car_model_name)
            car_year = form_car.cleaned_data['car_year']
            car_color = form_car.cleaned_data['car_color']
            number_of_doors = form_car.cleaned_data['number_of_doors']
            body_type = form_car.cleaned_data['body_type']
            country = form_car.cleaned_data['country']
            car_number = form_car.cleaned_data['car_number']
            transmission = form_car.cleaned_data['transmission']
            car_class = form_car.cleaned_data['car_class']
            type_fuel = form_car.cleaned_data['type_fuel']
            type_drive = form_car.cleaned_data['type_drive']
            car_image = form_car.cleaned_data['car_image']
            
            Car.objects.create(name=name, car_model=car_model, car_year=car_year, car_color=car_color,
                                number_of_doors=number_of_doors, body_type=body_type, country=country,
                                car_number=car_number, transmission=transmission, car_class=car_class, 
                                type_fuel=type_fuel, type_drive=type_drive, car_image=car_image)
            
            car = Car.objects.get(name=name, car_model=car_model, car_year=car_year, car_color=car_color,
                                   number_of_doors=number_of_doors, body_type=body_type, country=country,
                                   car_number=car_number, transmission=transmission, car_class=car_class, 
                                   type_fuel=type_fuel, type_drive=type_drive)
            
            dealer_name = form_add_to_dealer.cleaned_data['dealer']
            dealer = Dealer.objects.get(name=dealer_name)
            price = form_add_to_dealer.cleaned_data['price']
            DealerCars.objects.create(dealer=dealer, price=price, car=car)
            return redirect('dealer_cars')
        else:
            messages.error(request, 'Неверный ввод данных')
    else:
        form_car = CarForm()
        form_add_to_dealer = DealerCarsForm()
    return render(request, 'Dealer/add_car.html', {'context1': form_car, 'context2': form_add_to_dealer, 'is_buy': is_manager_buy(request)})


@login_required
def get_delaer_cars(request):
    if request.method == "GET":
        bought_car = DealersSalesHistory.objects.filter(is_active=True).values_list('id_dealer_car')
        dealer_cars = DealerCars.objects.filter(is_active=True).exclude(id__in=Subquery(bought_car)).order_by('car__name')
        dealer_car_filter = DealerCarsFilter(request.GET, queryset=dealer_cars)
        dealer_cars = dealer_car_filter.qs
        paginator = Paginator(dealer_cars, per_page=15)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'Dealer/dealers.html', {'page_obj': page_object, 'dealer_filter': dealer_car_filter, 
                                                       'is_buy': is_manager_buy(request), 'is_customer': is_manager_customer(request)})


@login_required
def update_dealer(request, dealer):
    dealer_ = Dealer.objects.get(name=dealer)
    if request.method == 'GET':
        form = DealerForm(instance=dealer_)
        return render(request, 'Dealer/edit_dealer.html', {'context': form, 'is_buy': is_manager_buy(request)})
    elif request.method == 'POST':
        form = DealerForm(request.POST, instance=dealer_)
        if form.is_valid():
            form.save()
            return redirect('get_dealers')
        messages.error(request, 'Неверный ввод данных')
        return render(request, 'Dealer/edit_dealer.html', {'context': form, 'is_buy': is_manager_buy(request)})


def get_car(request, car_id):
    if request.method == "GET":
        car = Car.objects.get(id=car_id)
        return render(request, 'Dealer/car_page.html', {'car': car, 'is_buy': is_manager_buy(request), 'user_authenticated': check_user(request),
                                                        'is_customer': is_manager_customer(request)})


@login_required
def get_tradecar(request, car_id):
    if request.method == "GET":
        car = TradeCar.objects.get(id=car_id)
        return render(request, 'Dealer/car_page.html', {'car': car, 'is_buy': is_manager_buy(request), 'user_authenticated': check_user(request),
                                                        'is_customer': is_manager_customer(request)})


@login_required
def update_car(request, car_id):
    car = Car.objects.get(id=car_id)
    if request.method == 'GET':
        form = CarForm(instance=car)
        return render(request, 'Dealer/edit_car.html', {'context': form, 'is_buy': is_manager_buy(request)})
    elif request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('get_car', car_id=car_id)
        else:
            print(form.errors)
        messages.error(request, 'Неверный ввод данных')
        return render(request, 'Dealer/edit_car.html', {'context': form, 'is_buy': is_manager_buy(request)})


@login_required
def dealer_history(request):
    requests = DealersSalesHistory.objects.filter(is_active=True)
    paginator = Paginator(requests, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'Dealer/dealer_history.html', {'page_obj': page_object, 'is_buy': is_manager_buy(request)})


@login_required
def confirm_buy_by_dealership(request):
    requests = DealersSalesHistory.objects.filter(is_active=False)
    paginator = Paginator(requests, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'Dealer/dealer_confirm.html', {'page_obj': page_object, 'is_buy': is_manager_buy(request)})


@login_required
def checked(request, request_id):
    confirm = DealersSalesHistory.objects.get(id=request_id)
    car = DealerCars.objects.get(id=confirm.id_dealer_car.id)
    confirm.is_active = True
    confirm.save()
    car.is_active = False
    car.save()
    return redirect('dealer_confirm')
    

@login_required
def deny(request, request_id):
    get_obj = DealersSalesHistory.objects.get(id=request_id)
    deny = DealerCars.objects.get(id=get_obj.id_dealer_car.id)
    deny.is_booked = False
    deny.save()
    get_obj.delete()
    return redirect('dealer_confirm')


@login_required
def get_dealers(request):
    dealers = Dealer.objects.all().order_by('name')
    paginator = Paginator(dealers, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'Dealer/all_dealers.html', {'page_obj': page_object, 'is_buy': is_manager_buy(request)})
