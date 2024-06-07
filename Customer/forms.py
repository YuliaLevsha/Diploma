import re
from typing import Any
from django import forms
from Customer.models import *
from django.contrib.auth.forms import UserCreationForm
from base_model import *
from Dealer.models import CarModel
from datetime import datetime


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Почта')
    password1 = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердить пароль', strip=False, widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ('username', 'email')
        labels = {
            'username': 'Псевдоним'
        }


class ForgotForm(forms.Form):
    email = forms.EmailField(required=True, label='Почта')


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label='Старый пароль')
    new_password = forms.CharField(widget=forms.PasswordInput(), label='Новый пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение нового пароля')
    
    def clean_new_password(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        if new_password == old_password:
            raise forms.ValidationError(
                'Новый пароль является старым паролем',
                code='password_equal',
            )
        return new_password
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        new_password = self.cleaned_data.get('new_password')
        if new_password != confirm_password:
            raise forms.ValidationError(
                'Новый пароль и пароль подтверждения не совпадают',
                code='password_mismatch',
            )
        return confirm_password


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label='Старый пароль')
    new_password = forms.CharField(widget=forms.PasswordInput(), label='Новый пароль')
    
    def clean_new_password(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        if new_password == old_password:
            raise forms.ValidationError(
                'Новый пароль и старый совпадают',
                code='password_mismatch',
            )
        return new_password 


class ChangeCustomerForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Почта')
    date_birth = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}), label='Дата рождения')
    passport = forms.CharField(max_length=10, label='Паспорт')
    phone = forms.CharField(max_length=15, label='Телефон')
    class Meta:
        model = Customer
        fields = ('username', 'first_name', 'last_name')
        labels = {
            'username': 'Псевдоним',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.compile(r'^\+\d{12}$').match(phone):
            raise forms.ValidationError('Неверный формат телефона')
        return phone
    
    def clean_passport(self):
        passport = self.cleaned_data.get('passport')
        if not re.compile(r'^[A-Z]{2}\d{7}$').match(passport):
            raise forms.ValidationError('Неверный формат номера паспорта')
        return passport


class OfferForm(forms.Form):
    max_price = forms.DecimalField(max_digits=7, decimal_places=2, label='Мах стоимость')
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all(), label='Марка')
    car_year = forms.IntegerField(label='Год создания')
    body_type = forms.ChoiceField(choices=BodyTypes.choices, label='Кузов')
    type_drive = forms.ChoiceField(choices=DriveTypes.choices, label='Привод')
    transmission = forms.ChoiceField(choices=Transmission.choices, label='КПП')
    car_class = forms.ChoiceField(choices=ConfigurationType.choices, label='Комплектация')
    type_fuel = forms.ChoiceField(choices=FuelType.choices, label='Топливо')
    
    def clean_car_year(self):
        car_year = self.cleaned_data.get('car_year')
        current_year = datetime.now().year
        if not (car_year >= 1950 and car_year <= current_year):
            raise forms.ValidationError('Неверный формат года. Должно быть от 1950 до ' + str(current_year))
        return car_year
    
    def clean_max_price(self):
        max_price = self.cleaned_data.get('max_price')
        if not max_price >= 0:
            raise forms.ValidationError('Отрицательная цена')
        return max_price


class CreateCreditForm(forms.Form):
    sum_credit = forms.DecimalField(max_digits=7, decimal_places=2, label='Сумма')
    period_time = forms.ChoiceField(choices=PeriodCredit.choices, label='Период')
    
    def clean_sum_credit(self):
        sum_credit = self.cleaned_data.get('sum_credit')
        if not sum_credit >= 0:
            raise forms.ValidationError('Отрицательная сумма')
        return sum_credit
