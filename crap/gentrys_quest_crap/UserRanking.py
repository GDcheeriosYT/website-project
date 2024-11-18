from crap.PSQLConnection import PSQLConnection as DB


class UserRanking:
    id = None
    weighted = None
    unweighted = None
    rank = None
    tier = None

    def __init__(self, id, classic: bool):
        prefix = 'c_' if classic else ''
        result = DB.get(
            f"""
            SELECT 
                id, 
                {prefix}weighted, 
                {prefix}unweighted, 
                {prefix}rank, 
                {prefix}tier, 
                placement
            FROM (
                SELECT 
                    id, 
                    {prefix}weighted, 
                    {prefix}unweighted, 
                    {prefix}rank, 
                    {prefix}tier, 
                    RANK() OVER (ORDER BY {prefix}weighted DESC) AS placement
                FROM rankings
            ) subquery 
            WHERE id = %s
            """,
            params=(id,)
        )

        self.id = id
        try:
            self.placement = result[5]
            self.weighted = result[1]
            self.unweighted = result[2]
            self.rank = result[3]
            self.tier = result[4]
        except TypeError:
            self.placement = 0
            self.weighted = 0
            self.unweighted = 0
            self.rank = 'unranked'
            self.tier = 'I'

    def jsonify(self) -> dict:
        return {
            'rank': self.rank,
            'score': self.weighted
        }

    def __repr__(self):
        return f"#{self.placement} {self.weighted} {self.rank} {self.tier}"
