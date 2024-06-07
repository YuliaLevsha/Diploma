import django_filters
from Dealer.models import *
from base_model import Colors


class DealerCarsFilter(django_filters.FilterSet):
    car__car_model = django_filters.ModelChoiceFilter(field_name='car__car_model', queryset=CarModel.objects.all())
    car__car_year = django_filters.NumberFilter(field_name='car__car_year', lookup_expr='lte')
    car__car_color = django_filters.ChoiceFilter(field_name='car__car_color', choices=Colors.choices)
    car__body_type = django_filters.ChoiceFilter(field_name='car__car_body_type', choices=BodyTypes.choices)
    car__type_drive = django_filters.ChoiceFilter(field_name='car__car_type_drive', choices=DriveTypes.choices)
    car__transmission = django_filters.ChoiceFilter(field_name='car__transmission', choices=Transmission.choices)
    car__car_class = django_filters.ChoiceFilter(field_name='car__car_class', choices=ConfigurationType.choices)
    dealer = django_filters.ModelChoiceFilter(field_name='dealer', queryset=Dealer.objects.all())
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    
    class Meta:
        models = DealerCars
        fields = ('dealer', 'car__car_model', 'car__car_year', 'car__car_color', 'car__body_type', 'car__type_drive', 
                  'car__transmission', 'car__car_class')
