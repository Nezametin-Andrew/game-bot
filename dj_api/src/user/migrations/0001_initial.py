# Generated by Django 3.2.11 on 2022-04-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_tg', models.BigIntegerField(unique=True, verbose_name='Telegram ID')),
                ('user_name', models.CharField(max_length=255, verbose_name='Full name')),
                ('account_balance', models.DecimalField(decimal_places=5, default=0, max_digits=7, verbose_name='Account balance')),
                ('ref_balance', models.DecimalField(decimal_places=5, default=0, max_digits=7, verbose_name='Partner balance')),
            ],
            options={
                'verbose_name': 'Users',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
