from typing import ClassVar
from cryptography.hazmat.primitives import serialization

from config.constans import PASSPHRASE, FILENAME_PUBLIC_KEY_LOCATION, FILENAME_PRIVATE_KEY_LOCATION


class ImportKeysCryptography:
    """ Importa llaves RSA tanto privadas como publicas utilizando cryptography """

    _file_name: ClassVar[str]
    _PASSPHRASE: ClassVar[bytes] = PASSPHRASE.encode()
    _PUBLIC_KEY_FILE: ClassVar[bytes] = FILENAME_PUBLIC_KEY_LOCATION
    _PRIVATE_KEY_FILE: ClassVar[bytes] = FILENAME_PRIVATE_KEY_LOCATION

    @property
    def get_private_key(self):
        with open(self._PRIVATE_KEY_FILE, mode='rb') as key_file:
            return serialization.load_pem_private_key(
                key_file.read(),
                password=self._PASSPHRASE,
            )

    @property
    def get_public_key(self):
        with open(self._PUBLIC_KEY_FILE, mode='rb') as key_file:
            return serialization.load_pem_public_key(
                key_file.read(),
            )
