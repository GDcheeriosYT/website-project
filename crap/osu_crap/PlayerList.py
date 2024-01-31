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
        for id in ServerData.osu_player_json.keys():
            print(f"loading osu player {id}")
            PlayerList.create_player(id)
            time.sleep(Client_Credentials.load_time)

    @staticmethod
    def unload() -> None:
        for player in PlayerList.Players:
            print(player.id, player.name)
            ServerData.osu_player_json[player.id] = player.jsonify()[player.id]

        json.dump(ServerData.osu_player_json, open("player_data.json", "w"), indent=4)

    @staticmethod
    def get_users(user_list) -> list:
        new_list = []

        for user_id in user_list:
            found = False
            for player in PlayerList.Players:
                player_id = str(player.id)
                if user_id == player_id:
                    found = True
                    new_list.append(player)

            if not found:
                new_list.append(PlayerList.create_player(user_id))

        return new_list

    @staticmethod
    def create_player(id):
        player = Player(id)
        PlayerList.Players.append(player)
        return player
