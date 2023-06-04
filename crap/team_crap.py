import json
import pathlib

from crap import player_crap

def team_score(match_name, team_name, old_match: bool):
  '''
  calculates team total score
  
  parameters:
  
  match_name : string
    the match name(needs to target a match)
    
  team_name : string
    the team name(needs to target a team)
  '''

  match_string = "match_history" if old_match else "matches"
  file_path = pathlib.Path().parent / match_string / match_name
  print(file_path)
  with file_path.open() as fh:
    match_data = json.load(fh)

  file_path = pathlib.Path().parent / "player_data.json"
  print(file_path)
  with file_path.open() as fh:
    player_data = json.load(fh)
    
  score = 0
  for user in match_data["team metadata"][team_name]["players"]:
    user_pos = match_data["users"].index(user)
    score += player_data[user]["user data"]["score"] - match_data["initial score"][user_pos]
  
  return score




def team_users(match_name, team_name, old_match: bool):
  '''
  constructs the user list of users in a team
  
  parameters:
  
  match_name : string
    the match name(needs to target a match)
    
  team_name : string
    the team name(needs to target a team)
  '''

  match_string = "match_history" if old_match else "matches"
  file_path = pathlib.Path().parent / match_string / match_name
  print(file_path)
  with file_path.open() as fh:
    match_data = json.load(fh)


    
  return match_data["team metadata"][team_name]["players"]




class Teams:
  '''
  constructs a team object to then be used in the website
  
  parameters:
  
  match_name : string
    the match name(it needs to target a match)
  '''
  def __init__(self, name, match_name, old_match: bool):
    match_string = "match_history" if old_match else "matches"
    file_path = pathlib.Path().parent / match_string / match_name
    print(file_path)
    with file_path.open() as fh:
      match_data = json.load(fh)
    self.score = team_score(match_name, name, old_match)
    self.users = team_users(match_name, name, old_match)