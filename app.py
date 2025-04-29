from flask import Flask, render_template, jsonify, request
import random
from spades.spades import SpadesGame


# 临时存储游戏状态和座位状态（生产环境应使用数据库）
games = {}

app = Flask(__name__)

@app.route('/')
def main_index():
    
    if not games:
        games['game_id'] = SpadesGame()
    game = games.get('game_id')
    
    #如果已经选了座位，则显示index.html，如果没有选择，则显示select_seat.html
    
    
    if len([i for i in game.seats if i!=0]) != 0:
        return index(game)#
    else:    
        return render_template('select_seat.html')    

def index(game):   

    #如果座位满了，则初始化游戏
    if all(seat != 0 for seat in game.seats):
        game.new_game()
        # 发牌给四个玩家
        cards_per_player = len(game.deck) // len(game.players)
        for i, player in enumerate(game.players_info):
            start_index = i * cards_per_player
            ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            end_index = (i + 1) * cards_per_player
            hand = game.deck[start_index:end_index] 
            game.players[player['id']]['hand'] = sorted(hand, key=lambda x: (x['suit'], ranks.index(x['rank'])))
        game.deck = []
    return render_template('index.html', players_info=game.players_info)

@app.route('/select_seat', methods=['POST'])
def select_seat():
    seat_id = int(request.form.get('seat_id'))
    player_id = int(request.form.get('player_id'))  # 可以根据需要生成或传递
    game = games.get('game_id')
    if game.select_seat(seat_id, player_id):
        return 'success'
    return 'fail'

@app.route('/status/<game_id>')
def game_status(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify({
        'players': game.players,
        'current_player': game.current_player,
        'phase': game.phase
    })

@app.route('/play/<game_id>', methods=['POST'])
def play_card(game_id):
    data = request.json
    player = data.get('player')
    card_index = data.get('card_index')
    
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    if game.play_card(player, card_index):
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Invalid move'}), 400

if __name__ == '__main__':
    app.run(debug=True)
