import os


def initialize_files():
    print("Initializing files!")

    def verify_dir(dir_name: str):
        if not os.path.isdir(dir_name):
            os.mkdir("matches")

    def verify_file(file_name: str):
        if not os.path.exists(file_name):
            file = open(file_name, "w+")
            file.write("{}")
            file.close()

    verify_dir("matches")
    verify_dir("match_history")
    verify_file("player_data.json")
    verify_file("tokens.txt")


def retrieve_initialized_objects():
    pass


def gentrys_quest_handlers():
    pass
