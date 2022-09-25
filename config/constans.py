import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY_AES: bytes = b"P0l1m3nt3s#Fr0nt3ndXYZ.20210101_"
IV_AES: bytes = b"P0l1m3nt3sB4ckXX"

# -- Configuración JWT
DEFAULT_EXPIRATION_MINUTES = 90
ALG = 'RSA-OAEP-256'
ENC = 'A256CBC-HS512'

# -- Configuración en la generación de claves RSA
PASSPHRASE = config("PASSPHRASE")
PROTECTION = config("PROTECTION")
BITS_RSA = config("BITS_RSA")
FILENAME_PRIVATE_KEY = config("FILENAME_PRIVATE_KEY")
FILENAME_PUBLIC_KEY = config("FILENAME_PUBLIC_KEY")
FILENAME_PRIVATE_KEY_LOCATION = config("FILENAME_PRIVATE_KEY_LOCATION")
FILENAME_PUBLIC_KEY_LOCATION = config("FILENAME_PUBLIC_KEY_LOCATION")
