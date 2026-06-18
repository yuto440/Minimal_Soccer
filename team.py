from player import Player
import constants as c

class Team:
    def __init__(self, color):
        self.score = 0
        self.players = []
        self.color = color

    def add_player(self, player:Player):
        self.players.append(player)
        player.color = self.color