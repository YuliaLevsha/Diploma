from django.shortcuts import render, redirect
from Dealer.models import *
from django.contrib.auth.decorators import login_required
from Dealer.forms import *
from django.contrib import messages
from Customer.views import is_manager_buy
from django.core.paginator import Paginator
from CarDealership.models import CarDealership


@login_required
def add_dealer(request):
    if request.method == 'POST':
        form = DealerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dealer_cars')
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
            
            car_model_name = form_car.cleaned_data['car_model']
            car_model = CarModel.objects.get(name=car_model_name)
            car_year = form_car.cleaned_data['car_year']
            car_color = form_car.cleaned_data['car_color']
            number_of_doors = form_car.cleaned_data['number_of_doors']
            body_type = form_car.cleaned_data['body_type']
            country = form_car.cleaned_data['country']
            type_drive = form_car.cleaned_data['type_drive']
            volume_fuel_tank = form_car.cleaned_data['volume_fuel_tank']
            car_image = form_car.cleaned_data['car_image']
            
            Car.objects.create(car_model=car_model, car_year=car_year, car_color=car_color,
                                number_of_doors=number_of_doors, body_type=body_type, country=country,
                                type_drive=type_drive, volume_fuel_tank=volume_fuel_tank, car_image=car_image)
            
            car = Car.objects.get(car_model=car_model, car_year=car_year, car_color=car_color,
                                  number_of_doors=number_of_doors, body_type=body_type, country=country,
                                  type_drive=type_drive, volume_fuel_tank=volume_fuel_tank)
            
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
        dealer = Dealer.objects.all()
        dealer_cars = DealerCars.objects.select_related('dealer').select_related('car')
        paginator = Paginator(dealer_cars, per_page=8)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'Dealer/dealers.html', {'dealers': dealer, 'page_obj': page_object, 'is_buy': is_manager_buy(request)})


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
            return redirect('main')
        messages.error(request, 'Неверный ввод данных')
        return render(request, 'Dealer/edit_dealer.html', {'context': form, 'is_buy': is_manager_buy(request)})


@login_required
def get_car(request, car_id):
    if request.method == "GET":
        car = Car.objects.get(id=car_id)
        return render(request, 'Dealer/car_page.html', {'car': car, 'is_buy': is_manager_buy(request)})


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
    car = DealerCars.objects.filter(is_active=True, car__car_model__name='BMV').order_by('price').first()
    history = DealersSalesHistory.objects.filter(is_active=True)
    dealerships = CarDealership.objects.all()
    searches = []
    for dealership in dealerships:
        search_model = dealership.description_cars.get('car_model')
        searches.append(search_model)
    return render(request, 'Dealer/dealer_history.html', {'car': searches, 'is_buy': is_manager_buy(request)})


@login_required
def confirm_buy_by_dealership(request):
    requests = DealersSalesHistory.objects.filter(is_active=False)
