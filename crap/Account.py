import json


class Account:
    def __init__(self, id):
        print(f"Loading account: {id}")

        self.id = id

        data = json.load(open(f"accounts/{id}.json", "r"))

        self.username = data["username"]
        self.password = data["password"]
        self.pfp = data["pfp url"]

        metadata = data["metadata"]

        self.osu_id = metadata["osu id"]
        self.gentrys_quest_classic_data = metadata["Gentry's Quest Classic data"]
        self.gentrys_quest_data = metadata["Gentry's Quest data"]

        self.about = metadata["about me"]

        self.perms = data["perms"]

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
