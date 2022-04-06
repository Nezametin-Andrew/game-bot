from django.shortcuts import redirect
from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path('<int:user_id>/', PaymentApiView.as_view()),
    path('all/', PaymentApiView.as_view()),
    path('create/', CreatePaymentApiView.as_view()),
    path('delete/<int:pk>/', DeletePaymentApiView.as_view()),
]
