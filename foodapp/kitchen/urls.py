from django.urls import path, include
from kitchen.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'owner', OwnerViewSet)
router.register(r'kitchen', KitchenViewSet)

urlpatterns = [
    path('', include(router.urls))

]