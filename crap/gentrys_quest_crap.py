import json

character_factor = 1.20
weapon_factor = 0.95
artifact_factor = 0.65


class Player:

    account_name = None
    aura = None
    power_level = None
    
    def __init__(self, account_name, aura=None, power_level=0):
        self.account_name = account_name
        self.aura = aura
        self.power_level = power_level

    def __repr__(self):
        return f"{self.account_name} {self.power_level}p"


def generate_power_level(account_data):
    power_level = 0
    #characters
    print(account_data["inventory"]["characters"][0]["name"])
    character_ratings = []
    for character in account_data["inventory"]["characters"]:
        character_rating = 0
        character_rating += character["star rating"]
        character_rating += character["experience"]["level"]
        equips = character["equips"]
        for artifact in equips["artifacts"]:
            character_rating += artifact["star rating"]
            character_rating += artifact["experience"]["level"]

        try:
            character_rating += equips["weapon"]["star rating"]
            character_rating += equips["weapon"]["experience"]["level"]
            character_rating += equips["weapon"]["stats"]["attack"] / 2
        except KeyError:
            pass

        character_ratings.append(character_rating)

    character_ratings.sort(reverse=True)

    #artifacts
    artifact_ratings = []
    for artifact in account_data["inventory"]["artifacts"]:
        artifact_rating = 0
        artifact_rating += artifact["star rating"]
        artifact_rating += artifact["experience"]["level"]

        artifact_ratings.append(artifact_rating)

    artifact_ratings.sort(reverse=True)

    #weapons
    weapon_ratings = []
    for weapon in account_data["inventory"]["weapons"]:
        weapon_rating = 0
        weapon_rating += weapon["star rating"]
        weapon_rating += weapon["experience"]["level"]
        weapon_rating += weapon["stats"]["attack"] / 2

        weapon_ratings.append(weapon_rating)
    
    weapon_ratings.sort(reverse=True)

    for chararcter_rating in character_ratings:
        power_level += character_rating * character_factor**(character_ratings.index(character_rating))

        factored_character_rating = '{:,}'.format(character_rating * character_factor**(character_ratings.index(character_rating)))
        new_character_rating = '{:,}'.format(character_rating)
        print(f"character #{character_ratings.index(character_rating) + 1} {factored_character_rating} | {new_character_rating}")
    
    for artifact_rating in artifact_ratings:
        power_level += artifact_rating * artifact_factor**(artifact_ratings.index(artifact_rating))

        factored_artifact_rating = '{:,}'.format(artifact_rating * artifact_factor**(artifact_ratings.index(artifact_rating)))
        new_artifact_rating = '{:,}'.format(artifact_rating)
        print(f"artifact #{artifact_ratings.index(artifact_rating) + 1} {factored_artifact_rating} | {new_artifact_rating}")
        
    for weapon_rating in weapon_ratings:
        power_level += weapon_rating * weapon_factor**(weapon_ratings.index(weapon_rating))

        factored_weapon_rating = '{:,}'.format(weapon_rating * weapon_factor**(weapon_ratings.index(weapon_rating)))
        new_weapon_rating = '{:,}'.format(weapon_rating)
        print(f"weapon #{weapon_ratings.index(weapon_rating) + 1} {factored_weapon_rating} | {new_weapon_rating}")
    
    print(power_level)
    
    return int(power_level)