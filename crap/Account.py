import json


class Account:
    def __init__(self, id):
        print(f"Loading {id}")

        self.id = id

        data = json.load(open(f"accounts/{id}.json", "r"))

        self.username = data["username"]
        self.password = data["password"]
        self.pfp = data["pfp url"]

        metadata = data["metadata"]

        self.osu_id = metadata["osu id"]
        self.gentrys_quest_classic_data = metadata["Gentry's Quest Classic data"]
        self.gentrys_quest_data = metadata["Gentry's Quest data"]
        self.backrooms_data = metadata["backrooms_data"]

        self.about = metadata["about me"]
