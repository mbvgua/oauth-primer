# python standard libraries
import os
import logging

# third party libraries
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import sqlite3

# internal imports
from .db import init_db_command
from .models import User

load_dotenv()
logger = logging.getLogger(__name__)


def create_app():
    """
    create the main application
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # import & register various blueprints
    from .auth import auth
    from .oauth import oauth
    from .views import views

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(oauth, url_prefix="/oauth")
    app.register_blueprint(views, url_prefix="/")

    # implement flask_login functionality
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Oh no! You need to be logged in to access this page"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        """
        check if use exists in db.
        takes in user_id string and returns corresponding user object.
        else none is returned
        """
        return User.get(user_id)

    # implement logging
    # levels = debug(10),info(20),warning(30),error(40),critical(50)
    # disable werkzeug logging. Too much
    logging.getLogger("werkzeug").disabled = True
    logging.basicConfig(
        filename="oauth.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(module)s >>> %(message)s",
        datefmt="%B %d, %Y %H:%M:%S %Z",
    )

    return app


# create_database
# moved to the bottom since app wont run if its at the top
# also removed it from the function as app says to much recursion
try:
    init_db_command()
except sqlite3.OperationalError:
    print("An error occurred while creating the database!")
