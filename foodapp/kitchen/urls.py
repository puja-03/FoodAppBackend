from django.urls import path, include
from kitchen.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'owner', OwnerViewSet)
router.register(r'kitchen', KitchenViewSet)
router.register(r'bank', BankViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'menuquantity', MenuQuantityViewSet)

urlpatterns = [
    path('', include(router.urls))
]