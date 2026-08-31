from django.db import models

# Create your models here.
class CarDataSet(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.FloatField()
    leavy=models.CharField(max_length=6)
    manufacturer=models.CharField(max_length=25)
    model=models.CharField(max_length=30)
    prod_year=models.CharField(max_length=4)
    category=models.CharField(max_length=20)
    leather_interior=models.BooleanField()
    fuel_type=models.CharField(max_length=20)
    engine_volume=models.CharField(max_length=20)
    mileage=models.CharField(max_length=20)
    cylinders=models.CharField(max_length=5)
    gear_bo_type=models.CharField(max_length=20)
    drive_wheel=models.CharField(max_length=20)
    door=models.CharField(max_length=20)
    wheel=models.CharField(max_length=20)
    color=models.CharField(max_length=20)
    airbag=models.CharField(max_length=20)

    def __str__(self):
        return self.model

    def __getitem__(self, item):
        return self.__dict__[item]