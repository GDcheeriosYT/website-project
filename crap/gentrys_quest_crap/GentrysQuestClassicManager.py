import time
import requests

import Client_Credentials

from .GentrysQuestManager import GentrysQuestManager


class GentrysQuestClassicManager(GentrysQuestManager):
    def __init__(self):
        print("\nLoading Gentry's Quest Classic data\n")
        time.sleep(Client_Credentials.section_load_time)

        super().__init__(
            requests.get("https://api.github.com/repos/GDcheeriosYT/Gentrys-Quest-Python/releases/latest").json()["name"],
            True
        )

    @staticmethod
    def attribute_convert(attribute: int):
        if attribute == 0:
            return "health"
        elif attribute == 1:
            return "attack"
        if attribute == 2:
            return "defense"
        if attribute == 3:
            return "critrate"
        if attribute == 4:
            return "critdamage"
