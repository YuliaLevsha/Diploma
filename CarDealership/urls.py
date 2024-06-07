from CarDealership.views import *
from django.urls import path, include


urlpatterns = [
    path('add-dealership/', add_dealership, name='create_dealership'),
    path('edit-dealership/<dealership>/', update_dealership, name='edit_dealership'),
    path('get-dealerships/', get_dealerships, name='get_dealerships'),
    
    path('get-dealership-cars/', get_delaership_cars, name='get_dealership_cars'),
    path('get-dealership-history/', dealership_history, name='get_dealership_history'),
    
    path('confirm-offer/', confirm_buy_by_customer, name='confirm_offer'),
    path('confirm-offer/<request_id>/', checked, name='confirm_by_dealership'),
    path('deny-offer/<request_id>/', deny, name='deny_by_dealership'),
    
    path('confirm-credit/', confirm_credit, name='confirm_credit'),
    path('confirm-credit/<request_id>/', checked_credit, name='checked_credit'),
    path('deny-credit/<request_id>/', deny_credit, name='deny_credit'),
    path('dealership-requests/', get_cardealership_requests, name='dealership_requests'),
    
    path('confirm-trade/', confirm_trade_dealership, name='confirm_trade'),
    path('confirm-trade/<request_id>/', confirm_trade, name='checked_trade'),
    path('deny-trade/<request_id>/', deny_trade, name='deny_trade'),
]