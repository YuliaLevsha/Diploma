from django.contrib import admin
from Customer.models import *
from Customer.filters import GroupFilter


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone")
    list_filter = ("is_active", GroupFilter)
    search_fields = ("username", "email", "phone")
    list_display_links = ("username",)


@admin.register(CustomerPurchaseHistory)
class CustomerPurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ("customer", "id_dealership_car", "cost")
    list_filter = (
        "customer__username",
        "id_dealership_car__id_dealer_car__car__car_model__name"
    )
    search_fields = ("customer__username", "id_dealership_car")
    list_display_links = None
