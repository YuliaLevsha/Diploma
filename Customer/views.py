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
from Dealer.models import CarModel, DealersSalesHistory


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


def check_user(request):
    return True if request.user.is_authenticated else False


def is_manager_buy(request):
    try:
        user = Customer.objects.get(username=request.user)
    except(Customer.DoesNotExist):
        user = None
    if user is not None:
        manager_buy_group = Group.objects.get_or_create(name='Manger_buy')
        return True if manager_buy_group in user.groups.all() else False
    return False


def is_manager_customer(request):
    try:
        user = Customer.objects.get(username=request.user)
    except(Customer.DoesNotExist):
        user = None
    if user is not None:
        manager_buy_group = Group.objects.get(name='Manager_customer')
        return True if manager_buy_group in user.groups.all() else False
    return False


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
    return render(request, 'Customer/pages/main.html', {'user_authenticated': check_user(request), 'is_buy': is_manager_buy(request),
                                                        'is_customer': is_manager_customer(request)})


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
    return render(request, 'Customer/forgot_password.html', {'context': form})


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
            volume_fuel_tank = form.cleaned_data['volume_fuel_tank']
            json_data = {
                'car_model': car_model.pk,
                'car_year': car_year,
                'car_color': None,
                'number_of_doors': 2,
                'body_type': body_type,
                'type_drive': type_drive,
                'country': None,
                'volume_fuel_tank': volume_fuel_tank
            }
            offer = Offer.objects.create(max_price=max_price,
                                         customer=user,
                                         interested_in_car=json_data)
            return redirect('main')
        messages.error(request, 'Неверный ввод данных')
    form = OfferForm()
    return render(request, 'Customer/create_offer.html', {'context': form, 'user_authenticated': check_user(request)})


@login_required
def create_credit(request):
    user = Customer.objects.get(username=request.user)
    if request.method == 'POST':
        form = CreateCreditForm(request.POST)
        if form.is_valid():
            sum_credit = form.cleaned_data['sum_credit']
            period_time = form.cleaned_data['period_time']
            
            Credit.objects.create(sum_credit=sum_credit, customer=user, period_time=period_time)
        messages.error(request, 'Неверный ввод данных')
    form = CreateCreditForm()
    return render(request, 'Customer/create_credit.html', {'context': form, 'user_authenticated': check_user(request)})


@login_required
def create_trade_car(request):
    if request.method == 'POST':
        user = Customer.objects.get(username=request.user)
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car_model_name = form.cleaned_data['car_model']
            car_model = CarModel.objects.get(name=car_model_name)
            car_year = form.cleaned_data['car_year']
            car_color = form.cleaned_data['car_color']
            number_of_doors = form.cleaned_data['number_of_doors']
            body_type = form.cleaned_data['body_type']
            country = form.cleaned_data['country']
            type_drive = form.cleaned_data['type_drive']
            volume_fuel_tank = form.cleaned_data['volume_fuel_tank']
            car_image = form.cleaned_data['car_image']
            
            TradeCar.objects.create(car_model=car_model, car_year=car_year, car_color=car_color,
                                    number_of_doors=number_of_doors, body_type=body_type, country=country,
                                    type_drive=type_drive, volume_fuel_tank=volume_fuel_tank, car_image=car_image,
                                    customer=user)
        else:
            messages.error(request, 'Неверный ввод данных')
    else:
        form = CarForm()
    return render(request, 'Customer/create_trade.html', {'context': form, 'user_authenticated': check_user(request)})


@login_required
def get_user_history(request):
    user = Customer.objects.get(username=request.user)
    history = CustomerPurchaseHistory.objects.filter(customer=user)
    return render(request, 'Customer/history.html', {'context': history, 'user_authenticated': check_user(request)})


@login_required
def get_customer_trade_cars(request):
    user = Customer.objects.get(username=request.user)
    trade_cars = TradeCar.objects.filter(customer=user)
    return render(request, 'Customer/customer_trade.html', {'context': trade_cars, 'user_authenticated': check_user(request)})


@login_required
def get_dealership_cars(request):
    user = Customer.objects.get(username=request.user)
    dealership_cars = DealersSalesHistory.objects.filter(is_booked=False, is_bought=False, is_active=True)
    return render(request, 'Customer/delaership_cars.html', {'context': dealership_cars, 'user_authenticated': check_user(request)})


@login_required
def get_all_customer_requests(request):
    ...
