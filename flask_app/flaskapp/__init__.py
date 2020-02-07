from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskapp.config import Config


db = SQLAlchemy()
login_manager = LoginManager() # Handles login sessions. Makes it super easy
login_manager.login_view = "users.login" # It is the name of the login function



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from flaskapp.users.routes import users
    from flaskapp.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(main)

    return app

