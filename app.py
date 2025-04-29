from flask import Flask, render_template, jsonify, request, session
import random
from spades.spades import SpadesGame

app = Flask(__name__)
app.secret_key = random.getrandbits(128)  # 添加session密钥

games = {}

@app.route('/')
def main_index():
    game_id = session.get('game_id')
    
    if not game_id:
        return render_template('select_seat.html')
    
    game = games.get(game_id)
    if not game:
        return render_template('select_seat.html')
    
    if all(seat != 0 for seat in game.seats):
        return render_template('index.html', players_info=game.players_info)
    return render_template('select_seat.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    game_id = str(random.randint(1000,9999))
    session['game_id'] = game_id
    games[game_id] = SpadesGame()
    return jsonify({'game_id': game_id})

@app.route('/select_seat', methods=['POST'])
def select_seat():
    game_id = session.get('game_id')
    if not game_id:
        return jsonify({'error': 'No game session'}), 400
    
    data = request.json
    game = games[game_id]
    if game.select_seat(data['seat_id'], data['player_id']):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'fail'}), 400

@app.route('/status/<game_id>')
def game_status(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify({
        'players': game.players,
        'current_player': game.current_player,
        'phase': game.phase,
        'seats': game.seats
    })

@app.route('/play/<game_id>', methods=['POST'])
def play_card(game_id):
    data = request.json
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    if game.play_card(data['player'], data['card_index']):
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Invalid move'}), 400

if __name__ == '__main__':
    app.run(debug=True)
