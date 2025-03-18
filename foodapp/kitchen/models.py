from django.db import models

class Owner(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

# class Kitchen(models.Model):
#     owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=10)
#     logo = models.ImageField(upload_to='kitchens/logos/', null=True, blank=True)
#     cover_image = models.ImageField(upload_to='kitchens/covers/', null=True, blank=True)
#     status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])
