from __future__ import annotations

from typing import List, Tuple

from player import Player
import constants as c


class Team:
    def __init__(self, team_id: c.TeamID, color: Tuple[int, int, int]) -> None:
        self.team_id: c.TeamID = team_id
        self.score: int = 0
        self.players: List[Player] = []
        self.color: Tuple[int, int, int] = color

    def add_player(self, player: Player) -> None:
        self.players.append(player)
        player.color = self.color