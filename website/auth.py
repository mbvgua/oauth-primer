from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, logger

auth = Blueprint("auth", __name__)


# register route
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        # search for user in db
        user = User.query.filter_by(username=username).first()

        if user:
            message = "User already exists! Try again?"
            log_message = f"Failed creation of a new account with username: {username} and email: {email}, which are already in use by user of id: {user.id}"
            logger.warning(log_message)
            flash(message, category="danger")
        else:
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
            )
            message = (
                f"Congratulations {username}! You have successfully created an account."
            )
            log_message = f"{username} successfully created new user account of id:{new_user.id}"
            logger.info(log_message)
            flash(message, category="success")

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("views.dashboard"))

    return render_template("register.html", user=current_user)


# login route
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        # search for user in db
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                message = f"Congratulations {username}! You have successfully logged in to your account."
                log_message = f"{username} successfully logged into their account"
                logger.info(log_message)
                flash(message, category="success")
                login_user(user)
                return redirect(url_for("views.dashboard", user=current_user))
            else:
                message = "Oops! Looks like the passwords do no match. Try again?"
                log_message = f"{username} registered a failed login attempt due to incorrect password"
                logger.warning(log_message)
                flash(message, category="warning")
        else:
            message = "There is no user account with the above details. Register for a new account instead? "
            flash(message, category="warning")
            return redirect(url_for("auth.register"))
    return render_template("login.html")


# logout route
@auth.route("/logout")
@login_required
def logout():
    log_message = f"{current_user.username} has logged out of their account"
    logger.info(log_message)
    logout_user()
    return redirect(url_for("auth.login"))
