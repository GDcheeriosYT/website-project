import json

from GPSystem.GPmain import GPSystem
from crap.PSQLConnection import PSQLConnection as DB
from crap.gentrys_quest_crap.Item import Item


def ranking(func):
    def wrapper(*args, **kwargs):
        item: Item = func(*args, **kwargs)
        if not item.deleted:
            item.rank_item()

        if item.is_classic:
            result = GQManager.update_user_rating(item.owner, True)
        else:
            result = GQManager.update_user_rating(item.owner, False)

        details = {
            'item': item.jsonify(),
            'user': result
        }

        return details

    return wrapper


class GQManager:
    @staticmethod
    def load_rankings():
        print("Loading rankings")
        print("#1 Rating items")
        items = DB.get_group("SELECT id, type, owner, metadata, version FROM gentrys_quest_items;")
        for item in items:
            if item[4] != GPSystem.version:  # check the version
                if item[1] == "character":
                    rating = GPSystem.rater.get_character_rating(item[3])
                elif item[1] == "artifact":
                    rating = GPSystem.rater.get_artifact_rating(item[3])
                else:
                    rating = GPSystem.rater.get_weapon_rating(item[3])

                DB.do(
                    f"UPDATE gentrys_quest_items SET rating = {rating}, version = \'{GPSystem.version}\' where id = {item[0]}")

        print("#2 Ranking users (classic)")
        for id in DB.get_group("SELECT distinct owner FROM gentrys_quest_items where is_classic = true;"):
            id = id[0]
            GQManager.update_user_rating(id, True)

        print("#2 Ranking users (current)")
        for id in DB.get_group("SELECT distinct owner FROM gentrys_quest_items where is_classic = false;"):
            id = id[0]
            GQManager.update_user_rating(id, False)

    @staticmethod
    def update_user_rating(id, classic: bool) -> dict:
        # weighting
        weighted = (GQManager.get_weighted_rating(id, "character", classic) +
                    GQManager.get_weighted_rating(id, "artifact", classic) +
                    GQManager.get_weighted_rating(id, "weapon", classic))

        DB.do(
            """
            INSERT INTO rankings (id, weighted, unweighted, c_weighted, c_unweighted)
            VALUES (%s, %s, (SELECT SUM(rating) FROM gentrys_quest_items WHERE owner = %s), 0, 0)
            ON CONFLICT (id) DO UPDATE
            SET
                weighted = EXCLUDED.weighted,
                c_weighted = CASE 
                    WHEN EXCLUDED.id IS NOT NULL AND %s THEN EXCLUDED.weighted 
                    ELSE rankings.c_weighted 
                END,
                unweighted = (SELECT SUM(rating) FROM gentrys_quest_items WHERE owner = EXCLUDED.id);
            """,
            params=(id, weighted, id, classic)
        )

        return GQManager.get_ranking(id, classic)

    @staticmethod
    @ranking
    def update_item(id: int, data):
        return Item.update_to_init(id, data)

    @staticmethod
    @ranking
    def add_item(item_type: str, data, is_classic: bool, owner: int):
        return Item.create_item(item_type, data, is_classic, owner)

    @staticmethod
    @ranking
    def remove_item(id: int):
        return Item.remove(id)

    @staticmethod
    def remove_items(id_list: list):
        for id in id_list:
            GQManager.remove_item(id)

    @staticmethod
    def submit_classic_data(id: int, start_amount: int, money: int):
        DB.do("""
            INSERT INTO gentrys_quest_classic_data (id, startup_amount, money)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) 
            DO UPDATE SET startup_amount = EXCLUDED.startup_amount, money = EXCLUDED.money
        """, params=(id, start_amount, money))

        return ":thumbs_up:"

    # <editor-fold desc="getters">

    @staticmethod
    def get_rating(id):
        raise NotImplementedError

    @staticmethod
    def get_item(id) -> Item:
        return Item(id)

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
            selection = DB.get("SELECT startup_amount, money FROM gentrys_quest_classic_data WHERE id = %s",
                               params=(id,))
            if selection:
                startup_amount = selection[0]
                money = selection[1]

        data["startup amount"] = startup_amount
        data["money"] = money
        data["items"] = items

        return data

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

    @staticmethod
    def get_ranking(id: int, classic: bool) -> dict:
        mode = 'c_weighted' if classic else 'weighted'
        result = DB.get(f"SELECT id, weighted, rank "
                        "FROM (SELECT id, weighted, RANK() OVER (ORDER BY weighted DESC) AS rank "
                        "FROM rankings"
                        ") subquery where id = %s", params=(id,))
        if result:
            return {
                'rank': result[2],
                'score': result[1]
            }

        return {
            'rank': 0,
            'score': 0
        }

    # </editor-fold>
