from .PowerLevel import PowerLevel
from .Ranking import Ranking


class Player:
    account_name = None
    id = None
    power_level = None
    ranking = None

    def __init__(self, account_name, id, data):
        self.account_name = account_name
        self.id = id
        self.data = data
        self.power_level = PowerLevel()
        self.ranking = Ranking()
        self.color = "white"

    def update_power_level(self, rater):
        old_pl = self.power_level.unweighted
        gps_stuff = rater.generate_power_details(self.data)
        self.power_level.unweighted,self.power_level.weighted = gps_stuff['rating']['unweighted'], gps_stuff['rating']['weighted']
        self.ranking.rank, self.ranking.tier = gps_stuff['ranking']['tier'], gps_stuff['ranking']['tier value']
        print(f"{self.account_name} power level just updated!\n{old_pl} -> {self.power_level.unweighted} {self.ranking}")
        if self.ranking.rank == 'copper':
            self.color = "red"
        elif self.ranking.rank == 'bronze':
            self.color = "brown"
        elif self.ranking.rank == 'silver':
            self.color = "gray"
        elif self.ranking.rank == 'gold':
            self.color = "gold"
        elif self.ranking.rank == 'platinum':
            self.color = "blue"
        elif self.ranking.rank == 'diamond':
            self.color = "cyan"
        elif self.ranking.rank == 'gentry warrior':
            self.color = "lime"
        else:
            self.color = "#00000000"
            self.ranking = Ranking()

    def jsonify(self):
        json_thing = {
            "username": self.account_name,
            "id": self.id,
            "power level": self.power_level.jsonify(),
            "ranking": self.ranking.jsonify()
        }
        return str(json_thing)