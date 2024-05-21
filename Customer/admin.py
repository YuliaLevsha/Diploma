from django.contrib import admin
from Customer.models import *

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone")
    list_filter = ("is_active",)
    search_fields = ("username", "email")
    list_display_links = ("username",)
