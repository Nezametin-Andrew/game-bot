from rest_framework import serializers
from .models import UserProfile
from pay_sys.serializers import WalletSerializer


class UserProfileSerializer(serializers.ModelSerializer):

    account_balance = serializers.DecimalField(read_only=True, decimal_places=5, max_digits=7)
    ref_balance = serializers.DecimalField(read_only=True, decimal_places=5, max_digits=7)

    class Meta:
        model = UserProfile
        fields = ('id', 'id_tg', 'user_name', 'account_balance', 'ref_balance',)


class UserDetailSerializer(serializers.ModelSerializer):

    wallet = WalletSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'id_tg', 'user_name', 'account_balance', 'ref_balance', 'wallet',)
