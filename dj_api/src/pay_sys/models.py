from django.db import models
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):

    user = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, related_name='wallet')
    address = models.CharField(_('Address'), max_length=255)
    private_key = models.CharField(_('Private key'), max_length=255)
    public_key = models.CharField(_('Public key'), max_length=255)
    wif = models.CharField('WIF', max_length=255)


class Payment(models.Model):

    user = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, verbose_name=_('User'), related_name='payment', unique=True)
    total_sum = models.DecimalField(_('Total sum'), max_digits=7, decimal_places=5)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)



# # Server models
#
# class PayOutRequest(models.Model):
#     ...
#
#
# class HistoryTranslateCheckMoney(models.Model):
#     ...
#
#
# class HistoryTranslateGameMoney(models.Model):
#     ...
#
