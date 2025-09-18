from flask import Blueprint, render_template, session, url_for, redirect
from flask_login import login_user
from . import app_oauth, logger, db
from .models import User
from dotenv import load_dotenv
import os

load_dotenv()

oauth = Blueprint("oauth", __name__)

# implement google oauth config
google_oauth = app_oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_uri="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email"},
)

# @oauth.route("/register",methods=["GET","POST"])
# def register():
#     pass


@oauth.route("/login/google", methods=["GET", "POST"])
def login():
    """
    oauth implmented with google login
    """
    try:
        redirect_uri = url_for("oauth.authorize_google", _external=True)
        return google_oauth.authorize_redirect(redirect_uri)
    except Exception as e:
        logger.error(f"Error occurred during login: {str(e)}")
        return "Error occurred during login", 500


@oauth.route("/authorize/google", methods=["GET", "POST"])
def authorize_google():
    token = google_oauth.authorize_access_token()
    userinfo_endpoint = google_oauth.server_metadata["userinfo_endpoint"]
    resp = google_oauth.get(userinfo_endpoint)
    user_info = resp.json()
    email = user_info["email"]

    user = User.query.filter_by(email=email).first()
    # if user does not exist in db
    if not user:
        new_user = User(email=email)
        db.session.add(new_user)
        db.session.commit()

        session["oauth_token"] = token
        login_user(new_user)

    return redirect(url_for("views.dashboard"))
