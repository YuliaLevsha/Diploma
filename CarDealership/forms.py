from CarDealership.models import *
from Dealer.models import CarModel
from django import forms
from datetime import datetime
from base_model import *
from Dealer.models import DealersSalesHistory


class DealershipForm(forms.Form):
    name = forms.CharField(max_length=255, label='Наименование')
    location = forms.CharField(max_length=255, label='Адрес')
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all(), label='Марка специализации')
    
    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = initial.get('name', '')
        self.fields['location'].initial = initial.get('location', '')
        self.fields['car_model'].initial = initial.get('car_model', None)


class ConfirmForm(forms.Form):
    type_payment = forms.ChoiceField(choices=Payment.choices, label='Способ оплаты')


class CarChooseForm(forms.Form):
    car_choose = forms.ModelChoiceField(queryset=DealersSalesHistory.objects.filter(is_active=True, is_booked=False, is_bought=False), label='Предложить')
