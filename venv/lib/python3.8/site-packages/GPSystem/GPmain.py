from .GPRater import GPRater


class GPSystem:
    rater = GPRater()
    version = "1.0"

    def __init__(self):
        print("You're using GPSystem version ", GPSystem.version)


if __name__ == '__main__':
    import os
    import json
    from tabulate import tabulate
    table_style = "pipe"
    file_path = "GPSystem/Data"
    program = GPSystem()
    if os.path.isdir(file_path):
        pass
    else:
        os.mkdir(file_path)

    if len(os.listdir(file_path)) == 0:
        print("you have no users in the data directory...")
    else:
        characters = []
        print("rating characters...")
        for file in os.listdir(file_path):
            character_name = file[:-5]
            print(f"rating {character_name}")

            with open(f"{file_path}/{file}", "r") as f:
                character_data = json.loads(f.read())

            characters.append([character_name, program.rater.generate_power_details(character_data)])

        def table_data_maker(character_data: list, rank: int) -> list:
            return [rank, character_data[0], character_data[1]["rating"]["weighted"], character[1]["rating"]["unweighted"]]


        while True:
            print(f"\n GP version {program.rater.version}\n")
            headers = ["rank", "player", "weighted gp", "unweighted gp"]

            table = []

            characters.sort(key=lambda x: x[1]["rating"]["weighted"], reverse=True)
            rank_counter = 1
            for character in characters:
                table.append(table_data_maker(character, rank_counter))
                rank_counter += 1


            print(tabulate(table, headers=headers, tablefmt=table_style))

            option = int(input("\nview info about player (select rank)\n"))

            character = characters[option - 1]
            while True:
                print("")
                print(character[0])
                print(f"weighted gp: {character[1]['rating']['weighted']}")
                print(f"unweighted gp: {character[1]['rating']['unweighted']}\n")

                option = int(input("1. view section overview\n"
                                   "2. view json\n"
                                   "3. back\n"))

                if option == 1:
                    headers = ["section number", "section type", "weighted gp", "unweighted gp"]
                    characters = character[1]["totals"]["characters"]
                    artifacts = character[1]["totals"]["artifacts"]
                    weapons = character[1]["totals"]["weapons"]
                    table = [
                        [
                            1,
                            "characters",
                            characters["weighted"],
                            characters["unweighted"]
                        ],
                        [
                            2,
                            "artifacts",
                            artifacts["weighted"],
                            artifacts["unweighted"]
                        ],
                        [
                            3,
                            "weapons",
                            weapons["weighted"],
                            weapons["unweighted"]
                        ]
                    ]
                    print(tabulate(table, headers=headers, tablefmt=table_style))
                elif option == 2:
                    print(json.dumps(character[1], indent=4))
                else:
                    break