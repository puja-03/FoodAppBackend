from django.db import models
from userapp.models import *

class Owner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

