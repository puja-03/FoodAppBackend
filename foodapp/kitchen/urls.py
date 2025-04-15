from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from kitchen.views import OwnerViewSet, KitchenProfileViewSet, BankViewSet, MenuViewSet, ToppingViewSet, CategoryViewSet,ThaliViewSet

router = routers.DefaultRouter()
router.register(r'owner', OwnerViewSet)
router.register(r'kitchenprofile', KitchenProfileViewSet, basename='kitchen')
router.register(r'bank', BankViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'topping', ToppingViewSet, basename='topping')
router.register(r'category', CategoryViewSet)
router.register(r'thalis', ThaliViewSet, basename='thali')

# router.register(r'menuquantity', MenuQuantityViewSet)

urlpatterns = [
    path('', include(router.urls))
]