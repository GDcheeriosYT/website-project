import json
import os
import time

import Client_Credentials

from .Match import Match


class MatchHandler:
    def __init__(self):
        self.matches = []
        self.old_matches = []

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
