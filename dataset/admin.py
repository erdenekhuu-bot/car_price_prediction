from django.contrib import admin
from dataset.models import CarDataSet


# Register your models here.

@admin.register(CarDataSet)
class CarAdminView(admin.ModelAdmin):
    list_display = ('price', 'leavy', 'manufacturer')
    search_fields = ('leavy', 'price')