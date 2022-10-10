import json

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
    for character in account_data["inventory"]["characters"]:
        power_level += character["star rating"]
        power_level += character["experience"]["level"]
        equips = character["equips"]
        for artifact in equips["artifacts"]:
            power_level += artifact["star rating"]
            power_level += artifact["experience"]["level"]

        try:
            power_level += equips["weapon"]["star rating"]
            power_level += equips["weapon"]["experience"]["level"]
            power_level += equips["weapon"]["stats"]["attack"] / 2
        except KeyError:
            pass

    for artifact in account_data["inventory"]["artifacts"]:
        power_level += artifact["star rating"]
        power_level += artifact["experience"]["level"]

    for weapon in account_data["inventory"]["weapons"]:
        power_level += weapon["star rating"]
        power_level += weapon["experience"]["level"]
        power_level += weapon["stats"]["attack"] / 2
    
    return int(power_level)