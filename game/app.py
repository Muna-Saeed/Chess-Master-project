# Chess Master project using Flask for the backend

from flask import Flask, render_template, request, jsonify
from game.more_routes.user import routes
from game.more_routes.api import api_route

app = Flask(__name__)
app.register_blueprint(routes)
app.register_blueprint(api_route)

# Sample data for demonstration
players = {
    "player1": {"name": "Alice", "rating": 1200},
    "player2": {"name": "Bob", "rating": 1100}
}

games = []

@app.route('/')
def index():
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
        # Logic to create a new game, add to 'games' list, etc.
        return jsonify({"message": "New game created"})

if __name__ == '__main__':
    app.run(debug=True)
