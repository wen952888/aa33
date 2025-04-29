from flask import Flask, render_template, jsonify, request
import random
from collections import defaultdict

app = Flask(__name__)

# 临时存储游戏状态（生产环境应使用数据库）
games = {}

class SpadesGame:
    def __init__(self):
        self.players = {
            'north': {'hand': [], 'bid': 0, 'tricks': 0},
            'east': {'hand': [], 'bid': 0, 'tricks': 0},
            'south': {'hand': [], 'bid': 0, 'tricks': 0},
            'west': {'hand': [], 'bid': 0, 'tricks': 0}
        }
        self.deck = []
        self.current_player = 'north'
        self.played_cards = []
        self.trump = 'spades'
        self.phase = 'bidding'  # or 'playing'

    def new_game(self):
        # 创建并洗牌
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = []
        for s in suits:
            for r in ranks:
                filename = f"{r}_of_{s}.png"
                self.deck.append({'suit': s, 'rank': r, 'filename': filename})
        random.shuffle(self.deck)
        
        # 发牌（每人13张）
        for player in self.players:
            hand = self.deck[:13]
            for card in hand:
                card['filename'] = card['filename']
            self.players[player]['hand'] = sorted(hand, key=lambda x: (x['suit'], ranks.index(x['rank'])))
            self.deck = self.deck[13:]

        
        
    def play_card(self, player, card_index):
        # 验证出牌逻辑
        hand = self.players[player]['hand']
        if 0 <= card_index < len(hand):
            played_card = hand.pop(card_index)
            self.played_cards.append({
                'player': player,
                'card': played_card
            })
            return True
        return False

    def calculate_trick_winner(self):
        # 确定赢墩的逻辑
        leading_suit = self.played_cards[0]['card']['suit']
        trump = self.trump
        
        valid_cards = []
        for play in self.played_cards:
            card = play['card']
            if card['suit'] == trump:
                valid_cards.append((play['player'], card))
            elif card['suit'] == leading_suit and not trump:
                valid_cards.append((play['player'], card))
        
        # 比较牌大小（A最大）
        ranks_order = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        winner = max(valid_cards, key=lambda x: ranks_order.index(x[1]['rank']))
        return winner[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    game_id = str(random.randint(1000,9999))
    games[game_id] = SpadesGame()
    games[game_id].new_game()
    return jsonify({'game_id': game_id})

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
