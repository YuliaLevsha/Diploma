from django.contrib import admin
from CarDealership.models import *


@admin.register(CarDealership)
class CarDealershipAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
