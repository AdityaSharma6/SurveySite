from flask import render_template, url_for, flash, redirect, request, Blueprint, send_file
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import db
from flaskapp.models import User 
from flaskapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from flaskapp.algorithms import AlgorithmSolutions
import json
import os

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:   # If user is already logged in
        return redirect(url_for("main.home")) 
    if form.validate_on_submit():
        user1 = User(username=form.username.data)
        #print(User.query.all())
        db.session.add(user1)
        db.session.commit()
        flash(f"Dear {form.username.data}, your account has successfully been created account! Please login to continue.", "success")
        return redirect(url_for("main.home"))
    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if form.validate_on_submit():
        user1 = User.query.filter_by(username=form.username.data).first()
        if user1:
            login_user(user1, remember=form.remember.data)
            attempted_access = request.args.get("next") # passes in "/ATTEMPTED_ACCESS_PAGE_NAME"
            if attempted_access:
                flash("You have successfully logged in!", "success")
                return redirect(attempted_access)
            else:
                flash("You have successfully logged in!", "success")
                return redirect(url_for("main.home"))
        else:
            flash("Your login was unsuccessful. Please check your username", "danger")
    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
@login_required # Ensures that in order to access this page, you need to login
def account():
    form = UpdateAccountForm()
    #print(User.query.all())

    if form.survey_token.data:
        sols = AlgorithmSolutions()
        current_user.username = current_user.username
        current_user.survey_token = form.survey_token.data
        current_user.survey_cheat = sols.is_cheating(current_user.survey_token)
        current_user.survey_clicks = sols.num_clicks(current_user.survey_token, current_user.survey_cheat)
        db.session.commit()
        flash("Updated!", "success")
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        form.survey_token.data = current_user.survey_token
    return render_template("account.html", title="Account", form=form)

@users.route("/download")
def download():
    user_list = User.query.all()
    user_hashtable = {}
    for i in range(len(user_list)):
        user_node = user_list[i]
        user_hashtable[user_node.username] = {"Survey Type": user_node.survey_type,
                                              "Survey Token": user_node.survey_token,
                                              "Survey Cheat": user_node.survey_cheat,
                                              "Survey Clicks": user_node.survey_clicks
                                              }
    directory = os.getcwd()
    print(directory)
    with open(f"{directory}/flaskapp/SurveyData.json", "w") as file:
        json.dump(user_hashtable, file)
    return send_file('SurveyData.json', attachment_filename='SurveyData.json', as_attachment=True, cache_timeout=0)
    
    return redirect(url_for("main.home"))
