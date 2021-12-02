import json
import os
from crap import player_crap

def match_amount(currently_running=True, ended=True):
  '''
  shows the amount of matches
  
  :currently_running: boolean if false will not count for currently running matches
  :ended: boolean if false will not count for ended matches
  '''
  count = 0
  if currently_running == True:
    for match in os.listdir("matches/"):
      count+=1
  
  if ended == True:
    for match in os.listdir("matches/"):
      count+=1
  
  return(count)




class StartMatch:
  '''
  starts a match
  
  :team_mode: boolean, if True will tell it that its a team match
  :teams: int, will tell how many teams there are
  :match_name: string, will decide match name
  '''
  def __init__(self, team_mode=False, teams=0, match_name=f"match{match_amount()}"):
    
    if team_mode == True:
      teams = {}
      for i in range(teams):
        players = []
        team_name = input("give this team a name\n")
        while True:
          player_input = player_crap.player_list()
          if player_input == "done":
            break
          players.append(player_input)
        teams[f"{team_name}"] = players
    
    #match json file constructor from global match_start(mode) variables
    match_dict = {}
    match_dict["users"] = players_selected
    match_dict["match name"] = match_name
    match_dict["initial score"] = initial_score
    match_dict["initial playcount"] = initial_playcount
    match_dict["mode"] = mode
    match_dict["team metadata"] = teams
    match_dict["match score history"] = {}
    
    #put the values in the json file
    with open(f"matches/{match_name}.json", "w+") as joe:
      json.dump(match_dict, joe, indent = 4, sort_keys = False)
