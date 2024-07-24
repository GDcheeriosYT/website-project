from GPSystem.GPmain import GPSystem
from crap.PSQLConnection import PSQLConnection as DB


class GQManager:
    @staticmethod
    def load_rankings():
        version = GPSystem.version
        print("Loading rankings")
        print("#1 Rating items")
        rater = GPSystem.rater
        items = DB.get_group("SELECT id, type, owner, metadata, version FROM gentrys_quest_items;")
        for item in items:
            if item[4] != version:  # check the version
                if item[1] == "character":
                    rating = rater.get_character_rating(item[3])
                elif item[1] == "artifact":
                    rating = rater.get_artifact_rating(item[3])
                else:
                    rating = rater.get_weapon_rating(item[3])

                DB.do(f"UPDATE gentrys_quest_items SET rating = {rating}, version = \'{version}\' where id = {item[0]}")

        print("#2 Ranking users (classic)")
        for id in DB.get_group("SELECT distinct owner FROM gentrys_quest_items where is_classic = true;"):
            id = id[0]
            GQManager.update_rating(id, True)

        print("#2 Ranking users (current)")
        for id in DB.get_group("SELECT distinct owner FROM gentrys_quest_items where is_classic = false;"):
            id = id[0]
            GQManager.update_rating(id, False)

    @staticmethod
    def update_rating(id, classic: bool) -> None:
        # weighting
        weighted = (GQManager.get_weighted_rating(id, "character", classic) +
                    GQManager.get_weighted_rating(id, "artifact", classic) +
                    GQManager.get_weighted_rating(id, "weapon", classic))
        DB.do(f"UPDATE rankings SET {'c_weighted' if classic else 'weighted'} = %s WHERE id = %s;",
              params=(weighted, id))  # weighted
        DB.do(
            f"UPDATE rankings SET {'c_unweighted' if classic else 'unweighted'} = (SELECT SUM(rating) FROM gentrys_quest_items WHERE owner = %s) WHERE id = %s;",
            params=(id, id))  # unweighted

    # <editor-fold desc="getters">

    @staticmethod
    def get_rating(id):
        raise NotImplementedError

    @staticmethod
    def get_data(id, is_classic: bool) -> dict:
        data = {}
        items = DB.get_group(
            """
            SELECT id, type, metadata
            FROM gentrys_quest_items WHERE owner = %s AND is_classic = %s
            """,
            params=(id, is_classic)
        )

        startup_amount = 0
        money = 0

        if is_classic:
            selection = DB.get("SELECT startup_amount, money FROM gentrys_quest_classic_data WHERE id = %s", params=(id,))
            if selection:
                startup_amount = selection[0]
                money = selection[1]

        data["startup amount"] = startup_amount
        data["money"] = money
        data["items"] = items

        return data

    # </editor-fold>

    @staticmethod
    def get_weighted_rating(id, object_type: str, classic: bool) -> int:
        rating = 0
        counter = 0
        for item in DB.get_group(
                "SELECT rating FROM gentrys_quest_items WHERE owner = %s AND type = %s AND is_classic = %s ORDER BY rating desc limit 100;",
                params=(id, object_type, classic)):
            rating += item[0] * 0.95 ** counter
            counter += 1

        return rating

    @staticmethod
    def get_leaderboard(classic: bool, start: int = 0, amount: int = 50) -> list:
        mode = 'c_weighted' if classic else 'weighted'
        query = f"""
                SELECT rankings.id, accounts.username, rankings.{mode} 
                FROM rankings 
                INNER JOIN accounts ON rankings.id = accounts.id 
                ORDER BY {mode} desc
                LIMIT %s OFFSET %s;
            """

        return DB.get_group(query, params=(amount, start))
