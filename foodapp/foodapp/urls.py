from django.contrib import admin
from django.urls import path, include
from foodapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", home_page),
    path('api/kitchen/', include('kitchen.urls')),
    path('api/Delivery_panel/', include('Delivery_panel.urls')),
    path('api/user/', include('userapp.urls')),
    path('api/customer/', include('customer.urls')),
    path('razorpay/', include('customer.api.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
