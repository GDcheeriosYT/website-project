from typing import List

from crap.osu_crap.Player import Player


class TeamData:
    def __init__(self, team_name: str, players: List[Player]):
        self.team_name = team_name
        self.players = players

    def jsonify(self) -> dict:
        return {
            "players": [player.id for player in self.players]
        }
