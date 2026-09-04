from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from .models import CarDataSet
from .serializer import Serializer

# Create your views here.

class Limit(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'

class CarViewSet(APIView):
    serializer_class = Serializer

    def get(self,request):
        car_dataset = CarDataSet.objects.all()
        manufacturer = request.query_params.get('manufacturer')
        if manufacturer:
            car_dataset = car_dataset.filter(manufacturer__icontains=manufacturer)
        paginator = Limit()
        paginated_cars = paginator.paginate_queryset(car_dataset, request, view=self)
        serializer = self.serializer_class(paginated_cars, many=True)
        return paginator.get_paginated_response(serializer.data)