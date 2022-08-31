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
    for match in os.listdir("match_history/"):
      count+=1
  
  return(count)




async def start_match(team_mode=False, team_amount=2, match_name=(f"match{match_amount()}")):
  '''
  starts a match
  
  :team_mode: boolean, if True will tell it that its a team match
  :teams: int, will tell how many teams there are
  :match_name: string, will decide match name
  '''
  
  teams = {}
  
  if team_mode == True:
    mode = "teams"
    players_selected = []
    initial_score = []
    initial_playcount = []
    for i in range(team_amount):
      team_data = {}
      players = []
      team_name = input("give this team a name\n")
      team_color = input("give a hexcode or string color for this team?\n")
      team_data["team color"] = team_color
      while True:
        player_input = player_crap.player_list()
        if player_input == "done":
          break
        else:
          players.append(player_input)
          players_selected.append(player_input)
          initial_score.append(player_crap.user_data_grabber(id=player_input, specific_data=["score"])[0])
          initial_playcount.append(player_crap.user_data_grabber(id=player_input, specific_data=["playcount"])[0])
      team_data["players"] = players
      teams[f"{team_name}"] = team_data
  
  else:
    mode = "ffa"
    players_selected = []
    initial_score = []
    initial_playcount = []
    while True:
      player_input = player_crap.player_list()
      if player_input == "done":
        break
      else:
        players_selected.append(player_input)
        initial_score.append(player_crap.user_data_grabber(id=player_input, specific_data=["score"])[0])
        initial_playcount.append(player_crap.user_data_grabber(id=player_input, specific_data=["playcount"])[0])
  
  #match json file constructor from global match_start(mode) variables
  match_dict = {}
  match_dict["users"] = players_selected
  match_dict["match name"] = match_name
  match_dict["initial score"] = initial_score
  match_dict["initial playcount"] = initial_playcount
  match_dict["mode"] = mode
  match_dict["team metadata"] = teams
  match_dict["nicknames"] = {}
  
  #setting up stat gain graphs
  match_dict["graph data"] = {}
  match_dict["graph data"]["overall score"] = {}
  match_dict["graph data"]["daily stats"] = {}
  
  #put the values in the json file
  with open(f"matches/{match_name}.json", "w+") as joe:
    json.dump(match_dict, joe, indent = 4, sort_keys = False)
    



def get_match_data(match_name, match_open=True):
  if match_open == True:
    with open(f"matches/{match_name}") as f:
      match_data = json.load(f)
    return(match_data)
  else:
    with open(f"match_history/{match_name}") as f:
      match_data = json.load(f)
    return(match_data)