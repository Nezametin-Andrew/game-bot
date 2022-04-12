from django.shortcuts import redirect
from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path('', PaymentListApiView.as_view()),
    path('<int:pk>/', PaymentRetrieveDestroyApiView.as_view()),
    path('tg/<int:user_id', PaymentTelegramApiView.as_view()),
]
