import datetime as dt
import json
import uuid

from jwcrypto import jwt
from typing import ClassVar, Dict, Any

from config.constans import DEFAULT_EXPIRATION_MINUTES, ENC, ALG
from config.backends.rsa_keys.import_keys_jwk import ImportKeysJWE


class EncodeJWT:
    _alg: ClassVar[str] = ALG
    _enc: ClassVar[str] = ENC
    _DEFAULT_EXPIRATION_MINUTES: ClassVar[int] = DEFAULT_EXPIRATION_MINUTES

    def __init__(self, uuid_code_user: uuid.uuid4, pub_key: ImportKeysJWE):
        self._code = str(uuid_code_user)
        self._key = pub_key.key

    @staticmethod
    def _unix_time(date_time: dt.datetime):
        return dt.datetime.timestamp(date_time)

    @property
    def _header(self) -> Dict[str, Any]:
        return {
            "alg": self._alg,
            "enc": self._enc
        }

    @property
    def _payload(self) -> Dict[str, Any]:
        return {
            "iss": self._code,
            "exp": self._unix_time(dt.datetime.now() + dt.timedelta(minutes=self._DEFAULT_EXPIRATION_MINUTES)),
            "iat": self._unix_time(dt.datetime.now())
        }

    @property
    def _create_encryp_jwt(self) -> jwt.JWT:
        token = jwt.JWT(header=self._header, claims=self._payload)
        token.make_encrypted_token(self._key)
        return token

    @property
    def serialize_token(self) -> str:
        return self._create_encryp_jwt.serialize(compact=True)


class DecodeJWT:
    def __init__(self, jwt_token: str, private_key: ImportKeysJWE):
        self._jwt = jwt_token
        self._private_key = private_key.key

    @property
    def _dencryp_jwt(self) -> jwt.JWT:
        return jwt.JWT(key=self._private_key, jwt=self._jwt, expected_type="JWE")

    @property
    def payload(self) -> Dict[str, Any]:
        return json.loads(self._dencryp_jwt.claims)
