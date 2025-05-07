from django.db import models
from userapp.models import *
from kitchen.models import *
import os
from decimal import Decimal

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

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thali = models.ForeignKey(Thali, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'thali')
    
    def get_total_price(self):
        """Calculate total price including thali and toppings"""
        base_price = self.thali.price * self.quantity
        
        topping_price = sum(topping.price for topping in self.thali.toppings.all())
        total_topping_price = topping_price * self.quantity
        
        return Decimal(base_price + total_topping_price)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.thali.title} x {self.quantity}"
    

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    )
    
    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    payment_status = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thali = models.ManyToManyField(Thali)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist"
    
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    thali = models.ForeignKey(Thali, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.thali.title} x {self.quantity}"
    
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255,verbose_name="Payment ID")
    order_id = models.CharField(max_length=255,verbose_name="Order ID")
    signature = models.CharField(max_length=255, null=True, blank=True,verbose_name="Signature")
    amount = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Amount")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username}"
    