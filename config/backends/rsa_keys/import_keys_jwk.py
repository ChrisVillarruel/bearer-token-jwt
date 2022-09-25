from abc import ABC, abstractmethod
from typing import NoReturn
from jwcrypto.jwk import JWK

from config.constans import FILENAME_PUBLIC_KEY_LOCATION, FILENAME_PRIVATE_KEY_LOCATION, PASSPHRASE


class ImportKeys(ABC):
    @abstractmethod
    def _get_key(self, password: str = None) -> NoReturn:
        ...


class ImportKeysJWE(ImportKeys):
    """ Importar llaves RSA tanto privadas como publicas utilizando la librearia JWK """

    def __init__(self, is_public: bool):
        if is_public:
            self._file_name = FILENAME_PUBLIC_KEY_LOCATION
            self.key = self._get_key()
        else:
            self._file_name = FILENAME_PRIVATE_KEY_LOCATION
            self.key = self._get_key(password=PASSPHRASE.encode())

    def _get_key(self, password: bytes | None = None) -> JWK:
        with open(self._file_name, mode='rb') as f:
            return JWK.from_pem(f.read(), password=password)
