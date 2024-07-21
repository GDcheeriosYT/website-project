import json


from .Player import Player


# this is static because we will use the instance in other files
class PlayerList:
    Players = []

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
