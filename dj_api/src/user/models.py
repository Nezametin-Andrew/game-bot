from django.db import models


class UserProfile(models.Model):

    id_tg = models.BigIntegerField('Telegram ID', unique=True)
    user_name = models.CharField('Full name', max_length=255)
    account_balance = models.DecimalField('Account balance', max_digits=7, decimal_places=5, default=0)
    ref_balance = models.DecimalField('Partner balance', max_digits=7, decimal_places=5, default=0)

    def __str__(self):
        return f"{self.user_name} : {self.id_tg}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = "Users"
