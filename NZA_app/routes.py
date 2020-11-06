from NZA_app import app, db
from NZA_app.models import Client, client_schema, clients_schema, User, check_password_hash
from flask import jsonify, request, render_template, redirect, url_for

from flask_login import login_required, login_user, current_user, logout_user

import jwt

from NZA_app.forms import UserForm, LoginForm
#from NZA_app.token_verification import token_required


@app.route('/')
def index():
    return render_template('index.html')

@app.route('users/register', methods = ['GET', 'POST'])
#Endpoint for Creating Case Notes!!
@app.route('/clients/create', methods = ['POST'])
#@token_required
def create_patient(#current_user_token)
    name =

    client = 

