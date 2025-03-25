from django.db import models
from userapp.models import *
from kitchen.models import *
import os

# Create your models here.
# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    profile_image = models.ImageField(upload_to='customer-profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_image = Customer.objects.filter(pk=self.pk).first()
            if old_image and old_image.profile_image != self.profile_image:
                if old_image.profile_image and os.path.isfile(old_image.profile_image.path):
                    os.remove(old_image.profile_image.path)
        super(Customer, self).save(*args, **kwargs)
    
# Customer Order Model
class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name="orders")
    # delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ])
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')])

    def __str__(self):
        return f"Order {self.id} - {self.customer.user.username}"

# Order itemn Model
class OrderItem(models.Model):
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name="order_items")
    # food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.food_item.name} in Order {self.order.id}"

