from django.urls import path, include


urlpatterns = [
    path('user/', include('user.urls')),
    #path('game/', include('game.urls')),
    path('payment-system/', include('pay_sys.urls')),
]
