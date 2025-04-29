from flask import Flask, render_template, jsonify, request
import random
from collections import defaultdict
from spades.spades import SpadesGame


# 临时存储游戏状态和座位状态（生产环境应使用数据库）
games = {}


class SpadesGame:
    def __init__(self):
        self.players_info = [
            {'name': '玩家1', 'avatar': './static/avatar1.png', 'id': 0, 'hand': [],'seat_id':None},
            {'name': '玩家2', 'avatar': './static/avatar2.png', 'id': 1, 'hand': []},
            {'name': '玩家3', 'avatar': './static/avatar3.png', 'id': 2, 'hand': []},
            {'name': '玩家4', 'avatar': './static/avatar4.png', 'id': 3, 'hand': []},
        ]
        self.deck = []
        self.current_player = 0
        self.played_cards = []
        self.players = {
            0: {'hand': [], 'bid': 0, 'tricks': 0, 'position': 'top-player'},
            1: {'hand': [], 'bid': 0, 'tricks': 0, 'position': 'left-player'},
            2: {'hand': [], 'bid': 0, 'tricks': 0, 'position': 'right-player'},
            3: {'hand': [], 'bid': 0, 'tricks': 0, 'position': 'bottom-player'},
        }

        self.trump = 'spades'
        self.phase = 'bidding'  # or 'playing'
        self.order = ['north', 'east', 'south', 'west']
        self.seats = [0, 0, 0, 0]
        self.current_player_index = 0

    def new_game(self):
        # 创建并洗牌
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [{'suit': s, 'rank': r, 'filename': f"{r}_of_{s}.png"} for s in suits for r in ranks]
        random.shuffle(self.deck)
        
    def select_seat(self, seat_id, player_id):
        if 0 <= seat_id < len(self.seats) and self.seats[seat_id] == 0:
            self.seats[seat_id] = player_id
            return True
        else:
            return False

        
        
    def play_card(self, player, card_index):
        # 检查当前玩家是否正确
        if player != self.current_player:
          return False

        # 验证出牌逻辑
        hand = self.players[player]['hand']
        if 0 <= card_index < len(hand):
            played_card = hand.pop(card_index)
            self.played_cards.append({
                'player': player,
                'card': played_card,
            })
            self.current_player_index = (self.current_player_index + 1) % len(self.order)
            if self.current_player_index == 0 :
              self.calculate_trick_winner()
              self.played_cards = []
            return True
        return False

    def calculate_trick_winner(self):
        # 确定赢墩的逻辑
        leading_suit = self.played_cards[0]['card']['suit']
        trump = self.trump
        if len(self.played_cards) == len(self.players):
          valid_cards = []
          for play in self.played_cards:
              card = play['card']
              if card['suit'] == trump:
                  valid_cards.append((play['player'], card))
              elif card['suit'] == leading_suit and not trump in [item[1]['suit'] for item in valid_cards]:
                  valid_cards.append((play['player'], card))
          
          # 比较牌大小（A最大）
          ranks_order = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
          winner = max(valid_cards, key=lambda x: ranks_order.index(x[1]['rank']))
          self.players[winner[0]]['tricks']+=1
          return winner[0]
        return None

app = Flask(__name__)

@app.route('/')
def main_index():
    
    if not games:
        games['game_id'] = SpadesGame()
    game = games.get('game_id')
    
    #如果已经选了座位，则显示index.html，如果没有选择，则显示select_seat.html
    
    
    if len([i for i in game.seats if i!=0]) != 0:
        return index(game)
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
