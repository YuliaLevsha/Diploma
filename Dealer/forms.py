from Dealer.models import *
from django import forms
from datetime import datetime
from base_model import *


class DealerForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label='Название')
    foundation_year = forms.IntegerField(label='Год основания')
    
    class Meta:
        model = Dealer
        fields = ('name', 'foundation_year')
    
    def clean_foundation_year(self):
        foundation_year = self.cleaned_data.get('foundation_year')
        current_year = datetime.now().year
        if not (foundation_year >= 1900 and foundation_year <= current_year):
            raise forms.ValidationError('Неверный формат года. Должно быть от 1900 до ' + str(current_year))
        return foundation_year


class CarForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Полное наименование')
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all(), label='Марка')
    car_year = forms.IntegerField(label='Год создания')
    car_color = forms.ChoiceField(choices=Colors.choices, label='Цвет')
    number_of_doors = forms.IntegerField(label='Кол-во дверей')
    body_type = forms.ChoiceField(choices=BodyTypes.choices, label='Кузов')
    country =  forms.ChoiceField(choices=Countries.choices, label='Производитель')
    car_number = forms.CharField(max_length=20, label='Номер')
    transmission = forms.ChoiceField(choices=Transmission.choices, label='КПП')
    car_class = forms.ChoiceField(choices=ConfigurationType.choices, label='Комплектация')
    type_fuel = forms.ChoiceField(choices=FuelType.choices, label='Топливо')
    type_drive = forms.ChoiceField(choices=DriveTypes.choices, label='Привод')
    car_image = forms.ImageField(label='Фотография')
    
    class Meta:
        model = Car
        fields = ('name', 'car_model', 'car_year', 'car_color', 'number_of_doors', 'body_type', 'country', 
                  'car_number', 'transmission', 'car_class', 'type_fuel', 'type_drive', 'car_image')
    
    def clean_car_year(self):
        car_year = self.cleaned_data.get('car_year')
        current_year = datetime.now().year
        if not (car_year >= 1950 and car_year <= current_year):
            raise forms.ValidationError('Неверный формат года. Должно быть от 1950 до ' + str(current_year))
        return car_year
    
    def clean_number_of_doors(self):
        number_of_doors = self.cleaned_data.get('number_of_doors')
        if not (number_of_doors >= 2 and number_of_doors <= 5):
            raise forms.ValidationError('Неверный формат количества дверей. Должно быть от 2 до 5')
        return number_of_doors


class DealerCarsForm(forms.Form):
    dealer = forms.ModelChoiceField(queryset=Dealer.objects.all(), label='Поставщик')
    price = forms.DecimalField(max_digits=7, decimal_places=2, label='Цена')
    
    def clean_max_price(self):
        price = self.cleaned_data.get('price')
        if not price >= 0:
            raise forms.ValidationError('Отрицательная цена')
        return price
