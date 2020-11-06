from NZA_app import app, db, ma, login_manager

from datetime import datetime

import uuid

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(75), nullable = False)
    case_num = db.Column(db.String(18), nullable = False)
    phone_num = db.Column(db.String(14), nullable = False)
    address = db.Column(db.String(30), nullable = False)
    legal_dep = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(60), nullable = False)

    def __init__(self,name,case_num,phone_num,address,legal_dep, id=id)
        self.name = name
        self.case_num = case_num
        self.phone_num = phone_num
        self.address = address
        self.legal_dep = legal_dep

    def __repr__(self):
        return f'Client(s) profile initiated.'

class ClientSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'case_num', 'phone_num', 'address', 'legal_dep']

client_schema = ClientSchema()
clients_schema = ClientSchema(many = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(75), nullable = False)
    email = db.Column(db.String(60))
    password = db.Column(db.String(50), nullable = False)
    token = db.Column(db.String(300))
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    token_refresh = db.Column(db.Boolean, default = False)
    date_update = db.Column(db.DateTime)

    def __init__(self,name,email,password, id = id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'{self.name} is now available to edit.'