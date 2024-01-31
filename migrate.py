import json
import os

if __name__ == "__main__":
    for account in os.listdir("accounts"):
        print(account)
        data : dict = json.load(open(f"accounts/{account}", "r", encoding="utf-8"))

        try:
            data["metadata"].pop("backrooms_data")
        except KeyError:
            data["metadata"].pop("backrooms data")

        json.dump(data, open(f"accounts/{account}", "w"), indent=4)
