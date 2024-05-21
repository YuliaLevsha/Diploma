from CarDealership.views import *
from django.urls import path, include


urlpatterns = [
    path('add-dealership/', add_dealership, name='create_dealership'),
    path('get-dealership-cars/', get_cars, name='get_dealership_cars'),
]