import random

class SpadesGame:
    def __init__(self):
        self.seats = [0, 0, 0, 0]  # 座位状态
        self.players_info = [
            {'name': '玩家1', 'avatar': 'avatar1.png', 'id': 0, 'hand': []},
            {'name': '玩家2', 'avatar': 'avatar2.png', 'id': 1, 'hand': []},
            {'name': '玩家3', 'avatar': 'avatar3.png', 'id': 2, 'hand': []},
            {'name': '玩家4', 'avatar': 'avatar4.png', 'id': 3, 'hand': []},
        ]
        self.deck = []
        self.current_player = 0
        self.played_cards = []
        self.players = {
            0: {"hand": [], "bid": 0, "tricks": 0},
            1: {"hand": [], "bid": 0, "tricks": 0},
            2: {"hand": [], "bid": 0, "tricks": 0},
            3: {"hand": [], "bid": 0, "tricks": 0},
        }
        self.trump = 'spades'
        self.phase = 'bidding'
        self.current_player_index = 0

    def new_game(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [{"suit": s, "rank": r, "filename": f"cards/{r}_of_{s}.png"} for s in suits for r in ranks]
        random.shuffle(self.deck)
        
        # 正确发牌逻辑
        cards_per_player = 13
        for i in range(4):
            start = i * cards_per_player
            end = start + cards_per_player
            self.players[i]['hand'] = sorted(
                self.deck[start:end],
                key=lambda x: (x['suit'], ranks.index(x['rank']))
        self.deck = []

    def select_seat(self, seat_id, player_id):
        if 0 <= seat_id < 4 and self.seats[seat_id] == 0:
            self.seats[seat_id] = player_id
            return True
        return False

    def play_card(self, player, card_index):
        try:
            card = self.players[player]['hand'].pop(card_index)
            self.played_cards.append(card)
            return True
        except IndexError:
            return False
