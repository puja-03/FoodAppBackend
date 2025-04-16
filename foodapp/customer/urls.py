
from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter



router = routers.DefaultRouter()

router.register('profile', CustomerViewSet)
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
# router.register(r'order-items', OrderItemViewSet, basename='order-item')
# router.register(r'Wishlist'), WishlistViewSet, basename='wishlist')


urlpatterns = [
    path('', include(router.urls)),
]