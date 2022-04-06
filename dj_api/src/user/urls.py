from django.shortcuts import redirect
from django.urls import path
from .views import *

urlpatterns = [
    path('', ListUserApiView.as_view()),
    path('<int:pk>/', DetailUserApiView.as_view()),
    path('create/', CreateProfileApiView.as_view()),
]
