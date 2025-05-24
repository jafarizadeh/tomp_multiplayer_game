class GameLogic:
    def __init__(self, game_map):
        self.map = game_map
        self.players = {}

    def add_player(self, player):
        self.players[player.id] = player

    def handle_move(self, player_id, direction):
        pass

    def handle_collision(self, player):
        pass

    def check_win_condition(self):
        pass

    