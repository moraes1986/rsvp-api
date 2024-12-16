import os
from datetime import timedelta

MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_RUN_PORT = os.getenv("FLASK_RUN_PORT")
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES")))

#Internal APIs

GUEST_API_URL = os.getenv("GUEST_API_URL")
USER_API_URL = os.getenv("USER_API_URL")

LOCALHOST_URL = os.getenv("LOCALHOST_URL")

