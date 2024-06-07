from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from Customer.forms import *
from Customer.models import *
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage 
from Customer.tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from Dealer.forms import CarForm
from Dealer.models import *
from django.core.paginator import Paginator
from CarDealership.filters import DealershipCarsFilter
from django.db.models import F, Value
from djmoney.models.fields import MoneyField
from decimal import Decimal
from CarDealership.models import *


# отправка сообщения на почту
def send_message_to_email(request, user, subject, email_template, url, text) -> None:
    current_site = get_current_site(request) 
    mail_subject = subject
    message = render_to_string(email_template, 
                               {'user': user, 
                                'domain': current_site.domain, 
                                'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                                'token':account_activation_token.make_token(user),
                                'todo': url,
                                'text': text
                                }
                               ) 
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email]) 
    email.send() 


# проверка на определенного пользователя
def check_user(request):
    return True if request.user.is_authenticated else False


def is_manager_buy(request):
    try:
        user = Customer.objects.get(username=request.user)
    except(Customer.DoesNotExist):
        user = None
    if user is not None:
        try:
            manager_buy_group = Group.objects.get_or_create(name='Manager_buy')[0]
        except (Group.DoesNotExist):
            manager_buy_group = False
        return True if manager_buy_group in user.groups.all() else False
    return False


def is_manager_customer(request):
    try:
        user = Customer.objects.get(username=request.user)
    except(Customer.DoesNotExist):
        user = None
    if user is not None:
        try:
            manager_customer_group = Group.objects.get_or_create(name='Manager_customer')[0]
        except (Group.DoesNotExist):
            manager_customer_group = False
        return True if manager_customer_group in user.groups.all() else False
    return False


def is_director(request):
    try:
        user = Customer.objects.get(username=request.user)
    except(Customer.DoesNotExist):
        user = None
    if user is not None:
        try:
            director_group = Group.objects.get_or_create(name='Director')[0]
        except (Group.DoesNotExist):
            director_group = False
        return True if director_group in user.groups.all() else False
    return False


# подтверждение по почте
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Аккаунт подвержден, можете авторизовываться.') 
    else:
        return HttpResponse('Ссылка не действительна.')


def reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                return redirect('login')
        else:
            form = ResetPasswordForm()
    return render(request, 'Customer/reset_password.html', {'context': form})


