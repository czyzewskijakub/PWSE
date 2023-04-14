"""Application configuration file.
Every field should be correctly filled"""
import os.path
import pathlib

APP_NAME: str = "FlickTrendz Backend"
DEBUG: bool = True
TESTING: bool = False
SECRET_KEY: str = ""
ALGORITHM: str = ""
EXP_TIME_MIN: float = 0
SQLALCHEMY_DATABASE_URI: str = "sqlite://///" + os.path.join(pathlib.Path(__file__).parent.parent, "sqlite.db")
OAUTHLIB_INSECURE_TRANSPORT: str = "1"


GOOGLE_CLIENT_ID: str = ""
GOOGLE_CLIENT_SECRET: str = ""
GOOGLE_AUTH_URI: str = ""
GOOGLE_TOKEN_URI: str = ""
GOOGLE_USER_INFO_URI: str = "https://www.googleapis.com/oauth2/v1/userinfo"

REDIRECT_URI = ""

SCOPES = []
