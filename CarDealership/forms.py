from CarDealership.models import *
from Dealer.models import CarModel
from django import forms
from datetime import datetime
from base_model import Colors, BodyTypes, DriveTypes, G8Countries
from django_countries.fields import CountryField


class DealershipForm(forms.Form):
    name = forms.CharField(max_length=255)
    location = forms.CharField(max_length=255)
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all())
