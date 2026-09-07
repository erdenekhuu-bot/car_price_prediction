from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import CarDataSet
from .serializer import Serializer
from rest_framework.response import Response
from car_price.prepare_dataclean import Execute
import math
# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CarViewSet(APIView):
    serializer_class = Serializer

    def get(self, request):
        car_dataset = CarDataSet.objects.all()
        manufacturer = request.query_params.get('search')

        if manufacturer:
            car_dataset = car_dataset.filter(manufacturer__icontains=manufacturer)

        paginator = StandardResultsSetPagination()
        paginated_cars = paginator.paginate_queryset(car_dataset, request, view=self)
        serializer = self.serializer_class(paginated_cars, many=True)
        return paginator.get_paginated_response(serializer.data)


class CarFilter(APIView):
    serializer_class = Serializer

    def get(self, request):
        car_dataset = CarDataSet.objects.filter(manufacturer__icontains=request.query_params.get('search'))
        paginator = StandardResultsSetPagination()
        paginated_cars = paginator.paginate_queryset(car_dataset, request, view=self)
        serializer = self.serializer_class(paginated_cars, many=True)
        return paginator.get_paginated_response(serializer.data)


class PredictionView(APIView):
    serializer_class = Serializer

    def post(self, request):
        car_dataset = CarDataSet.objects.get(id=request.data.get('id'))
        serializer = self.serializer_class(car_dataset, data=request.data, partial=True)
        if serializer.is_valid():
            car_instance = serializer.save()
            app = Execute()
            predicted_price = math.ceil(float(app.predict(car_instance))*3600.39)

            return Response({
                "message": "Successfully predicted",
                "predicted_price": round(predicted_price, 2)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)