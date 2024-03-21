# Chess Master project using Flask for the backend

from flask import Flask, render_template, request, jsonify
from game.more_routes.user import routes


app = Flask(__name__)
app.register_blueprint(routes)

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
    return render_template('play.html')

@app.route('/user')
def play():
    return render_template('user_profile.html')

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
