from rest_framework.serializers import ModelSerializer
from .models import Wallet, Payment


class WalletSerializer(ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('address',)


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
