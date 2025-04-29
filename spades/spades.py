import random

class SpadesGame():
    def __init__(self):
        self.seats = [0, 0, 0, 0]  # 0: 空闲, 1: 已占用
        self.players_info = [
            {'name': '玩家1', 'avatar': './static/avatar1.png', 'id': 0, 'hand': []},
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
        self.current_player_index = 0
        
    def new_game(self):
        # 创建并洗牌
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [{'suit': s, 'rank': r, 'filename': f"{r}_of_{s}.png"} for s in suits for r in ranks]
        random.shuffle(self.deck)
        
        # 发牌给四个玩家
        cards_per_player = len(self.deck) // len(self.players)
        for i, player in enumerate(self.players_info):
            start_index = i * cards_per_player
            end_index = (i + 1) * cards_per_player
            hand = self.deck[start_index:end_index] 
            self.players[player][\'hand\'] = sorted(hand, key=lambda x: (x[\'suit\'], ranks.index(x[\'rank\'])))
        self.deck = []


    def select_seat(self, seat_id, player_id):
        if 0 <= seat_id < len(self.seats) and self.seats[seat_id] == 0:
            self.seats[seat_id] = player_id
            return True
        return False
