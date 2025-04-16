from django.db import models
from userapp.models import *
from django.core.exceptions import ValidationError
import os
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
    
class KitchenProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tag = models.CharField(max_length=50, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    preparation_time = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='kitchens/logos/',null=True, blank=True)
    cover_image = models.ImageField(upload_to='kitchens/covers/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Bank(models.Model):
    kitchen = models.OneToOneField(KitchenProfile, on_delete=models.PROTECT)
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
    kitchen = models.ForeignKey(KitchenProfile, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    Isavailable = models.BooleanField()
    prep_Time = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='kitchens/Images/', null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} ({self.kitchen.name})"

class MenuQuantity(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='quantities')
    quantity = models.IntegerField()
    price = models.IntegerField()
    quantity_type = models.CharField(max_length=200)

class Topping(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='topping_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    time = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.pk:
            old_topping = Topping.objects.filter(pk=self.pk).first()
            if old_topping and old_topping.image != self.image:
                if old_topping.image and os.path.isfile(old_topping.image.path):
                        os.remove(old_topping.image.path)
        super(Topping, self).save(*args, **kwargs)

class Thali(models.Model):
    kitchen = models.ForeignKey(KitchenProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    toppings = models.ManyToManyField(Topping)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    preparation_time = models.CharField(max_length=20)
    image = models.ImageField(upload_to='thalis/',null=True,blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title






