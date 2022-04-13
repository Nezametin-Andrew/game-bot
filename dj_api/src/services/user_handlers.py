import logging
from django.contrib.contenttypes.models import ContentType
from .base import BaseHandler
from .blockcypher_api import BlockCypherAPI
from user.serializers import UserDetailSerializer
from .blockcypher_api import InvalidAddressError


logger = logging.getLogger(__name__)


class CreatingUserHandler(BaseHandler):
    """
    The class for creating model `UserProfile`, creating model `Wallet`
    and add instance user profile in model `Wallet`.

    Available methods:

    `method=create`
    """

    LIST_VALID_FIELD = ['id_tg', 'user_name']
    CT_MANAGER_USER = ContentType.objects.filter(model='userprofile')[0].model_class()._base_manager
    ERROR_MSG = {

    }

    def __init__(self, method, serializer=None, data=None, user_id=None):
        super().__init__(method=method, serializer=serializer, input=data, user_id=None, data=None)
        self.methods.update({
            'create': self._create,
            'get_balance': ...,
            'update_balance': ...,

        })

    def _create(self) -> UserDetailSerializer:
        """ Creating user and wallet """

        # Creating user and add in to model `UserProfile`
        try:
            self.__create_user()
        except InvalidFieldError as exc:
            return self.returns_error(msg=exc, logger=logger, data=f' data: {str(self.input)}')
        except ExistsUserProfileError as exc:
            return self.returns_error(msg=exc, logger=logger)
        except AssertionError as exc:
            return self.returns_error(msg=exc, logger=logger)

        # Creating wallet
        try:
            self.__create_wallet()
        except CreateWalletError as exc:
            return self.returns_error(msg=exc, logger=logger)
        except InvalidFieldError as exc:
            return self.returns_error(msg=exc, logger=logger)
        except Exception as exc:
            return self.returns_error(msg=exc, logger=logger)

        # Add wallet in to model `Wallet`
        try:
            self.__create_model_wallet()
        except Exception or AssertionError or CreateWalletError as exc:
            user = self.CT_MANAGER_USER.filter(pk=self.data['id'])
            if user:
                self.CT_MANAGER_USER.filter(pk=self.data['id']).delete()
            return self.returns_error(msg=exc, logger=logger)

        return UserDetailSerializer(
            instance=self.CT_MANAGER_USER.filter(pk=self.data['id'])[0]
        )

    def __create_user(self) -> None:
        """ Validate data and creating user """
        serialize_data = self.serializer(data=self.input)
        serialize_data.is_valid()
        self.is_valid_field(data=self.input)
        self.is_exists_user(id_tg=self.input['id_tg'], obj=self)
        serialize_data.save()
        self.data = serialize_data.data

    def __create_wallet(self) -> None:
        """ Creating and validate data for `wallet` """
        wallet = BlockCypherAPI(method='create_wallet').process()
        if not isinstance(wallet, dict):
            raise CreateWalletError('Remote end closed connection without response')
        self.wallet = BlockCypherAPI.is_valid_address_data(wallet)

    def __create_model_wallet(self) -> None:
        """ Add wallet in to model `Wallet` """
        wallet = BlockCypherAPI.create_model(
            us_instance=self.CT_MANAGER_USER.get(pk=self.data['id']),
            wallet=self.wallet
        )
        if not isinstance(wallet, dict):
            raise CreateWalletError('Error creating model `Wallet`')

    @classmethod
    def is_valid_field(cls, data: dict) -> None:
        """ Validating correct fields for model `UserProfile` """

        # Check exists data
        if not data:
            raise InvalidFieldError('Invalid field')

        # Check fields in data
        for field in data:
            if field not in cls.LIST_VALID_FIELD:
                raise InvalidFieldError('Invalid field')

        # Check exists field in data
        for field in cls.LIST_VALID_FIELD:
            if field not in data:
                raise InvalidFieldError('Invalid field')

        cls.is_valid_id_tg(data['id_tg'])
        cls.is_valid_user_name(data['user_name'])

    def get_balance(self):
        ...

    @classmethod
    def is_exists_user(cls, id_tg: int, obj) -> None:
        """ Check user if exists """
        users = obj.CT_MANAGER_USER.filter(id_tg=id_tg)
        if users:
            raise ExistsUserProfileError('User already exists')

    @classmethod
    def is_valid_id_tg(cls, id_tg: int) -> None:
        """ Validating field `id_tg` """
        for ch in str(id_tg):
            if not ch.isdigit():
                raise InvalidFieldError('Invalid field')

    @classmethod
    def is_valid_user_name(cls, user_name: str) -> None:
        """ Check length field `user_name` """
        if len(str(user_name)) < 1:
            raise InvalidFieldError('Invalid field')


class InvalidFieldError(Exception):
    ...


class ExistsUserProfileError(Exception):
    ...


class CreateWalletError(Exception):
    ...