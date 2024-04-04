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

@app.route('/play')
def play():
    return render_template('login.html')

@app.route('/user')
def user_profile():
    return render_template('user_profile.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/history')
def game_history():
    return render_template('game_history.html')

@app.route('/api/players')
def get_players():
    return jsonify(players)

@app.route('/api/games', methods=['GET', 'POST'])
def manage_games():
    if request.method == 'GET':
        return jsonify(games)
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({"message": "New game created"})


@socketio.on("connect")
def connect(auth):
    if not rooms:
        return
    room = session.get("main")
    name = session.get("name")
    player_id = session.get("player_id")
    if room:
        join_room(room)
        rooms[room]['members'] += 1
        send({"name":name, "message": 'connected', 'player_id':player_id}, to=room)
        print("joined ************** ", name)
    else:
        print(" not joined **************")

@socketio.on("disconnect")
def disconnect():
    name = session.get("name")
    player_id = session.get("player_id")
    for key in rooms.keys():
        leave_room(key)
        send({"name":name, "message": 'diconnected', 'player_id':player_id}, to=key)
        
    print("leaved **************", name)


@socketio.on('message')
def handle_message(data):
    print(data)
    if data["message"] == "board":
        room = session.get("gameId")
        player_id = session.get("player_id")
        send({'message':"board", 'start':data['start'], 'end':data['end'], 'game':data['game'], 'player_id':player_id}, to=room)
        return 
    elif data["message"] == "accept":
        print("recieved accept **", data)
        player2 = storage.get(User, data["to_id"])
        game = storage.get(Game, data['room'])
        print("************", data['room'])
        if player2 and game:
            print("recieved accept **", data)
            room = data['room']
            session["gameId"]  = game.id
            join_room(room)
            player2.color = "black"
            game.black = player2
            send({'message':"play", 'game':game.id}, to=room)
        return
    elif data["message"] == "chat":
        room = session.get("gameId")
        player2 = storage.get(User, data["from_id"])
        if room:
            send({'message':"chat", "name":player2.username, 'content':data['content']}, to=room)
        print(room, "#########################")
        return
    elif data["message"] == "invite":
        game = Game()
        session["gameId"]  = game.id
        player1 = storage.get(User, data["from_id"])
        player1.color="white"
        game.white = player1
        rooms[game.id] = {"members":0, "messages":[]}
        game.first_move = {str(1 * 8 + i):False for i in range(8)}
        for i in range(48, 56):
            game.first_move[str(i)] = False
        join_room(game.id)
        room = "main"
        player_id = session.get("player_id")
        name = session.get("name")
        storage.new(game)
        #storage.save()
        send({'room':game.id, "message": data['message'], 'player_id':player_id, 'from_id':data['from_id']}, to=room)        
        return        
    room = session.get("main")
    player_id = session.get("player_id")
    name = session.get("name")
    print('Received message:*************', data)
    send({"name":name, "message": data['message'], 'player_id':player_id, 'from_id':data['from_id']}, to=room)


@app.route('/auth', methods=["POST", "GET"])
def auth():
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


    

if __name__ == '__main__':
     socketio.run(app, debug=True)
