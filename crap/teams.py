#team in a match class
class Teams:
  def __init__(self, team_name, match_data):
    self.team_name = team_name
    self.users = match_data["team metadata"][team_name]