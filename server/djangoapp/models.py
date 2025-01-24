from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class CarModel(models.Model):
    TYPES = [
        ('SUV', 'SUV'),
        ('SEDAN', 'Sedan'),
        ('WAGON', 'Wagon'),
    ]
    
    dealer_id = models.IntegerField(null=True)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10, choices=TYPES, default='Sedan')
    year = models.IntegerField(default=2025, validators=[MinValueValidator(2015), MaxValueValidator(2025)])
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    