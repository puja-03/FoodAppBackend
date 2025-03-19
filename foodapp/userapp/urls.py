
from django.contrib import admin
from django.urls import path, include
from .auth_view import *
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('register/<str:role>/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),

    path('adminview/', AdminView.as_view(), name='adminview'),
    path('ownerview/', OwnerView.as_view(), name='ownerview'),
]
