import json
import pathlib

from crap import player_crap

def team_score(match_name, team_name):
  '''
  calculates team total score
  
  parameters:
  
  match_name : string
    the match name(needs to target a match)
    
  team_name : string
    the team name(needs to target a team)
  '''

  file_path = pathlib.Path().parent / "matches" / match_name
  print(file_path)
  with file_path.open() as fh:
    match_data = json.load(fh)
    
  file_path = pathlib.Path().parent / "player_data.json"
  print(file_path)
  with file_path.open() as fh:
    player_data = json.load(fh)
    
  score = 0
  
  for user in match_data["team metadata"][team_name]:
    user_pos = match_data["users"].index(user)
    score += player_data[user]["user data"]["score"] - match_data["initial score"][user_pos]
  
  return score




def team_users(match_name, team_name):
  '''
  constructs the user list of users in a team
  
  parameters:
  
  match_name : string
    the match name(needs to target a match)
    
  team_name : string
    the team name(needs to target a team)
  '''
  
  players = {}
  
  file_path = pathlib.Path().parent / "matches" / match_name
  print(file_path)
  with file_path.open() as fh:
    match_data = json.load(fh)
  
  for user in match_data["team metadata"][team_name]:
    player = player_crap.player_match_constructor(user, match_data)
    players[player[0]] = player[1]
    
  players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))
    
  return players_sorted




class Teams:
  '''
  constructs a team object to then be used in the website
  
  parameters:
  
  match_name : string
    the match name(it needs to target a match)
  '''
  def __init__(self, name, match_name):
    file_path = pathlib.Path().parent / "matches" / match_name
    print(file_path)
    with file_path.open() as fh:
      match_data = json.load(fh)
    self.score = team_score(match_name, name)
    self.users = team_users(match_name, name)