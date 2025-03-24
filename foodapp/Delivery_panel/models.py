from django.db import models
from userapp.models import *

# Create your models here.
class Delivery_boy(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=[('bike', 'Bike'), ('scooter', 'Scooter'), ('cycle', 'Cycle')])
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('busy', 'Busy'), ('inactive', 'Inactive')])
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
