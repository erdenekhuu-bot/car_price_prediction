from rest_framework import serializers
from .models import CarDataSet

class Serializer(serializers.ModelSerializer):
     class Meta:
            model = CarDataSet
            fields = '__all__'