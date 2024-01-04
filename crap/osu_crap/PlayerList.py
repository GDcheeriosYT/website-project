import json

from crap.osu_crap.Player import Player


class PlayerList:
    Players = []
    Player_json = json.load(open("player_data.json", "r"))

    @staticmethod
    def unload():
        for player in PlayerList.Players:
            PlayerList.Player_json[player.id] = player.jsonify()[player.id]

        with open("player_data.json", "r") as f:
            json.dump(PlayerList.Player_json, f)

    @staticmethod
    def get_users(user_list):
        new_list = []
        for player in PlayerList.Players:
            id = str(player.id)
            if id in user_list:
                new_list.append(player)
            else:
                new_list.append(Player(id))
