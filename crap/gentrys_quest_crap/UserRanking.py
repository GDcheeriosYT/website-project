from crap.PSQLConnection import PSQLConnection as DB


class UserRanking:
    id = None
    weighted = None
    unweighted = None
    rank = None
    tier = None

    def __init__(self, id):
        result = DB.get("SELECT c_weighted, c_unweighted, c_rank, c_tier FROM rankings where id = %s;", params=(id,))
        self.id = id,
        try:
            self.weighted = result[0]
            self.unweighted = result[1]
            self.rank = result[2]
            self.tier = result[3]
        except TypeError:
            pass
