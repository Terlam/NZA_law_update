from NZA_app import app, db, ma, login_manager

from datetime import datetime

import uuid

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

# Creation of the Casenote Model
# The Casenote model will have an 
# id, title, content, date_created
# user_id
class Casenote(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.String(200), db.ForeignKey('user.id'), nullable = False)

    def __init__(self,title,content,user_id):
        self.title = title
        self.content=content
        self.user_id = user_id

    def __repr__(self):
        return f'The title of the Case Note is {self.title} \n and the content is {self.content}'

# removed the client model - T

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.String(200), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(150))
    password = db.Column(db.String(256), nullable = False)
    token = db.Column(db.String(400))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    token_refreshed = db.Column(db.Boolean, default = False)
    date_refreshed = db.Column(db.DateTime)

    def __init__(self,name,email,password,id = id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = self.set_pasword(password)

    def set_pasword(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'{self.name} has been created successfully! Date: {self.date_created}'