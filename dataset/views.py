from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CarDataSet
from .serializer import Serializer

# Create your views here.

class CarViewSet(APIView):
    serializer_class = Serializer

    def get(self,request):
        car_dataset = CarDataSet.objects.all()
        serializer = Serializer(car_dataset, many=True)
        return Response(serializer.data)