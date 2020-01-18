from flask import render_template, url_for, flash, redirect, request, send_file
from flaskapp import app, db
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskapp.models import User
from flask_login import login_user, current_user, logout_user, login_required # Login_user immediately logs them in. Current_user checks who they are
from flaskapp.algorithms import AlgorithmSolutions
import json
import os

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:   # If user is already logged in
        return redirect(url_for("home")) 
    if form.validate_on_submit():
        user1 = User(username=form.username.data)
        print(User.query.all())
        db.session.add(user1)
        db.session.commit()
        flash(f"Dear {form.username.data}, your account has successfully been created account!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("home"))
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
                return redirect(url_for("home"))
        else:
            flash("Your login was unsuccessful. Please check your username", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account", methods=["GET", "POST"])
@login_required # Ensures that in order to access this page, you need to login
def account():
    form = UpdateAccountForm()
    print(User.query.all())

    if form.survey_token.data:
        sols = AlgorithmSolutions()
        current_user.username = current_user.username
        current_user.survey_token = form.survey_token.data
        current_user.survey_cheat = sols.is_cheating(current_user.survey_token)
        current_user.survey_clicks = sols.num_clicks(current_user.survey_token, current_user.survey_cheat)
        db.session.commit()
        flash("Updated!", "success")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.survey_token.data = current_user.survey_token
    return render_template("account.html", title="Account", form=form)

@app.route("/admin")
def admin():
    return render_template("admin.html", title="Admin")

@app.route("/download")
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
    with open(f"{directory}/flask_app/flaskapp/SurveyData.json", "w") as file:
        json.dump(user_hashtable, file)
    return send_file('SurveyData.json', attachment_filename='SurveyData.json', as_attachment=True, cache_timeout=0)
    
    return redirect(url_for("home"))