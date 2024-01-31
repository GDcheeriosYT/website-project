from .Nickname import Nickname
from .PlayerList import PlayerList
from .TeamData import TeamData
from .Player import Player


class Match:
    def __init__(self, json_data, has_ended: bool):
        self.name = json_data["match name"]

        print(f"Loading match {self.name}")

        self.players = PlayerList.get_users(json_data["users"])
        self.initial_score = json_data["initial score"]
        self.initial_playcount = json_data["initial playcount"]

        # check if they have final values
        try:
            self.final_score = json_data["final score"]
            self.final_playcount = json_data["final playcount"]
        except KeyError:
            self.final_score = 0
            self.final_playcount = 0

        self.team_data = []

        team_metadata = json_data["team metadata"]

        for team in team_metadata.keys():
            players = PlayerList.get_users(team_metadata[team]["players"])
            self.team_data.append(TeamData(team, players))

        self.mode = json_data["mode"]
        self.nicknames = []

        for id in json_data["nicknames"].keys():
            self.nicknames.append(Nickname(id, json_data["nicknames"][id]))

        self.ended = has_ended

    def get_score(self, player: Player) -> int:
        pos = self.players.index(player)
        if self.ended:
            return self.final_score[pos] - self.initial_score[pos]
        else:
            return player.score - self.initial_score[pos]

    def get_playcount(self, player: Player) -> int:
        pos = self.players.index(player)
        if self.ended:
            return self.final_playcount[pos] - self.initial_playcount[pos]
        else:
            return player.play_count - self.initial_playcount[pos]

    def jsonify(self) -> dict:
        team_metadata = {}
        nicknames = {}

        for team in self.team_data:
            team_metadata[team.team_name] = team.jsonify()

        for nickname in self.nicknames:
            nicknames[nickname.id] = nickname.name

        return {
            "users": [str(player.id) for player in self.players],
            "match name": self.name,
            "initial score": self.initial_score,
            "initial playcount": self.initial_playcount,
            "mode": self.mode,
            "team metadata": team_metadata,
            "nicknames": nicknames
        }
