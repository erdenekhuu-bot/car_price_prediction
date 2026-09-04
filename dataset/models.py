from django.db import models

# Create your models here.
class CarDataSet(models.Model):
    id=models.AutoField(primary_key=True)
    price=models.CharField()
    leavy=models.CharField()
    manufacturer=models.CharField()
    model=models.CharField()
    prod_year=models.CharField()
    category=models.CharField()
    leather_interior=models.CharField()
    fuel_type=models.CharField()
    engine_volume=models.CharField()
    mileage=models.CharField()
    cylinders=models.CharField()
    gear_bo_type=models.CharField()
    drive_wheel=models.CharField()
    door=models.CharField()
    wheel=models.CharField()
    color=models.CharField()
    airbag=models.CharField()

    def __str__(self):
        return self.model

    def __getitem__(self, item):
        return self.__dict__[item]