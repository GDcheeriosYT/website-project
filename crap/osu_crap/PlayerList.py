import json
import time

import Client_Credentials
from crap.ServerData import ServerData

from .Player import Player


# this is static because we will use the instance in other files
class PlayerList:
    Players = []

    @staticmethod
    def load() -> None:
        for id in ServerData.osu_player_json:
            print(f"loading osu player {id}")
            PlayerList.Players.append(PlayerList.create_player(id))
            time.sleep(Client_Credentials.load_time)

    @staticmethod
    def unload() -> None:
        for player in PlayerList.Players:
            ServerData.osu_player_json[player.id] = player.jsonify()[player.id]

        with open("player_data.json", "w") as f:
            json.dump(ServerData.osu_player_json, f, indent=4)

    @staticmethod
    def get_users(user_list) -> list:
        new_list = []
        for player in PlayerList.Players:
            id = str(player.id)
            if id in user_list:
                new_list.append(player)
            else:
                new_list.append(PlayerList.create_player(id))

        return new_list

    @staticmethod
    def create_player(id):
        return Player(id)
