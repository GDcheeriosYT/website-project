import json
import os
import time

import Client_Credentials

from .Match import Match


class MatchHandler:
    def __init__(self):
        self.matches = []
        self.old_matches = []

    def load(self) -> None:
        print("\nLoading osu matches\n")

        for file in os.listdir("matches"):
            with open(f"matches/{file}", "r") as f:
                match_data = json.loads(f.read())
                self.matches.append(Match(match_data, False))

        for file in os.listdir("match_history"):
            with open(f"match_history/{file}", "r") as f:
                match_data = json.loads(f.read())
                self.old_matches.append(Match(match_data, True))

    def unload(self) -> None:
        def write_to_file(json_object, file):
            json.dump(json_object, file, indent=4)

        for match in self.matches:
            write_to_file(match.jsonify(), open(f"matches/{match.name}.json", "w"))

    def get_match(self, match_name) -> Match:
        for match in self.matches:
            if match.name == match_name:
                return match

        for match in self.old_matches:
            if match_name == match.name:
                return match

    def end_match(self, match_name: str) -> None:
        for match in self.matches:
            if match.name == match_name:
                match.has_ended = True
                self.old_matches.append(match)
                self.matches.remove(match)
                json.dump(match.jsonify(), open(f"match_history/{match.name}.json", "w+"), indent=4)
