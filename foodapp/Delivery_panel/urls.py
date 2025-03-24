from django.urls import path, include
from Delivery_panel.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'delivery_boy', Delivery_boyViewSet)

urlpatterns = [
    path('', include(router.urls))
]