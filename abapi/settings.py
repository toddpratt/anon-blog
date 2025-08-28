import json
import os

CREDENTIALS_FILE = os.environ.get("CREDENTIALS_FILE", "/run/secrets/creds.json")

with open(CREDENTIALS_FILE, "r") as f:
    _creds = json.load(f)


# checks environment, then _creds, then a default
def get_cred(key: str, default: str = None):
    return os.getenv(key, _creds.get(key, default))


SECRET_KEY = get_cred('SECRET_KEY')
CORS_DOMAIN = get_cred('CORS_DOMAIN', '*')
RECAPTCHA_SECRET = get_cred('RECAPTCHA_SECRET')
SQLALCHEMY_DATABASE_URI = get_cred('SQLALCHEMY_DATABASE_URI')


if not SQLALCHEMY_DATABASE_URI or not SECRET_KEY:
    raise ValueError("SQLALCHEMY_DATABASE_URI or SECRET_KEY environment variable not set")
