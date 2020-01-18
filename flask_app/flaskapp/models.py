from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin
import random

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    survey_type = db.Column(db.Integer, nullable=False, default=random.randint(0,1))
    survey_token = db.Column(db.String(8), nullable=False, default=0)
    survey_cheat = db.Column(db.Boolean, nullable=False, default=False)
    survey_clicks = db.Column(db.Integer, nullable=False, default=0)
    #survey = db.relationship("Survey", backref="author", lazy=True)
    
    def __repr__(self): # It is a function that formats the output of the object
        return f"User('{self.username}', '{self.survey_type}', '{self.survey_token}', '{self.survey_cheat}', '{self.survey_clicks}')"

'''
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    survey_type = db.Column(db.Integer, nullable=False, default=0)
    survey_token = db.Column(db.Integer, nullable=False, default=0)
    survey_cheat = db.Column(db.Boolean, nullable=False, default=False)
    survey_clicks = db.Column(db.Integer, nullable=False, default=0)
    #user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __repr__(self): # It is a function that formats the output of the object
        return f"Survey({self.survey_type}', '{self.survey_token}', '{self.survey_cheat}', '{self.survey_clicks}')"
'''