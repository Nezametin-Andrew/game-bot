import logging
from django.contrib.contenttypes.models import ContentType

from .base import BaseHandler


class PaymentHandler(BaseHandler):

    CT_MANAGER_PAYMENT = ContentType.objects.filter(model='payment')[0].model_class()._base_manager

    def __init__(self, method, payment_id=None):
        self.methods.update({
            'delete': self.delete_pay,
            'get_payments': self.get_payments,
        })
        super().__init__(method=method, payment_id=payment_id)

    def delete_pay(self):
        try:
            self.CT_MANAGER_PAYMENT.filter(pk=self.payment_id).delete()
        except Exception as exc:
            print(exc)

    def get_payments(self):
        try:
            return list(self.CT_MANAGER_PAYMENT.all())
        except Exception as exc:
            print(exc)
