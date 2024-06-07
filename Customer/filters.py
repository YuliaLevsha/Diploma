from typing import Any
from django.contrib import admin
from django.contrib.auth.models import Group


class GroupFilter(admin.SimpleListFilter):
    title = "Groups"
    parameter_name = 'groups'
    
    def lookups(self, request, model_admin):
        return [(group.pk, group.name) for group in Group.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(groups__in=[self.value()])
        return queryset
