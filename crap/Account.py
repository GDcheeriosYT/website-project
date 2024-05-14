import os

from .JsonHelper import JsonHelper


class Account:
    def __init__(self, id):
        print(f"Loading account: {id}")

        self.id = id

        directory = f"accounts/{id}"

        self.data = JsonHelper(f"{directory}/data.json")

        self.username = self.data.safe_ensured_key("username")
        self.password = self.data.safe_ensured_key("password")
        self.pfp = self.data.safe_ensured_key("pfp url")
        self.osu_id = self.data.safe_ensured_key("osu id")
        self.perms = self.data.safe_ensured_key("perms")
        self.about = self.data.safe_ensured_key("about me")

        gqc_directory = f"{directory}/gentrys quest classic data"
        gq_directory = f"{directory}/gentrys quest data"

        self.gqc_data = JsonHelper.conditional_init(f"{gqc_directory}/data.json")
        self.gq_data = JsonHelper.conditional_init(f"{gq_directory}/data.json")

    def change_username(self, new_username: str):
        self.username = new_username
        self.update_data()

    def change_pfp(self, new_pfp: str):
        self.pfp = new_pfp
        self.update_data()

    def change_perms(self, new_perms: list):
        self.perms = new_perms
        self.update_data()

    def change_about(self, new_about: str):
        self.about = new_about
        self.update_data()

    def update_data(self):
        self.data.replace_data(self.jsonify())

    def jsonify(self):
        return {
            "username": self.username,
            "password": self.password,
            "pfp url": self.pfp,
            "id": self.id,
            "perms": self.perms,
            "osu id": self.osu_id,
            "about me": self.about
        }
