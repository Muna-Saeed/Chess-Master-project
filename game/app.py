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

@app.route('/user/<username>')
def user_profile(username):
    # Assuming you have a dictionary of users where the key is the username
    # and the value is a dictionary containing user information
    users = {
        "alice": {"username": "Alice", "rating": 1200},
        "bob": {"username": "Bob", "rating": 1100}
    }

    # Get the user information based on the provided username
    user_info = users.get(username)

    if user_info:
        # Pass the user information to the template
        return render_template('user_profile.html', user=user_info)
    else:
        # Handle the case where the provided username doesn't exist
        return "User not found", 404

@app.route('/settings')
def settings():
    # Sample data for demonstration
    settings_data = {
        "theme": "dark",
        "notifications": True,
        "sound": False
    }

    # Pass the settings data to the template
    return render_template('settings.html', settings=settings_data)

@app.route('/history')
def game_history():
    # Sample data for demonstration
    game_history_data = [
        {"date": "2024-02-01", "opponent": "Alice", "result": "Win"},
        {"date": "2024-02-15", "opponent": "Bob", "result": "Draw"},
        {"date": "2024-03-05", "opponent": "Charlie", "result": "Loss"}
    ]

    # Pass the game history data to the template
    return render_template('game_history.html', history=game_history_data)

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
