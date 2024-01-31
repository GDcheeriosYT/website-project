# packages
from crap.ServerData import ServerData

from .authentication_crap import *


# user crap class
class Player:

    def __init__(self, id):
        self.id = id

        if str(id) in ServerData.osu_player_json.keys():
            player_data = ServerData.osu_player_json[str(id)]
            self.name = player_data["user data"]["name"]
            self.rank = player_data["user data"]["rank"]
            self.play_count = player_data["user data"]["playcount"]
            self.score = player_data["user data"]["score"]
            self.avatar = player_data["user data"]["avatar url"]
            self.background = player_data["user data"]["background url"]
            self.link = player_data["user data"]["profile url"]
            self.accuracy = player_data["user data"]["accuracy"]
        else:
            self.update_data()

    def update_data(self):
        try:
            data = requests.get(
                f"https://osu.ppy.sh/api/v2/users/{self.id}/osu",
                headers={"Authorization": f'Bearer {check_access()}'}
            ).json()

            self.name = data['username']

            if data['statistics']['global_rank'] is not None:
                self.rank = data['statistics']['global_rank']
            else:
                self.rank = 999999999

            self.play_count = data['statistics']['play_count']
            self.score = data["statistics"]["total_score"]
            self.accuracy = data["statistics"]["hit_accuracy"]
            self.avatar = data['avatar_url']
            self.background = data['cover_url']
            self.link = f"https://osu.ppy.sh/users/{self.id}"
        except Exception as e:
            self.name = "Unknown"
            self.rank = 999999999
            self.play_count = 0
            self.score = 0
            self.avatar = "https://data.whicdn.com/images/100018401/original.gif"
            self.background = "https://data.whicdn.com/images/100018401/original.gif"
            self.link = None
            self.accuracy = 0

    def jsonify(self):
        return {
            f"{self.id}": {
                "user data": {
                    "name": self.name,
                    "rank": self.rank,
                    "score": self.score,
                    "playcount": self.play_count,
                    "avatar url": self.avatar,
                    "background url": self.background,
                    "profile url": self.link,
                    "accuracy": self.accuracy
                }
            }
        }
