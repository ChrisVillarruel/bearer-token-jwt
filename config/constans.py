import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# -- Configuración del montor de envio de correos
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")