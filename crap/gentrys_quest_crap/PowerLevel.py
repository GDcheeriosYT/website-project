class PowerLevel:
    def __init__(self, weighted: int = 0, unweighted: float = 0.00):
        self.weighted = weighted
        self.unweighted = unweighted

    def jsonify(self):
        return {
            'weighted': self.weighted,
            'unweighted': self.unweighted,
        }
