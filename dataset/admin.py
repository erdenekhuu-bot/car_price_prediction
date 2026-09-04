from django.contrib import admin
from dataset.models import CarDataSet


# Register your models here.

@admin.register(CarDataSet)
class CarAdminView(admin.ModelAdmin):
    list_display = ('id','price', 'leavy', 'manufacturer','model','prod_year','category','engine_volume','gear_bo_type')
    search_fields = ('leavy', 'price','manufacturer')