import json
import os
from GPSystem.GPmain import GPSystem

GPSystem = GPSystem()

def data_extractor(json_data):
    if json_data["metadata"]["Gentry's Quest data"] is not None:
        return json_data["username"], json_data["metadata"]["Gentry's Quest data"]


class Player:
    account_name = None
    id = None
    power_level = None

    def __init__(self, account_name, id, data):
        self.account_name = account_name
        self.id = id
        if isinstance(data, int):
            self.power_level = {
                'unweighted': 0,
                'weighted': 0
            }
            self.ranking = ('unranked', '')
        else:
            gps_stuff = GPSystem.rater.generate_power_details(data)
            self.power_level = gps_stuff['rating']
            self.ranking = gps_stuff['ranking']['tier'], gps_stuff['ranking']['tier value']

        if self.ranking[0] == 'copper':
            self.color = "red"
        elif self.ranking[0] == 'bronze':
            self.color = "brown"
        elif self.ranking[0] == 'silver':
            self.color = "gray"
        elif self.ranking[0] == 'gold':
            self.color = "gold"
        elif self.ranking[0] == 'platinum':
            self.color = "blue"
        elif self.ranking[0] == 'diamond':
            self.color = "cyan"
        elif self.ranking[0] == 'gentry warrior':
            self.color = "lime"
        else:
            self.color = "#00000000"
            self.ranking = ('', '')

    def update_power_level(self):
        old_pl = self.power_level
        gps_stuff = GPSystem.rater.generate_power_details(data_extractor(json.load(open(f"accounts/{self.id}.json", "r")))[1])
        self.power_level = gps_stuff['rating']
        self.ranking = gps_stuff['ranking']
        print(f"{self.account_name} power level just updated!\n{old_pl} -> {self.power_level} {self.ranking}")

    def __repr__(self):
        json_thing = {
            "username": self.account_name,
            "id": self.id,
            "power level": self.power_level,
            "ranking": self.ranking
        }
        return str(json_thing)


class GentrysQuestDataHolder:
    players = None
    online_players = None
    multiplayer_rooms = None

    def __init__(self):
        self.players = []
        self.multiplayer_rooms = []
        self.online_players = []
        print("initializing player data")
        account_list = os.listdir("accounts")
        account_list_length = len(account_list)
        counter = 1
        for data in account_list:
            print(f"{int((counter/account_list_length * 100))}%")
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
        