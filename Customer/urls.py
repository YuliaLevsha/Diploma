from Customer.views import *
from django.urls import path, include


urlpatterns = [
    path('', main_page, name='main'),
    
    path('register/', register_view, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', reset, name='reset'),
    path('change-password/', change_password, name='change_password'),
    
    path('user-profile/', get_user, name='user_profile'),
    path('change-profile/', change_user_info, name='change_profile'),
    
    path('create-offer/', create_offer, name='create_offer'),
    path('create-credit/', create_credit, name='create_credit'),
    path('customer-trade/', create_trade_car, name='create_trade'),
    
    path('customer-history/', get_user_history, name='customer_history'),
    path('customer-trade-cars/', get_customer_trade_cars, name='customer_trade'),
    path('customer-requests/', get_all_customer_requests, name='customer_requests'),
    path('dealership-cars/', get_dealership_cars, name='dealership_cars'),
]