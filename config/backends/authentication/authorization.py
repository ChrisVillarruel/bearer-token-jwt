import datetime as dt

from typing import ClassVar
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic
from jwcrypto.common import JWException

from rest_framework import authentication, exceptions

from apps.message_catalog.messages import MyValidationError
from apps.users.models import User
from config.backends.authentication.jwt_token import DecodeJWT
from config.backends.exceptions.base_exceptions import BaseAthorizationException
from config.backends.rsa_keys.import_keys_jwk import ImportKeysJWE
from config.settings import LIST_SERVICES_WITHOUT_AUTHENTICATING


class JWTAuthentication(authentication.BaseAuthentication):
    _DECODE_JWT: ClassVar[DecodeJWT] = DecodeJWT
    _IMPORT_KEY: ClassVar[ImportKeysJWE] = ImportKeysJWE
    _authentication_header_prefix: ClassVar[str] = 'Bearer'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self._authentication_header_prefix.lower()

        if request.headers.get("TypeService") in LIST_SERVICES_WITHOUT_AUTHENTICATING:
            return None
        elif not auth_header:
            err = MyValidationError(5).validation_error
            raise exceptions.AuthenticationFailed(err)
        elif len(auth_header) <= 1:
            err = MyValidationError(6).validation_error
            raise exceptions.AuthenticationFailed(err)
        elif len(auth_header) > 2:
            err = MyValidationError(7).validation_error
            raise exceptions.AuthenticationFailed(err)
        else:
            prefix = auth_header[0].decode('utf-8')
            token = auth_header[1].decode('utf-8')

            if prefix.lower() != auth_header_prefix:
                err = MyValidationError(8).validation_error
                raise exceptions.AuthenticationFailed(err)
            return self._authenticate_credentials(token)

    def _authenticate_credentials(self, token: str):
        try:
            private_key = self._IMPORT_KEY(is_public=False)
            decode_token = self._DECODE_JWT(token, private_key)
            payload = decode_token.payload

            with atomic():
                user: User = User.objects.get(hex_id=payload.get("iss"))
                user.last_login = dt.datetime.now()
                if not user.state:
                    user.is_active = False
                    raise BaseAthorizationException(9)
                if not user.is_active:
                    user.is_active = False
                    raise BaseAthorizationException(10)
                user.save()

        except ObjectDoesNotExist:
            err = MyValidationError(11).validation_error
            raise exceptions.AuthenticationFailed(err)
        except JWException as _:
            err = MyValidationError(12).validation_error
            raise exceptions.AuthenticationFailed(err)
        except BaseAthorizationException as e:
            err = MyValidationError(e.code_error).validation_error
            raise exceptions.AuthenticationFailed(err)
        except Exception as _:
            err = MyValidationError(12).validation_error
            raise exceptions.AuthenticationFailed(err)
        return user, token
