#!/usr/bin/python3
from flask import Blueprint, redirect, request, jsonify, render_template, session
from models import storage
from models.user import User
from models.game import Game
import re
import os
from PIL import Image


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





@routes.route('/play/<id>')
def play(id):
    user = storage.get(User, id)
    print(user)
    if user:
        user.color = "black"
        game = Game()
        game.first_move = {str(1 * 8 + i):False for i in range(8)}
        game.player1_id = user.id
        storage.new(game)
        return render_template('chess_board.html', user=user, game=game)
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



@routes.route('/upload', methods=['POST'])
def upload():
    user_id = session.get("player_id")
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'message': 'File upload Failed'})
    if 'profile_picture' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['profile_picture']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    filename, file_extension = os.path.splitext(file.filename)
    filename = '/static/images/profile/' + user_id + file_extension
    user.img = filename
    storage.save()

    absolute_filename = '/home/ubuntu/Chess-Master-project/game' + filename

    img = Image.open(file)

    new_width = 150
    new_height = 150

    resized_img = img.resize((new_width, new_height))

    resized_img.save(absolute_filename)

    return jsonify({'message': 'File uploaded successfully'})



if __name__ == '__main__':
    app.run(debug=True)
