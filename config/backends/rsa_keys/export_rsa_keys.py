from typing import ClassVar
from Crypto.PublicKey import RSA
from config.constans import (
    FILENAME_PRIVATE_KEY,
    PASSPHRASE,
    PROTECTION,
    BITS_RSA,
    FILENAME_PUBLIC_KEY
)


class ExportKeyRSAFile:
    """ Exporta las llaves privadas y publicas RSA a .pem """

    _SECRET_CODE: ClassVar[str] = PASSPHRASE
    _PKCS: ClassVar[int] = 8
    _PROTECTION: ClassVar[str] = PROTECTION
    _BITS_RSA: ClassVar[int] = int(BITS_RSA)

    def __init__(self):
        self.key = RSA.generate(self._BITS_RSA)
        self._export_private_key()
        self._export_public_key()

    def _export_private_key(self):
        _private_key = self.key.export_key(passphrase=self._SECRET_CODE, protection=self._PROTECTION)
        with open(FILENAME_PRIVATE_KEY, "wb") as file:
            file.write(_private_key)

    def _export_public_key(self):
        _public_key = self.key.public_key().export_key()
        with open(FILENAME_PUBLIC_KEY, "wb") as file:
            file.write(_public_key)
