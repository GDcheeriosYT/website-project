class Ranking:
    def __init__(self, rank: str = "unranked", tier: str = ""):
        self.rank = rank
        self.tier = tier

    def __repr__(self):
        return f"{self.rank} [{self.tier}]"

    def jsonify(self):
        return {
            'rank': self.rank,
            'tier': self.tier,
        }
