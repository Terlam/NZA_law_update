from NZA_app import app, db
from NZA_app.models import Client, client_schema, clients_schema, User, check_password_hash
from flask import jsonify, request, render_template, redirect, url_for

from flask_login import login_required, login_user, current_user, logout_user

import jwt

from NZA_app.forms import UserForm, LoginForm
#from NZA_app.token_verification import token_required


@app.route('/')
def home():
    return render_template('home.html')

@app.route('users/register', methods = ['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User(name,email,password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', user_form = form)

@app.route('/users/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data

    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password, password):
        login_user(logged_user)
        return redirect(url_for('get_key'))
    return render_template('login.html', login_form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/users/getkey', methods = ['GET'])
def get_key():
    token = jwt.encode({'public_id': current_user.id, 'email':current_user.email},app.config['SECRET_KEY'])
    user = User.query.filter_by(email = current_user.email).first()
    user.token = token

    db.session.add(user)
    db.session.commit()
    results = token.decode('utf-8')
    return render_template('token.html', token = results)

# Get a new API Key
@app.route('/users/updatekey', methods = ['GET', 'POST', 'PUT'])
def refresh_key():
    refresh_key = {'refreshToken': jwt.encode({'public_id':current_user.id, 'email': current_user.email}, app.config['SECRET_KEY'])}
    temp = refresh_key.get('refreshToken')
    new_token = temp.decode('utf-8')

    # Adding Refreshed Token to DB
    user = User.query.filter_by(email = current_user.email).first()
    user.token = new_token

    db.session.add(user)
    db.session.commit()

    return render_template('token_refresh.html', new_token = new_token)

#Endpoint for Creating Case Notes!!
@app.route('/notes', methods = ['GET', 'POST'])
@login_required
def notes():
    form = PostForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        post = Post(title,content,user_id)

        db.session.add(post)

        db.session.commit()
        return redirect(url_for('home'))
    return render_template('notes.html', post_form = form)

# post detail route to display info about a post
@app.route('/notes/<int:post_id>')
@login_required
def note_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('note_detail.html', post = post)

@app.route('/notes/update/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def note_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id

        # Update the database with the new Info
        post.title = title
        post.content = content
        post.user_id = user_id

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('note_update.html', update_form = form)

@app.route('/notes/delete/<int:post_id>',methods = ['GET','POST', 'DELETE'])
@login_required  
def note_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

