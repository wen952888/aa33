from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import random
from spades.spades import SpadesGame

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 生产环境应使用环境变量

games = {}

@app.route('/')
def main_index():
    # 如果未创建游戏会话，直接重定向到座位选择
    if 'game_id' not in session:
        return redirect(url_for('select_seat_ui'))
    
    game_id = session['game_id']
    game = games.get(game_id)
    
    # 如果游戏不存在或未满员，保持在选择界面
    if not game or not all(game.seats):
        return redirect(url_for('select_seat_ui'))
    
    return render_template('index.html', players_info=game.players_info)

@app.route('/select-seat')
def select_seat_ui():
    """独立座位选择页面"""
    return render_template('select_seat.html')

@app.route('/api/new-game', methods=['POST'])
def new_game():
    game_id = str(random.randint(1000,9999))
    session['game_id'] = game_id
    games[game_id] = SpadesGame()
    return jsonify({'game_id': game_id})

@app.route('/api/select-seat', methods=['POST'])
def select_seat():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'Invalid session'}), 400
    
    data = request.get_json()
    success = games[game_id].select_seat(
        seat_id=data['seat_id'],
        player_id=data['player_id']
    )
    return jsonify({'success': success})

# 其他路由保持不变...
