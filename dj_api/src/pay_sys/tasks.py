import logging
from celery import shared_task

from .models import Payment, Wallet
from services.blocksyper_api import BlockCypherAPI


logger = logging.getLogger(__name__)


class PaymentWorker:

    def __init__(self):
        self.payments = self.get_payments()

    def get_payments(self):
        try:
            return list(Payment.objects.filter().values('pk', 'created_at', 'total_sum', 'user'))
        except Exception as exc:
            logging.debug(str(exc))
            return []

    def get_wallet_address(self, user_id):
        try:
            return Wallet.objects.get(user=user_id).address
        except Exception as exc:
            logger.debug(str(exc))
            return None

    def balance_is_from_wallet(self, address):
        return BlockCypherAPI(method='get_balance', address=address).process()

    def check_transactions(self):
        ...

    @classmethod
    def process(cls, obj):
        cls.check_transactions(self=PaymentWorker())

