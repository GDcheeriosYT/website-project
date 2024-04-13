import time

import Client_Credentials

from .GentrysQuestManager import GentrysQuestManager


class GentrysQuestClassicManager(GentrysQuestManager):
    def __init__(self, version: str):
        print("\nLoading Gentry's Quest Classic data\n")
        time.sleep(Client_Credentials.section_load_time)

        super().__init__(version, True)

    @staticmethod
    def attribute_convert(attribute: int):
        if attribute == 0:
            return "health"
        elif attribute == 1:
            return "attack"
        elif attribute == 2:
            return "defense"
        elif attribute == 3:
            return "critrate"
        elif attribute == 4:
            return "critdamage"
