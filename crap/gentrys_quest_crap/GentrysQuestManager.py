import json
import os
from GPSystem.GPmain import GPSystem

GPSystem = GPSystem()


class GentrysQuestManager:
    players = None
    online_players = None
    rater = GPSystem

    def __init__(self):
        self.players = []
        self.online_players = []
        print("initializing player data")
        account_list = os.listdir("accounts")
        account_list_length = len(account_list)
        counter = 1
        for data in account_list:
            print(f"{int((counter / account_list_length * 100))}%")
            id = data[:-5]
            data = json.load(open(f"accounts/{data}", "r"))
            username = data["username"]
            gq_data = data["metadata"]["Gentry's Quest data"]
            if gq_data is None:
                gq_data = 0
            self.players.append(Player(username, id, gq_data))

            counter += 1

        self.sort_players()

    def sort_players(self):
        def sort_thing(player: Player):
            # print(player)
            return player.power_level['weighted']

        print("sorting gq players!")
        self.players.sort(key=sort_thing, reverse=True)
        print("done!")

    def get_leaderboard(self, min_index: int = 0, max_index: int = 50):
        new_list = []

        counter = min_index

        while counter < max_index:
            try:
                if self.players[counter].power_level['weighted'] > 0:
                    new_list.append(self.players[counter])
            except IndexError:
                break

            counter += 1

        return new_list

    def update_player_power_level(self, id):
        for player in self.players:
            if id == player.id:
                player.update_power_level()
                break

    def get_player_power_level(self, id):
        for player in self.players:
            if id == player.id:
                return player.power_level

    def check_in_player(self, id):
        for player in self.players:
            if id == player.id:
                self.online_players.append(player)
                break

    def check_out_player(self, id):
        for player in self.players:
            if id == player.id:
                self.online_players.remove(player)
                break
