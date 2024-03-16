from JsonHelper import JsonHelper


class Account:
    def __init__(self, id):
        print(f"Loading account: {id}")

        self.id = id

        directory = f"accounts/{id}"

        self.data = JsonHelper(f"{directory}/account_data.json")

        self.username = self.data.safe_assured_key("username")
        self.password = self.data.safe_assured_key("password")
        self.pfp = self.data.safe_assured_key("pfp url")
        self.osu_id = self.data.safe_assured_key("osu id")

        gqc_directory = f"{directory}/gentrys quest classic data"

        self.gqc_data = JsonHelper(f"{gqc_directory}/data.json")
        # self.gentrys_quest_classic_data = metadata["Gentry's Quest Classic data"]
        # self.gentrys_quest_data = metadata["Gentry's Quest data"]

        # self.about = metadata["about me"]

        # self.perms = data["perms"]

    def change_username(self, new_username: str):
        self.username = new_username

    def jsonify(self):
        return {
            "username": self.username,
            "password": self.password,
            "pfp url": self.pfp,
            "id": self.id,
            "perms": self.perms,
            "metadata": {
                "osu id": self.osu_id,
                "Gentry's Quest data": self.gentrys_quest_data,
                "Gentry's Quest Classic data": self.gentrys_quest_classic_data,
                "about me": self.about
            }
        }
