import json
import os

if __name__ == "__main__":
    for account in os.listdir("accounts"):
        print(account)
        data : dict = json.load(open(f"accounts/{account}", "r", encoding="utf-8"))

        data["Perms"] = []
        json.dump(data, open(f"accounts/{account}", "w", encoding="utf-8"), indent=4)
