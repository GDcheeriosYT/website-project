import json
import os

from crap.ServerData import ServerData


from GPSystem.GPmain import GPSystem

GPSystem = GPSystem()


class GentrysQuestManager:
    players = None
    online_players = None
    rater = GPSystem
    version = None

    def __init__(self, version, players):
        self.players = players
        self.online_players = []
        self.version = version

        self.sort_players()

    @staticmethod
    def get_accounts(key_name: str):
        players = []
        counter = 1
        account_list_length = len(ServerData.accounts)
        for account in ServerData.accounts:
            print(f"{int((counter / account_list_length * 100))}%")
            gq_data = data["metadata"][key_name]
            if gq_data is None:
                gq_data = 0

            players.append(Player(username, id, gq_data))


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
