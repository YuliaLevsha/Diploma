import django_filters
from Dealer.models import *
from base_model import Colors
from CarDealership.models import CarDealership


class DealershipCarsFilter(django_filters.FilterSet):
    id_dealer_car__car__car_model = django_filters.ModelChoiceFilter(field_name='id_dealer_car__car__car_model', queryset=CarModel.objects.all())
    id_dealer_car__car__car_year = django_filters.NumberFilter(field_name='id_dealer_car__car__car_year', lookup_expr='lte')
    id_dealer_car__car__car_color = django_filters.ChoiceFilter(field_name='id_dealer_car__car__car_color', choices=Colors.choices)
    id_dealer_car__car__body_type = django_filters.ChoiceFilter(field_name='id_dealer_car__car__body_type', choices=BodyTypes.choices)
    id_dealer_car__car__type_drive = django_filters.ChoiceFilter(field_name='id_dealer_car__car__type_drive', choices=DriveTypes.choices)
    id_dealer_car__car__transmission = django_filters.ChoiceFilter(field_name='id_dealer_car__car__transmission', choices=Transmission.choices)
    id_dealer_car__car__car_class = django_filters.ChoiceFilter(field_name='id_dealer_car__car__car_class', choices=ConfigurationType.choices)
    car_dealership = django_filters.ModelChoiceFilter(field_name='car_dealership', queryset=CarDealership.objects.all())
    
    class Meta:
        models = DealersSalesHistory
        fields = ('car_dealership', 'id_dealer_car__car__car_model', 'id_dealer_car__car__car_year', 'id_dealer_car__car__car_color', 
                  'id_dealer_car__car__body_type', 'id_dealer_car__car__type_drive', 'id_dealer_car__car__transmission', 
                  'id_dealer_car__car__car_class')
