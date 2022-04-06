import logging
import blockcypher

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.forms import model_to_dict
from services.base import BaseHandler

logger = logging.getLogger(__name__)


class BlockCypher(BaseHandler):
    """
    The BaseClass to work with the `blockcypher` module.

    In particular, if a `method=` argument is passed then:

    .process() - Available.
    """

    BASE_URL = getattr(settings, "BASE_URL_SERV", None)
    TOKEN = getattr(settings, 'BLOCKCYPHER_TOKEN', None)
    DEFAULT_COIN_SYMBOL = 'ltc'
    ERROR_RESP = 'Connection aborted'
    MAIN_ADDRESS_WALLET = getattr(settings, 'ADMIN_WALLET', None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.methods.update({
            'create_wallet': self._create_wallet,
            'detail_address': self._get_details_address,
            'get_balance': self._get_balance_for_address,
            'clean_balance': self.__clean_balance
        })

    def _create_wallet(self) -> dict:
        """
        Creating new wallet.
        :returns address, private_key, public_key, wif
        """
        try:
            return blockcypher.generate_new_address(coin_symbol=self.DEFAULT_COIN_SYMBOL, api_key=self.TOKEN)
        except Exception as exc:
            logger.debug(str(exc))

    def _get_details_address(self) -> dict:
        """
        Getting details for address.
        :returns tx, unconfirmed_tx, balance, unconfirmed_balance
        """
        self.__check_address()
        try:
            return blockcypher.get_address_details(
                address=self.address, coin_symbol=self.DEFAULT_COIN_SYMBOL, api_key=self.TOKEN
            )
        except Exception as exc:
            logger.debug(str(exc))
            return {'error': self.ERROR_RESP}

    def _get_balance_for_address(self) -> dict:
        """
        Getting balance for address.
        :returns balance, unconfirmed_balance.
        """
        detail = self._get_details_address()
        if 'error' not in detail:
            return {'balance': detail['balance'], 'unconfirmed_balance': detail['unconfirmed_balance']}
        return detail

    def __clean_balance(self) -> dict:
        """
        Cleans balance and sent coins to admin address.
        """
        self.__check_address()
        self.__check_private_key()
        try:
            return blockcypher.simple_spend(
                coin_symbol=self.DEFAULT_COIN_SYMBOL, from_privkey=self.private_key,
                to_address=self.MAIN_ADDRESS_WALLET, to_satoshis=-1, api_key=self.TOKEN
            )
        except Exception as exc:
            logger.debug(str(exc))
            return {'error': self.ERROR_RESP}

    @staticmethod
    def is_valid_address_data(address: dict) -> dict:
        """ Validate wallet data """
        for key in ['address', 'private', 'public', 'wif']:
            if key not in address:
                raise InvalidAddressError(f'Invalid address {str(address)}')
        return address

    def __check_private_key(self) -> bool:
        """ Check attribute `private_key` """
        if 'private_key' not in self.__dict__ or self.private_key is None:
            raise AttributePrivateKeyError('Private key for address not found')
        return True

    def __check_address(self) -> bool:
        """ Check attribute `address` """
        if 'address' not in self.__dict__ or self.address is None:
            raise AttributeAddressError('Address for wallet not found')
        return True


class BlockCypherAPI(BlockCypher):
    """
    In particular, if a `address=` argument is passed then:

    method=detail_address - Available.
    method=get_balance - Available.

    In particular, if a `private_key=` argument is passed then:

    method=clean_balance - Available.
    """

    CT_MANAGER_WALLET = ContentType.objects.filter(model='wallet')[0].model_class()._base_manager

    def __init__(self, method: str, address: str = None, private_key: str = None):
        super(BlockCypherAPI, self).__init__(method=method, address=address, private_key=private_key)

    @classmethod
    def create_model(cls, us_instance, wallet: dict) -> dict:
        """ Add data in to model `Wallet` """
        return model_to_dict(cls.CT_MANAGER_WALLET.create(
            address=wallet['address'], private_key=wallet['private'],
            public_key=wallet['public'], wif=wallet['wif'],
            user=us_instance
        ))


class BaseAttributeError(Exception): ...


class AttributeAddressError(BaseAttributeError): ...


class AttributePrivateKeyError(BaseAttributeError): ...


class InvalidAddressError(BaseAttributeError): ...
