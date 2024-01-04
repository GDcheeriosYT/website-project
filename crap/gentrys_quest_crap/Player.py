from PowerLevel import PowerLevel
from Ranking import Ranking


class Player:
    account_name = None
    id = None
    power_level = None
    ranking = None

    def __init__(self, account_name, id, data):
        self.account_name = account_name
        self.id = id
        self.power_level = PowerLevel()
        self.ranking = Ranking()
        self.color = "white"

    def update_power_level(self, rater):
        old_pl = self.power_level
        gps_stuff = rater.generate_power_details(
            data_extractor(json.load(open(f"accounts/{self.id}.json", "r")))[1])
        self.power_level = gps_stuff['rating']
        self.ranking = gps_stuff['ranking']['tier'], gps_stuff['ranking']['tier value']
        print(f"{self.account_name} power level just updated!\n{old_pl} -> {self.power_level} {self.ranking}")
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

    def __repr__(self):
        json_thing = {
            "username": self.account_name,
            "id": self.id,
            "power level": self.power_level,
            "ranking": self.ranking
        }
        return str(json_thing)