from Dealer.models import *
from django import forms
from datetime import datetime
from base_model import Colors, BodyTypes, DriveTypes, G8Countries
from django_countries.fields import CountryField


class DealerForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    foundation_year = forms.IntegerField()
    
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
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all())
    car_year = forms.IntegerField()
    car_color = forms.ChoiceField(choices=Colors.choices)
    number_of_doors = forms.IntegerField()
    body_type = forms.ChoiceField(choices=BodyTypes.choices)
    country =  forms.ChoiceField(choices=G8Countries)
    type_drive = forms.ChoiceField(choices=DriveTypes.choices)
    volume_fuel_tank = forms.IntegerField()
    car_image = forms.ImageField()
    
    class Meta:
        model = Car
        fields = ('car_model', 'car_year', 'car_color', 'number_of_doors', 'body_type', 'country', 'type_drive', 'volume_fuel_tank', 'car_image')
    
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
    
    def clean_volume_fuel_tank(self):
        volume_fuel_tank = self.cleaned_data.get('volume_fuel_tank')
        if not (volume_fuel_tank >= 30 and volume_fuel_tank <= 100):
            raise forms.ValidationError('Неверный формат объема топливного бака. Должно быть от 30 до 100 л')
        return volume_fuel_tank


class DealerCarsForm(forms.Form):
    dealer = forms.ModelChoiceField(queryset=Dealer.objects.all())
    price = forms.DecimalField(max_digits=7, decimal_places=2)
    
    def clean_max_price(self):
        price = self.cleaned_data.get('price')
        if not price >= 0:
            raise forms.ValidationError('Отрицательная цена')
        return price
