from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "d3cba391bec5644c8e406c7ba7d989b6"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
login_manager = LoginManager(app) # Handles login sessions. Makes it super easy
login_manager.login_view = "login" # It is the name of the login function


from flaskapp import routes