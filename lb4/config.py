from base64 import b64encode, b64decode
from os import environ, urandom

def _try_parse_int(value: str, default: int) -> int:
    try:
        return int(value)
    except ValueError:  # pragma: no cover
        return default


DB_CONNECTION_STRING = environ.get("DB_CONNECTION_STRING", "sqlite://:memory:")
BCRYPT_ROUNDS = environ.get("BCRYPT_ROUNDS", 12)

JWT_KEY = b64decode(environ.get("JWT_KEY", b64encode(urandom(32)).decode("utf8")))

AUTH_JWT_TTL = _try_parse_int(environ.get("AUTH_JWT_TTL", 86400), 86400)