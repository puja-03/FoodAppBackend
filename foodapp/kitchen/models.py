from django.db import models
from userapp.models import *
from django.core.exceptions import ValidationError

def validate_account_number(value):
    """Ensures the account number contains only digits."""
    if not value.isdigit():
        raise ValidationError("Account number must contain only digits.")

class Owner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.business_name} - {self.user.username}"

class Kitchen(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='kitchens/logos/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='kitchens/covers/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return f"{self.name} ({self.owner.business_name})"
    
class Bank(models.Model):
    kitchen = models.OneToOneField(Kitchen, on_delete=models.PROTECT)
    bank_name = models.CharField(max_length=255)
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True, validators=[validate_account_number])
    ifsc_code = models.CharField(max_length=20)
    upi_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Bank Details of {self.kitchen.name}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Menu(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    Isavailable = models.BooleanField()
    prep_Time = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='kitchens/Images/', null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} ({self.kitchen.name})"

class MenuQuantity(models.Model):
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    quantity_type = models.CharField(max_length=200)









