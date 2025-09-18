import os
import json

from flask import Blueprint, flash, render_template, session, url_for, redirect, request
from flask_login import current_user, login_user
from oauthlib.oauth2 import WebApplicationClient
import requests
from dotenv import load_dotenv

from . import logger
from .models import User

load_dotenv()


oauth = Blueprint("oauth", __name__)

# implement google oauth config
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
client = WebApplicationClient(GOOGLE_CLIENT_ID)


@oauth.route("/login/google", methods=["GET", "POST"])
def login():
    """
    oauth implmented with google login
    """
    try:
        # get endpoint to hit for google login
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # construct request for goole login and provide scopes
        # which allow retrieve users profile from google
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)
    except Exception as e:
        message = f"Error occurred during oauth login: {str(e)}"
        logger.error(message)
        flash(message, category="danger")
        return redirect(url_for("views.home"))


@oauth.route("/login/google/callback", methods=["GET", "POST"])
def authorize_google():
    # get authorization code from google
    code = request.args.get("code")

    # get endpoint to hit for google auth tokens
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # prepare and send request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # having gotten the token, now let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # check if the users email account is verified as this
    # provides an additional layer of protection for your app
    # if so, you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        message = "User email not available or not verified by Google."
        logger.warning(message)
        flash(message, category="warning")
        return redirect(url_for("views.home"), 400)

    # create a user in your db with the info above
    # HACK: placeholder password before user updates it
    users_password = os.urandom(24)
    user = User(
        id_=unique_id,
        username=users_name,
        email=users_email,
        password=users_password,
        profile_pic=users_picture,
    )

    # check if user exists in db
    if not User.get_by_email(users_email):
        User.create(unique_id, users_name, users_email, users_password, users_picture)

    message = (
        f"Congratulations {users_name}! you have successfully logged in with google"
    )
    flash(message, category="success")
    log_message = (
        f"{users_name} of id: {unique_id} successfully logged in with their google"
    )
    logger.info(log_message)
    login_user(user)

    return redirect(url_for("views.dashboard", user=current_user))
