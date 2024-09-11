import os
import time

import Client_Credentials


def initialize_files():
    print("\nInitializing files!\n")

    def verify_dir(dir_name: str):
        print(f"Verifying directory {dir_name} exists")
        if not os.path.isdir(dir_name):
            print("Creating directory")
            os.mkdir(dir_name)

    def verify_file(file_name: str):
        print(f"Verifying {file_name} exists")
        if not os.path.exists(file_name):
            print("Creating file")
            file = open(file_name, "w+")
            file.write("{}")
            file.close()


def retrieve_initialized_objects():
    pass


def gentrys_quest_handlers():
    pass
