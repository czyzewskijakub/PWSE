import os.path
import pathlib

import cachecontrol
import google.auth.transport
import requests
import google.auth.transport.requests

from flask import request, session
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from backend import settings
from ..jwt import user_manager


client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=settings.SCOPES,
    redirect_uri=settings.REDIRECT_URI
)


def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return authorization_url


def callback_from_google_login():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        return {"error": "Internal system error", "status_code": 500}
    credentials = flow.credentials
    request_session = requests.Session()
    cached_session = cachecontrol.CacheControl(sess=request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_request,
        audience=settings.GOOGLE_CLIENT_ID
    )
    res = user_manager.register_google_account(name=id_info["name"],
                                               email=id_info["email"],
                                               profile_picture_url=id_info["picture"])
    return res
