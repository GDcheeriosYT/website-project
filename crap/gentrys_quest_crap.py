import json
import os

character_factor = 0.95
weapon_factor = 1
artifact_factor = 1


def generate_power_level(account_data):
    def attribute_rater(attribute):
        if isinstance(attribute, dict):
            attribute = attribute["buff"]
        rating = 0
        if attribute[0] == 1:
            rating += attribute[2] * 1.5

        elif attribute[0] == 2:
            rating += attribute[2] * 2.5

        elif attribute[0] == 3:
            rating += attribute[2] * 1

        elif attribute[0] == 4:
            rating += attribute[2] * 3

        elif attribute[0] == 5:
            rating += attribute[2] * 2

        return rating

    power_level = 0

    #characters
    character_ratings = []
    for character in account_data["inventory"]["characters"]:
        character_rating = 0
        character_rating += character["star rating"]
        character_rating += character["experience"]["level"]
        character_rating += ((character["experience"]["level"] / 20) * 2) + 1
        equips = character["equips"]
        for artifact in equips["artifacts"]:
            character_rating += artifact["star rating"] * 1.20
            character_rating += artifact["experience"]["level"]
            character_rating += ((artifact["experience"]["level"] / 4) * 2) + 1
            character_rating += attribute_rater(artifact["stats"]["main attribute"])
            for attribute in artifact["stats"]["attributes"]:
                character_rating += attribute_rater(attribute)

        try:
            character_rating += equips["weapon"]["star rating"] * 1.5
            character_rating += equips["weapon"]["experience"]["level"]
            character_rating += equips["weapon"]["stats"]["attack"] * 0.75
            character_rating += attribute_rater(equips["weapon"]["stats"]["buff"])
        except KeyError:
            pass

        except TypeError:
            pass

        if character["experience"]["xp"] > 0 or character["experience"]["level"] > 1:
            character_ratings.append(character_rating)

    character_ratings.sort(reverse=True)

    # artifacts
    artifact_ratings = []
    for artifact in account_data["inventory"]["artifacts"]:
        artifact_rating = 0
        artifact_rating += artifact["star rating"] * 1.20
        artifact_rating += ((artifact["experience"]["level"] / 4) * 2) + 1

        if artifact["experience"]["xp"] > 0 or artifact["experience"]["level"] > 1:
            artifact_ratings.append(artifact_rating)

    artifact_ratings.sort(reverse=True)

    # weapons
    weapon_ratings = []
    for weapon in account_data["inventory"]["weapons"]:
        weapon_rating = 0
        weapon_rating += weapon["star rating"] * 1.50
        weapon_rating += weapon["experience"]["level"] * 1.26
        weapon_rating += weapon["stats"]["attack"] / 2

        if weapon["experience"]["xp"] > 0 or weapon["experience"]["level"] > 1:
            weapon_ratings.append(weapon_rating)

    weapon_ratings.sort(reverse=True)

    for character_rating in character_ratings:
        power_level += character_rating * (character_factor ** (character_ratings.index(character_rating)))

        # factored_character_rating = '{:,}'.format(character_rating * character_factor**(character_ratings.index(character_rating)))
        # new_character_rating = '{:,}'.format(character_rating)
        # print(f"character #{character_ratings.index(character_rating) + 1} {factored_character_rating} | {new_character_rating}")

    for artifact_rating in artifact_ratings:
        power_level += artifact_rating * (artifact_factor ** (artifact_ratings.index(artifact_rating)))

        # factored_artifact_rating = '{:,}'.format(artifact_rating * artifact_factor**(artifact_ratings.index(artifact_rating)))
        # new_artifact_rating = '{:,}'.format(artifact_rating)
        # print(f"artifact #{artifact_ratings.index(artifact_rating) + 1} {factored_artifact_rating} | {new_artifact_rating}")

    for weapon_rating in weapon_ratings:
        power_level += weapon_rating * (weapon_factor ** (weapon_ratings.index(weapon_rating)))

        # factored_weapon_rating = '{:,}'.format(weapon_rating * weapon_factor**(weapon_ratings.index(weapon_rating)))
        # new_weapon_rating = '{:,}'.format(weapon_rating)
        # print(f"weapon #{weapon_ratings.index(weapon_rating) + 1} {factored_weapon_rating} | {new_weapon_rating}")

    # print(power_level)

    return int(power_level)


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
            self.power_level = data
        else:
            self.power_level = generate_power_level(data)

    def update_power_level(self):
        old_pl = self.power_level
        self.power_level = generate_power_level(data_extractor(json.load(open(f"accounts/{self.id}.json", "r")))[1])
        print(f"{self.account_name} power level just updated!\n{old_pl} -> {self.power_level}")

    def __repr__(self):
        json_thing = {
            "username": self.account_name,
            "id": self.id,
            "power level": self.power_level
        }


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
            return player.power_level

        print("sorting gq players!")
        self.players.sort(key=sort_thing, reverse=True)
        print("done!")

    def get_leaderboard(self, min_index: int = 0, max_index: int = 50):
        new_list = []

        counter = min_index

        while counter < max_index:
            try:
                if self.players[counter].power_level > 0:
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
        