# странички
def main_page(request):
    return render(request, 'Customer/pages/main.html', {'is_buy': is_manager_buy(request), 
                                                        'is_director': is_director(request),
                                                        'is_customer': is_manager_customer(request),
                                                        'user_authenticated': check_user(request)})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_message_to_email(request=request, 
                                  user=user, 
                                  subject='Подтверждение почты',
                                  email_template='Customer/email.html',
                                  url='activate',
                                  text='Пожалуйста, перейдите по ссылке, чтобы подвердить регистрацию:')
            
            messages.success(request, 'На вашу почту отправлено письмо для подтверждения!')
        
    else:
        form = RegisterForm()
    return render(request, 'Customer/pages/register.html', {'context': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        messages.error(request, 'Пароль неверный или имя пользователя')
    form = AuthenticationForm()
    return render(request, 'Customer/pages/login.html', {'context': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if 'cancel' in request.POST:
            return redirect('user_profile')
        elif 'save' in request.POST:
            if form.is_valid():
                user = Customer.objects.get(username=request.user)
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль изменен!')
    else:
        form = ChangePasswordForm()
    return render(request, 'Customer/pages/change_password.html', {'context': form, 'is_buy': is_manager_buy(request),
                                                                   'user_authenticated': check_user(request)})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():
            user = Customer.objects.get(email=form.cleaned_data['email'])
            send_message_to_email(request=request,
                                  user=user,
                                  subject='Сброс пароля',
                                  email_template='Customer/email.html',
                                  url='reset',
                                  text='Пожалуйста, перейдите по ссылке, чтобы сбросить пароль:')
            messages.success(request, 'На вашу почту отправлено письмо для подтверждения!')
    else:
        form = ForgotForm()
    return render(request, 'Customer/pages/forgot_password.html', {'context': form})


@login_required
def change_user_info(request):
    user = Customer.objects.get(username=request.user)
    if request.method == 'GET':
        form = ChangeCustomerForm(instance=user)
        return render(request, 'Customer/pages/change_user.html', {'context': form, 'user': user, 'user_authenticated': check_user(request)})
    elif request.method == 'POST':
        form = ChangeCustomerForm(request.POST, instance=user)
        if 'cancel' in request.POST:
            return redirect('main')
        elif 'save' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('user_profile')
            messages.error(request, 'Неверный ввод данных')
        return render(request, 'Customer/pages/change_user.html', {'context': form, 'is_buy': is_manager_buy(request),
                                                                   'user_authenticated': check_user(request)})


@login_required
def get_user(request):
    user = Customer.objects.get(username=request.user)
    return render(request, 'Customer/pages/profile.html', {'user': user, 'is_buy': is_manager_buy(request),
                                                           'user_authenticated': check_user(request)})


@login_required
def create_offer(request):
    user = Customer.objects.get(username=request.user)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            max_price = form.cleaned_data['max_price']
            car_model_name = form.cleaned_data['car_model']
            car_model = CarModel.objects.get(name=car_model_name)
            car_year = form.cleaned_data['car_year']
            body_type = form.cleaned_data['body_type']
            type_drive = form.cleaned_data['type_drive']
            transmission = form.cleaned_data['transmission']
            car_class = form.cleaned_data['car_class']
            type_fuel = form.cleaned_data['type_fuel']
            json_data = {
                'car_model': car_model.pk,
                'car_year': car_year,
                'car_color': None,
                'number_of_doors': 2,
                'body_type': body_type,
                'type_drive': type_drive,
                'country': None,
                'car_number': None,
                'car_class': car_class, 
                'transmission': transmission,
                'type_fuel': type_fuel
            }
            Offer.objects.create(max_price=max_price, customer=user, interested_in_car=json_data)
            return redirect('main')
        messages.error(request, 'Неверный ввод данных')
    form = OfferForm()
    return render(request, 'Customer/pages/create_offer.html', {'context': form, 'user_authenticated': check_user(request)})


@login_required
def create_credit(request):
    user = Customer.objects.get(username=request.user)
    if request.method == 'POST':
        form = CreateCreditForm(request.POST)
        if form.is_valid():
            sum_credit = form.cleaned_data['sum_credit']
            period_time = form.cleaned_data['period_time']
            
            Credit.objects.create(sum_credit=sum_credit, customer=user, period_time=period_time, is_active=False)
            return redirect('main')
        messages.error(request, 'Неверный ввод данных')
    form = CreateCreditForm()
    return render(request, 'Customer/pages/create_credit.html', {'context': form, 'user_authenticated': check_user(request)})


@login_required
def create_trade_car(request):
    if request.method == 'POST':
        user = Customer.objects.get(username=request.user)
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            car_model_name = form.cleaned_data['car_model']
            car_model = CarModel.objects.get(name=car_model_name)
            car_year = form.cleaned_data['car_year']
            car_color = form.cleaned_data['car_color']
            number_of_doors = form.cleaned_data['number_of_doors']
            body_type = form.cleaned_data['body_type']
            country = form.cleaned_data['country']
            car_number = form.cleaned_data['car_number']
            transmission = form.cleaned_data['transmission']
            car_class = form.cleaned_data['car_class']
            type_fuel = form.cleaned_data['type_fuel']
            type_drive = form.cleaned_data['type_drive']
            car_image = form.cleaned_data['car_image']
            if TradeCar.objects.create(name=name, car_model=car_model, car_year=car_year, car_color=car_color,
                                       number_of_doors=number_of_doors, body_type=body_type, country=country,
                                       car_number=car_number, transmission=transmission, car_class=car_class, 
                                       type_fuel=type_fuel, type_drive=type_drive, car_image=car_image,
                                       customer=user).exists():
                messages.error(request, 'Такая машина существует!')
                return render(request, 'Customer/pages/create_trade.html', {'context': form, 'user_authenticated': check_user(request)}) 
            TradeCar.objects.create(name=name, car_model=car_model, car_year=car_year, car_color=car_color,
                                    number_of_doors=number_of_doors, body_type=body_type, country=country,
                                    car_number=car_number, transmission=transmission, car_class=car_class, 
                                    type_fuel=type_fuel, type_drive=type_drive, car_image=car_image,
                                    customer=user)
            return redirect('main')
        else:
            messages.error(request, 'Неверный ввод данных')
    else:
        form = CarForm()
    return render(request, 'Customer/pages/create_trade.html', {'context': form, 'user_authenticated': check_user(request)})


@login_required
def get_user_history(request):
    user = Customer.objects.get(username=request.user)
    history = CustomerPurchaseHistory.objects.filter(customer=user, is_active=True).order_by('cost')
    paginator = Paginator(history, per_page=15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'Customer/pages/history.html', {'page_obj': page_object, 'user_authenticated': check_user(request)})


@login_required
def get_customer_trade_cars(request):
    user = Customer.objects.get(username=request.user)
    if request.method == "GET":
        trade_cars = TradeCar.objects.filter(customer=user).order_by('name')
        paginator = Paginator(trade_cars, per_page=10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        returns = ResultTrade.objects.all()
        return render(request, 'Customer/pages/customer_trade.html', {'page_obj': page_object, 'returns': returns, 
                                                                      'user_authenticated': check_user(request)})


@login_required
def get_cars_dealership(request):
    if request.method == "GET":
        dealership_cars = DealersSalesHistory.objects.filter(is_active=True, is_bought=False).annotate(new_price=F('id_dealer_car__price') * Value(Decimal('1.2'), output_field=MoneyField())).order_by('id_dealer_car__car__name')
        dealership_car_filter = DealershipCarsFilter(request.GET, queryset=dealership_cars)
        dealership_cars = dealership_car_filter.qs
        paginator = Paginator(dealership_cars, per_page=15)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'CarDealership/cars_to_offer.html', {'page_obj': page_object, 'dealership_filter': dealership_car_filter, 
                                                                    'is_customer': is_manager_customer(request), 
                                                                    'user_authenticated': check_user(request)})


@login_required
def booked_car(request, dealership_car_id):
    user = Customer.objects.get(username=request.user)
    car = DealersSalesHistory.objects.get(id=dealership_car_id)
    car.is_booked = True
    car.save()
    return redirect('dealership_cars')


@login_required
def get_all_customer_requests(request):
    user = Customer.objects.get(username=request.user)
    credits = Credit.objects.filter(customer=user)
    offers = CustomerPurchaseHistory.objects.filter(customer=user)
    return render(request, 'Customer/pages/requests.html', {'credits': credits, 'offers': offers, 'user_authenticated': check_user(request)})


@login_required
def get_car_trade(request, car_id):
    if request.method == "GET":
        car = TradeCar.objects.get(id=car_id)
        return render(request, 'Dealer/car_page.html', {'car': car, 'user_authenticated': check_user(request)})


@login_required
def history_director(request):
    dealer = Dealer.objects.all()
    cardealership = CarDealership.objects.all()
    customer = CustomerPurchaseHistory.objects.all()
    trade = ResultTrade.objects.all()
    credit = Credit.objects.all()
    car = Car.objects.all()
    dealer_car = DealerCars.objects.all()
    dealer_sales = DealersSalesHistory.objects.all()
    
    dealer_history = []
    cardealership_history = []
    customer_history = []
    trade_history = []
    credit_history = []
    car_history = []
    dealer_car_history = []
    dealer_sales_history = []
    for dealer_ in dealer:
        dealer_history.append(dealer_.history.all())
    for cardealership_ in cardealership:
        cardealership_history.append(cardealership_.history.all())
    for customer_ in customer:
        customer_history.append(customer_.history.all())
    for trade_ in trade:
        trade_history.append(trade_.history.all())
    for credit_ in credit:
        credit_history.append(credit_.history.all())
    for car_ in car:
        car_history.append(car_.history.all())
    for dealer_car_ in dealer_car:
        dealer_car_history.append(dealer_car_.history.all())
    for dealer_sales_ in dealer_sales:
        dealer_sales_history.append(dealer_sales_.history.all())
    
    history = [cardealership_history,
               dealer_history,
               customer_history,
               trade_history,
               credit_history,
               car_history,
               dealer_car_history,
               dealer_sales_history
    ]
    
    return render(request, 'Customer/pages/director.html', {'history': history, 'is_director': is_director(request)})


@login_required
def book_car_in_list(request, car_id):
    user = Customer.objects.get(username=request.user)
    car = DealersSalesHistory.objects.get(id=car_id)
    car.is_booked = True
    car.save()
    cost = car.id_dealer_car.price.amount * Decimal('1.2')
    CustomerPurchaseHistory.objects.create(customer=user, id_dealership_car=car, cost=cost, is_active=False)
    return redirect('customer_requests')


@login_required
def confirm_trade(request, request_id):
    res = ResultTrade.objects.get(id=request_id)
    res.is_active = True
    trade = TradeCar.objects.get(id=res.customer_car.pk)
    res.save()
    Car.objects.create(name=trade.name, car_model=trade.car_model, car_year=trade.car_year, car_color=trade.car_color,
                                number_of_doors=trade.number_of_doors, body_type=trade.body_type, country=trade.country,
                                car_number=trade.car_number, transmission=trade.transmission, car_class=trade.car_class, 
                                type_fuel=trade.type_fuel, type_drive=trade.type_drive, car_image=trade.car_image)
    return redirect('get_customer_trade')


@login_required
def deny_trade(request, request_id):
    res = ResultTrade.objects.delete(id=request_id)
    return redirect('get_customer_trade')
