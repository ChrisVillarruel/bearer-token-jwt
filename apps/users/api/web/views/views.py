import random
import string
from typing import Dict, Any, ClassVar

from django.db.transaction import atomic
from django.core.cache import cache

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import GenericViewSet

from apps.message_catalog.messages import MySuccessResponse, MyValidationError
from apps.users.api.web.serializers.serializers import SerializerLoginUser, SerializerUpdateUserPassword, \
    SerializersForgotPassword
from apps.users.exceptions import UserValidationException
from apps.users.models import User
from config.backends.authentication.jwt_token import EncodeJWT
from config.backends.emails.messages import MailUserCodeVerifications
from config.backends.rsa_keys.import_keys_jwk import ImportKeysJWE

from jwcrypto.common import JWException


class RequestData:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def get_email(self) -> str:
        return self.data.get("email", None)

    @property
    def get_password(self) -> str:
        return self.data.get("password", None)

    @property
    def get_new_password(self) -> str:
        return self.data.get("new_password", None)

    @property
    def get_confirm_password(self) -> str:
        return self.data.get("confirm_password", None)

    @property
    def get_code(self) -> str:
        return self.data.get("code", None)


class LoginUser:
    _serializer_class: ClassVar[SerializerLoginUser] = SerializerLoginUser

    def __init__(self, request_data: RequestData):
        self._request_data = request_data
        self.user = self._serializer

    @property
    def _data(self) -> Dict[str, Any]:
        return {
            "email": self._request_data.get_email,
            "password": self._request_data.get_password,
        }

    @property
    def _serializer(self) -> User:
        serializer = self._serializer_class(data=self._data)
        serializer.is_valid(raise_exception=True)
        return serializer.create()


class APILoginUser(CreateAPIView):
    permission_classes = ()
    _request_data: ClassVar[RequestData] = RequestData
    _login_user: ClassVar[LoginUser] = LoginUser
    _jwt: ClassVar[EncodeJWT] = EncodeJWT
    _keys: ClassVar[ImportKeysJWE] = ImportKeysJWE

    def create(self, request, *args, **kwargs):
        try:
            request_data = self._request_data(request.data)
            with atomic():
                login_user = self._login_user(request_data)
                public_key = self._keys(is_public=True)
                jwt_code = self._jwt(login_user.user.hex_id, public_key).serialize_token
        except UserValidationException as e:
            err = MyValidationError(e.code_error).validation_error
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        except JWException as e:
            err = MyValidationError(4).validation_error
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = MyValidationError(500).validation_error
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            succ = MySuccessResponse(0, data={"access_token": jwt_code}).success_response
            return Response(succ, status=status.HTTP_201_CREATED)


class APIUserInfo(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get_info_user(id=request.user.get_user_id)
        return Response(user, status=status.HTTP_200_OK)


class UpdatePasswordUser:
    _serializer_class: ClassVar[SerializerUpdateUserPassword] = SerializerUpdateUserPassword

    def __init__(self, request_data: RequestData, user: User):
        self._request_data = request_data
        self._user = user
        self.update()

    @property
    def _context(self) -> dict[str, Any]:
        return {
            "user": self._user
        }

    @property
    def _data(self) -> dict[str, Any]:
        return {
            "password": self._request_data.get_password,
            "new_password": self._request_data.get_new_password,
        }

    def update(self):
        serializer = self._serializer_class(data=self._data, context=self._context)
        serializer.is_valid(raise_exception=True)
        serializer.update()


class APIUpdatePasswordUser(UpdateAPIView):
    """ Actualiza la contraseña del cliente """

    _request_data: ClassVar[RequestData] = RequestData
    _update_password: ClassVar[UpdatePasswordUser] = UpdatePasswordUser

    def update(self, request, *args, **kwargs):
        user: User = request.user
        try:
            request_user = self._request_data(request.data)
            with atomic():
                self._update_password(request_user, user)
        except UserValidationException as e:
            err = MyValidationError(e.code_error).validation_error
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = MyValidationError(500).validation_error
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            succ = MySuccessResponse(0).success_response
            return Response(succ, status=status.HTTP_200_OK)


class CreateCodeCache:
    """ Genera codigo cache para verificar la autenticidad el usuario """

    _TIME: ClassVar[int] = 300

    def __init__(self, request_data: RequestData):
        self._request_data = request_data
        self.user = self.get_user
        self.code = self._random_code_cache

    @property
    def get_user(self) -> User:
        try:
            return User.objects.get(email=self._request_data.get_email)
        except Exception as e:
            raise UserValidationException(2)

    @property
    def _random_code_cache(self) -> str:
        code = "".join(random.choices(string.ascii_uppercase, k=8))
        email = self.user.email
        cache.set(email, code, self._TIME)
        return cache.get(email)


class ForgotPassword:
    """ Actualiza la nueva contraseña del cliente """

    _serializer_class: ClassVar[SerializersForgotPassword] = SerializersForgotPassword

    def __init__(self, request_data: RequestData):
        self._request_data = request_data
        self._update()

    @property
    def _data(self) -> dict[str, Any]:
        return {
            "code": self._request_data.get_code,
            "email": self._request_data.get_email,
            "new_password": self._request_data.get_new_password,
            "confirm_password": self._request_data.get_confirm_password,
        }

    def _update(self):
        serializer = self._serializer_class(data=self._data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_user_instance(self._request_data.get_email)
        serializer.update_password(user)


class APIForgotPassword(GenericViewSet):
    """ API REST actualizar contraseña cliente si fue olvidada """

    permission_classes = ()
    _message_user: ClassVar[MailUserCodeVerifications] = MailUserCodeVerifications
    _create_code_cache: ClassVar[CreateCodeCache] = CreateCodeCache
    _request_data: ClassVar[RequestData] = RequestData
    _forgot_password: ClassVar[ForgotPassword] = ForgotPassword

    def create(self, request, *args, **kwargs):
        try:
            request_data = self._request_data(request.data)
            code_cache = self._create_code_cache(request_data)
            self._message_user(to=code_cache.user.email, name=code_cache.user.name, code=code_cache.code)
        except Exception as e:
            err = MyValidationError(500).validation_error
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            succ = MySuccessResponse(0).success_response
            return Response(succ, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            request_data = self._request_data(request.data)
            with atomic():
                self._forgot_password(request_data)
        except UserValidationException as e:
            err = MyValidationError(e.code_error).validation_error
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = MyValidationError(500).validation_error
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            succ = MySuccessResponse(0).success_response
            return Response(succ, status=status.HTTP_200_OK)
