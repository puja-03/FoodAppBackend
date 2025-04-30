from django.urls import path
from .api_razorpay import RazorpayOrderView, TransactionAPIView

urlpatterns = [     
    path('order/', RazorpayOrderView.as_view(), name='razorpay_order'),
    path('verify_payment/', TransactionAPIView.as_view(), name='verify_payment'),
]