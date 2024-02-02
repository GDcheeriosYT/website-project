import time

import Client_Credentials
from crap.ServerData import ServerData
from crap.gentrys_quest_crap.Player import Player

from GPSystem.GPmain import GPSystem

GPSystem = GPSystem()


class GentrysQuestManager:
    players = None
    online_players = None
    rater = GPSystem.rater
    version = None

    def __init__(self, version, is_classic: bool):
        self.players = GentrysQuestManager.get_accounts(is_classic)
        self.online_players = []
        self.version = version

        self.sort_players()

    @staticmethod
    def get_accounts(is_classic: bool) -> list:
        players = []
        counter = 1
        for account in ServerData.account_manager.accounts:
            gq_data = account.gentrys_quest_classic_data if is_classic else account.gentrys_quest_data
            if gq_data:
                print(f"\nLoading {account.username} gq data")
                player = Player(account.username, account.id, gq_data)
                player.update_power_level(GentrysQuestManager.rater)
                players.append(player)
                time.sleep(Client_Credentials.load_time)

        return players

    def sort_players(self):
        def sort_thing(player: Player):
            # print(player)
            return player.power_level.weighted

        print("\nsorting gq players!")
        self.players.sort(key=sort_thing, reverse=True)
        print("done!")

    def get_leaderboard(self, min_index: int = 0, max_index: int = 50):
        new_list = []

        counter = min_index

        while counter < max_index:
            try:
                if self.players[counter].power_level.weighted > 0:
                    new_list.append(self.players[counter])
            except IndexError:
                break

            counter += 1

        return new_list

    def update_player_power_level(self, id):
        for player in self.players:
            if id == player.id:
                player.update_power_level(GentrysQuestManager.rater)
                break

    def get_player_power_level(self, id):
        for player in self.players:
            if id == player.id:
                return player.power_level.jsonify()

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
