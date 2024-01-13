import json
import os

from .Match import Match


class MatchHandler:
    def __init__(self):
        self.matches = []
        self.old_matches = []

    def load(self) -> None:
        print("Loading osu matches")

        for file in os.listdir("matches"):
            with open(file, "r") as f:
                match_data = json.loads(f.read())
                self.matches.append(Match(match_data, False))

        for file in os.listdir("match_history"):
            with open(file, "r") as f:
                match_data = json.loads(f.read())
                self.old_matches.append(Match(match_data, True))

    def unload(self) -> None:
        for match in self.matches:
            json.dump(match.jsonify(), open(f"matches/{match.name}", "w"))

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
                json.dump(match.jsonify(), open(f"match_history/{match.name}", "w+"))
