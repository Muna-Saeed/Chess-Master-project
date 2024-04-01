#!/usr/bin/python3
from flask import Blueprint, redirect, request, jsonify, render_template, session
from models import storage
from models.user import User
import re

routes = Blueprint('other_routes', __name__)
emails = storage.get_user_email();



@routes.errorhandler(405)
def method_not_allowed(e):
    return redirect('/')

@routes.route('/create')
def sigup():
    return render_template('signup.html')

@routes.route('/login')
def login():
    return render_template('login.html')


@routes.route('/check_new_user', methods=["POST"])
def check_new_user():
    username = request.form.get("username");
    first_name = request.form.get("first_name");
    last_name = request.form.get("last_name");
    email = request.form.get("email");
    pasw = request.form.get("password");
    if storage.auth(username) or storage.auth(email):
        return render_template("signup.html", message="username/email already exist")
    if not is_valid_username(username):
        return render_template('signup.html', username="invalid username!")
    if not is_valid_email(email):
        return render_template('signup.html', email="invalid email!")

    
    user = User()
    user.first_name, user.last_name = first_name, last_name
    user.username, user.email, user.pasw = username, email, pasw
    storage.new(user)
    storage.save()
    return render_template('login.html', welcome="Now you can login")

@routes.route('/auth', methods=["POST"])
def auth():
    username = request.form.get("username");
    pasw = request.form.get("pasw");
    obj = storage.auth(username);
    if obj and obj.pasw == pasw:
        online_users.append(obj)
        print(online_users)
        return render_template('index.html', user=obj)
    return render_template('login.html', message="incorrect password or username!")


@routes.route('/play/<id>')
def play(id):
    user = storage.get(User, id)
    if user:
        user.color = "black"
        return render_template('chess_board.html', user=user)
    return render_template('login.html')

@routes.route('/user', defaults={'user_id': None})
@routes.route('/user/<user_id>')
def profile(user_id):
    if user_id:
        user = storage.get(User, user_id)
        return render_template('user_profile.html', user=user)
    return render_template('login.html')



def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def is_valid_username(username):
    regex = r'^[a-zA-Z][a-zA-Z0-9]{2,19}$'
    return re.match(regex, username) is not None

def is_valid_password(password):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$'
    return re.match(regex, password) is not None


online_users = []

@routes.route('/getOnlineUsers')
def get_online():
    return jsonify({"online": [i.to_dict() for i in online_users]})


@routes.route('/logout/<user_id>')
def logout(user_id):
    for i in online_users:
        if i.id == user_id:
            online_user.remove(i)
            break
    return redirect('/')
