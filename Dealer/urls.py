from Dealer.views import *
from django.urls import path, include


urlpatterns = [
    path('add-dealer/', add_dealer, name='add_dealer'),
    path('edit-dealer/<dealer>/', update_dealer, name='edit_dealer'),
    
    path('add-car/', add_car, name='add_car'),
    path('cars/<car_id>/', get_car, name='get_car'),
    path('tradecar/<car_id>/', get_tradecar, name='get_tradecar'),
    path('edit-car/<car_id>/', update_car, name='edit_car'),
    
    path('dealer-cars/', get_delaer_cars, name='dealer_cars'),
    path('dealer-history/', dealer_history, name='dealer_history'),
    
    path('dealer-confirm/', confirm_buy_by_dealership, name='dealer_confirm'),
    path('confirm/<request_id>/', checked, name='confirm_by_dealer'),
    path('deny/<request_id>/', deny, name='deny_by_dealer'),
    
    path('dealers/', get_dealers, name='get_dealers'),
]
