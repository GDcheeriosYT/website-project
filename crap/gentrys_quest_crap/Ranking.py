class Ranking:
    def __init__(self, rank: str = "unranked", tier: str = ""):
        self.rank = rank
        self.tier = tier

    def __repr__(self):
        return {
            'ranking': self.rank,
            'tier': self.tier,
        }
