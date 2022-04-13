import logging
from celery import shared_task

from user.models import UserProfile
from .models import Payment, Wallet
from services.blocksyper_api import BlockCypherAPI


logger = logging.getLogger(__name__)


class PaymentWorker:

    def __init__(self):
        self.payments = self.get_payments()

    def get_payments(self):
        try:
            return list(Payment.objects.filter().values('pk', 'wallet__address', 'created_at', 'total_sum', 'user'))
        except Exception as exc:
            logging.debug(str(exc))
            return []

    def get_user_balance(self, user_id):
        return UserProfile.objects.get(pk=user_id).account_balance

    def balance_is_from_wallet(self, address):
        return BlockCypherAPI(method='get_balance', address=address).process()

    def check_transactions(self):
        pos_balance = [pay for pay in self.payments if self.balance_is_from_wallet(pay['wallet_address']).get('balance')]
        if pos_balance:
            ...

    @classmethod
    def process(cls):
        cls.check_transactions(self=PaymentWorker())

