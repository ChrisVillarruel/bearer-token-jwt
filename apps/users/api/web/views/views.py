from typing import Dict, Any, ClassVar

from django.db.transaction import atomic
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from apps.message_catalog.messages import MySuccessResponse, MyValidationError
from apps.users.api.web.serializers.serializers import SerializerLoginUser
from apps.users.exceptions import UserValidationException
from apps.users.models import User
from config.constans import FILENAME_PUBLIC_KEY_LOCATION
from config.backends.authentication.jwt_token import EncodeJWT
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
            succ = MySuccessResponse(0, data=jwt_code).success_response
            return Response(succ, status=status.HTTP_200_OK)


class APIUserInfo(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        user: User = User.objects.filter(id=request.user.get_user_id).values(
            "email",
            "username",
            "name",
            "last_name",
            "mother_last_name",
            "is_active",
            "is_new",
            "last_login",
            "state",
        ).first()
        return Response(user, status=status.HTTP_200_OK)
