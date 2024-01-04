import json
import os

from .Match import Match


class MatchHandler:
    def __init__(self):
        self.matches = []
        self.old_matches = []

    def load(self):
        for file in os.listdir("matches"):
            with open(file, "r") as f:
                match_data = json.loads(f.read())
                self.matches.append(Match(match_data, False))

        for file in os.listdir("match_history"):
            with open(file, "r") as f:
                match_data = json.loads(f.read())
                self.old_matches.append(Match(match_data, True))

    def unload(self):
        for match in self.matches:
            json.dump(match.jsonify(), open(f"matches/{match.name}", "w"))

    def end_match(self, match_name: str):
        for match in self.matches:
            if match.name == match_name:
                match.has_ended = True
                self.old_matches.append(match)
                self.matches.remove(match)
                json.dump(match.jsonify(), open(f"match_history/{match.name}", "w+"))


