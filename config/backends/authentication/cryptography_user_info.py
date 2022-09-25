import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from config.backends.rsa_keys.import_keys_cryptography import ImportKeysCryptography


class EncryptRSACryptography:
    """
        Encriptar información utilizando la llave publica del backend.
        Unicamente el backend podra saber el contenido encriptado
    """

    def __init__(self, data: str):
        self._rsa_keys = ImportKeysCryptography()
        self._data = data
        self.encrypt_data = self._to_base64(self._encrypt)

    @staticmethod
    def _to_base64(encrypt_data: bytes) -> str:
        return base64.b64encode(encrypt_data).decode()

    @property
    def _encrypt(self) -> bytes:
        return self._rsa_keys.get_public_key.encrypt(
            self._data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )


class DecryptRSACryptography:
    """
        Utilizando la llave privada, el backend puede decifrar el contido
    """

    def __init__(self, encrypt_message: str):
        self._rsa_keys = ImportKeysCryptography()
        self._encrypt_message = base64.b64decode(encrypt_message)
        self.decrypt_data = self._encrypt.decode()

    @property
    def _encrypt(self) -> bytes:
        return self._rsa_keys.get_private_key.decrypt(
            self._encrypt_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
