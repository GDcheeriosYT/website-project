from typing import List

from .Nickname import Nickname
from .PlayerList import PlayerList
from .TeamData import TeamData


class Match:
    def __init__(self, json_data, has_ended: bool):
        self.name = json_data["match name"]
        self.players = PlayerList.get_users(json_data["users"])
        self.initial_score = json_data["initial score"]
        self.final_score = json_data["final score"]
        self.initial_playcount = json_data["initial playcount"]
        self.final_playcount = json_data["final playcount"]
        self.team_data = []

        team_metadata = json_data["team metadata"]

        for team in team_metadata.keys():
            self.team_data.append(TeamData(team, PlayerList.get_users(team_metadata[team]["players"]), team_metadata[team]["team color"]))

        self.mode = json_data["mode"]
        self.nicknames = []

        for id in json_data["nicknames"].keys():
            self.nicknames.append(Nickname(id, json_data["nicknames"][id]))

        self.ended = has_ended
