import json
from crap.JsonHelper import JsonHelper
import os

if __name__ == "__main__":
    for account in os.listdir("accounts"):
        existing_data : dict = json.load(open(f"accounts/{account}", "r", encoding='utf-8'))
        dir_name = account[:-5]

        os.mkdir(f"accounts/{dir_name}")

        directory = f"accounts/{dir_name}"

        data = {
            'username': existing_data["username"],
            'password': existing_data["password"],
            'pfp url': existing_data["pfp url"],
            'id': existing_data["id"],
            'osu id': existing_data["metadata"]["osu id"],
            'perms': existing_data["perms"] if 'perms' in existing_data.keys() else [],
            'about me': existing_data["metadata"]["about me"]
        }
        json.dump(data, open(f"{directory}/account_data.json", "w+", encoding='utf-8'), indent=4)

        os.mkdir(f"{directory}/gentrys quest classic data")
        os.mkdir(f"{directory}/gentrys quest data")

        directory = f"{directory}/gentrys quest classic data"

        existing_data = existing_data["metadata"]["Gentry's Quest Classic data"]

        if existing_data:
            data = {
                'startup amount': existing_data["startupamount"],
                'settings': existing_data["settings"],
                'money': existing_data["inventory"]["money"]
            }
            json.dump(
                data,
                open(f"{directory}/data.json", "w+", encoding='utf-8'), indent=4
            )

            os.mkdir(f"{directory}/artifacts")
            x = 1
            for artifact in existing_data["inventory"]["artifacts"]:
                json.dump(artifact, open(f"{directory}/artifacts/{x}.json", "w+", encoding='utf-8'), indent=4)
                x += 1

            os.mkdir(f"{directory}/characters")
            x = 1
            for character in existing_data["inventory"]["characters"]:
                json.dump(character, open(f"{directory}/characters/{x}.json", "w+", encoding='utf-8'), indent=4)
                x += 1

            os.mkdir(f"{directory}/weapons")
            x = 1
            for weapon in existing_data["inventory"]["weapons"]:
                json.dump(weapon, open(f"{directory}/weapons/{x}.json", "w+", encoding='utf-8'), indent=4)
                x += 1

        os.remove(f"accounts/{account}")
