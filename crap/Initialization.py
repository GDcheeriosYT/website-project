import os
import time

import Client_Credentials


def initialize_files():
    print("\nInitializing files!\n")
    time.sleep(Client_Credentials.section_load_time)

    def verify_dir(dir_name: str):
        print(f"Verifying directory {dir_name} exists")
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

    def verify_file(file_name: str):
        print(f"Verifying {file_name} exists")
        if not os.path.exists(file_name):
            file = open(file_name, "w+")
            file.write("{}")
            file.close()

    verify_dir("accounts")
    verify_dir("matches")
    verify_dir("match_history")
    verify_dir("backups")
    verify_file("player_data.json")


def retrieve_initialized_objects():
    pass


def gentrys_quest_handlers():
    pass
