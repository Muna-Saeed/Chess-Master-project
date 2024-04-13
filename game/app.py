# Chess Master project using Flask for the backend
from flask import Flask, render_template, request, jsonify, session, redirect
from game.more_routes.user import routes
from models.game import Game
from models.user import User
from models import storage
from game.more_routes.api import api_route
from flask_socketio import SocketIO, send, emit, join_room, leave_room


app = Flask(__name__)
app.register_blueprint(routes)
app.register_blueprint(api_route)
app.config['SECRET_KEY'] = 'Chess@game%%%@90'
socketio = SocketIO(app)


online_users = []
rooms = {}
rooms['main'] = {"members":0, "messages":[]}
    

games = []

@app.route('/')
def index():
    user_id = session.get('user_id')
    return render_template('index.html')

@app.route('/sitemap')
def sitemap():
    """ this route for sitemap which is for google search requirement"""
    return render_template('sitemap.xml')

@app.route('/play')
def play():
    """ this route handles play request when the user not loged in """
    return render_template('login.html')


@app.route('/settings')
def settings():
    """ this route will handle game settings """
    return render_template('settings.html')

@app.route('/history')
def game_history():
    return render_template('game_history.html')


@socketio.on("connect")
def connect(auth):
    """ 
    socket connet:
    when user is online this function add the user to room
    and sends message to teh front end to detec that new user is online
    """
    room = session.get("main")
    name = session.get("name")
    player_id = session.get("player_id")
    if room:
        join_room(room)
        rooms[room]['members'] += 1
        send({"name":name, "message": 'connected', 'player_id':player_id}, to=room)
        print("joined ******************************** ", name, room)
    else:
        print(" not joined **************")

@socketio.on("disconnect")
def disconnect():
    """ this function handles the user offline """
    name = session.get("name")
    player_id = session.get("player_id")
    user = storage.get(User, player_id)

    if user and user in online_users:
        online_users.remove(user)

    room = session.get("main")
    if room:
        leave_room(room)
    print("leaved **************", name, room)


@socketio.on('message')
def handle_message(data):
    """ this function handles to detect some
        messages from socket emit 
    """
    player_id = session.get("player_id")
    name = session.get("name")

    if data["message"] == "board":
        room = session.get("gameId")
        send({'message':"board", 'start':data['start'], 'end':data['end'], 'game':data['game'], 'player_id':player_id}, to=room)
        return 
    room = session.get("main")
    send({"name":name, "message": data['message'], 'player_id':player_id, 'from_id':data['from_id']}, to=room)


@app.route('/auth', methods=["POST", "GET"])
def auth():
    """ 
    * this function is handles user login 
    * it checks if the passwornd matchs the username or email
    """
    if request.method == "POST":
        session.clear()
        username = request.form.get("username");
        pasw = request.form.get("pasw");
        obj = storage.auth(username);
        if obj and obj.pasw == pasw:
            if obj not in online_users: online_users.append(obj)
            session['name'] = obj.username
            session['player_id'] = obj.id
            session['main'] = "main"
            return render_template('play.html', user=obj, players=online_users)
    elif session.get("player_id"):
        obj = storage.get(User, session.get("player_id"))
        if obj:
            if obj not in online_users: online_users.append(obj)
            session['main'] = "main"
            return render_template('play.html', user=obj, players=online_users)
    return render_template('login.html', message="incorrect password or username!")



@socketio.on('invite')
def handle_invite(data):
    """ this function handles the game invitation request """
    player_id = session.get("player_id")
    name = session.get("name")
    #check if data['messge'] is invite to handle
    if data["message"] == "invite":
        # create new game object
        game = Game()
        session["gameId"]  = game.id
        player1 = storage.get(User, data["from_id"])
        player1.color="white"
        game.white = player1
        rooms[game.id] = {"members":0, "messages":[]}
        game.first_move = {str(1 * 8 + i):False for i in range(8)}
        for i in range(48, 56):
            game.first_move[str(i)] = False
        #both to players should join new room private room
        join_room(game.id)
        room = "main"
        name = session.get("name")
        storage.new(game)
        socketio.emit("invite", {'room':game.id, 'name':name, "message": data['message'], 'player_id':player_id, 'from_id':data['from_id']}, to=room)
    else:
        print("invalid invatation")

@socketio.on('accept')
def accept(data):
    """ This function handles when the suer accept the invitation """
    # since the game already created the player 2 gets the game object using game Id
    game = storage.get(Game, data['room']) #room is the room name and game Id
    player2 = storage.get(User, data["to_id"])
    if player2 and game:
        room = data['room']
        session["gameId"]  = game.id
        #player2 joins the private room
        join_room(room)
        player2.color = "black"
        game.black = player2
        socketio.emit("play", {'message':"play", 'game':game.id, "name": session.get("name")}, to=room)

@socketio.on('chat')
def chats(data):
    """ this function handles chat room for the 2 players """
    room = session.get("gameId")
    if room:
        player2 = storage.get(User, data["from_id"])
        join_room(room)
        send({'message':"chat", "name":player2.username, 'content':data['content']}, to=room)
    return



if __name__ == '__main__':
     socketio.run(app, debug=True)
