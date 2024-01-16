import json
import os

if __name__ == "main":
    for account in os.listdir("accounts"):
        print(account)
        data = json.load(open(f"accounts/{account}", "r", encoding="utf-8"))

        data["metadata"]["Gentry's Quest Classic data"] = data["metadata"]["Gentry's Quest data"]
        data["metadata"]["Gentry's Quest data"] = None

        json.dump(data, open(f"accounts/{account}", "w"), indent=4)
