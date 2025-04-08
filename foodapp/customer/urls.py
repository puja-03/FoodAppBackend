
from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter



router = routers.DefaultRouter()

router.register('profile', CustomerViewSet)
router.register(r'thalis', ThaliViewSet, basename='thali')
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]