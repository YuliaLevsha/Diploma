from django.shortcuts import render, redirect
from Dealer.models import DealersSalesHistory
from django.contrib.auth.decorators import login_required
from CarDealership.forms import *
from django.contrib import messages
from Customer.views import is_manager_customer
from django.core.paginator import Paginator


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
            CarDealership.objects.create(name=name, location=location, description_cars=json_data)
            return redirect('get_dealership_cars')
        messages.error(request, 'Неверный ввод данных')
    form = DealershipForm()
    return render(request, 'CarDealership/create_dealership.html', {'context': form, 'is_customer': is_manager_customer(request)})


@login_required
def get_cars(request):
    if request.method == "GET":
        dealer = CarDealership.objects.all()
        dealer_cars = DealersSalesHistory.objects.select_related('dealer').select_related('car')
        paginator = Paginator(dealer_cars, per_page=8)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        #return render(request, 'Dealer/dealers.html', {'dealers': dealer, 'page_obj': page_object, 'is_buy': is_manager_buy(request)})
