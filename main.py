import os

from numpy import broadcast
from crap.team_crap import Teams

#packages
from flask import Flask, redirect, render_template, request
import math
import json
import time
import shutil
import asyncio
import datetime as dt
from tabulate import tabulate

#osu packages
import Client_Credentials as client

#my packages
from crap import authentication_crap, match_crap, player_crap, function_crap, console_interface_crap

live_player_status = {}

#flask set up
app = Flask(  # Create a flask app
  __name__,
  template_folder='templates', # Name of html file folder
  static_folder='static' # Name of directory for static files
)
app.config['SECRET_KEY'] = "hugandafortnite"

#player score grab api crap
@app.route("/api/grab/<ids>/<match_name>")
async def grabber(ids, match_name):
  id_list = ids.split("+")
  with open(f"matches/{match_name}.json") as f:
    match_data = json.load(f)
    
  new_dict = {}
  if match_data["mode"] == "ffa":
  
    for id in id_list:
      user_pos = match_data["users"].index(id)
      score = player_crap.user_data_grabber(id=f"{id}", specific_data=["score"])[0] - match_data["initial score"][user_pos]
      if id in live_player_status:
        new_dict[id] = {"score" : score,"liveStatus" : live_player_status[id]}
      else:
        new_dict[id] = {"score" : score,"liveStatus" : None}
  
  else:
    for id in id_list:
      user_pos = match_data["users"].index(id)
      score = player_crap.user_data_grabber(id=f"{id}", specific_data=["score"])[0] - match_data["initial score"][user_pos]
      for team in match_data["team metadata"]:
        if id in team:
          if id in live_player_status:
            new_dict[id] = {"score" : score,"liveStatus" : live_player_status[id], "team" : f"{team}"}
          else:
            new_dict[id] = {"score" : score,"liveStatus" : None, "team" : f"{team}"}
    

  return new_dict

@app.route("/testing")
def testing():
  with open("matches/osu valley 2021-2022.json") as f:
    match_data = json.load(f)
  
  return(match_data["nicknames"][str(11339405)])

 
#api for refresh client
#match grabber
@app.route('/api/matches/<time>')
def api_match_request(time):
  returns = {}
  returns["matches"] = []
  if time == "current":
    for match in os.listdir("matches/"):
      returns["matches"].append(match)
    return returns
  else:
    for match in os.listdir("match_history/"):
      returns["matches"].append(match)
    return returns

#match data grabber
@app.route('/api/match-get/<time>/<match>')
def match_get(time, match):
  with open("player_data.json") as f:
    player_data = json.load(f)
  if time == "current":
    with open(f"matches/{match}") as f:
      match_data = json.load(f)
      
    table = {}
    table["rank"] = []
    table["players"] = []
    table["score"] = []
    table["playcount"] = []
    
    players = {}
    
    for user in match_data["users"]:
      player = player_crap.player_match_constructor(user, match_data)

      players[player[1][19]] = player[1]
      
    players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))
    
    x = 1
    
    for key in players_sorted.keys():
      user_pos = match_data["users"].index(str(key))
      player_thing = player_crap.user_data_grabber(id=key, specific_data=["name", "score", "playcount"])
      table["rank"].append(f"#{x}")
      table["players"].append(player_thing[0])
      table["score"].append("{:,}".format(player_thing[1] - match_data["initial score"][user_pos]))
      table["playcount"].append("{:,}".format(player_thing[2] - match_data["initial playcount"][user_pos]))
      x += 1
    
    print("\n", match_data["match name"])
    print(tabulate(table, headers="keys", tablefmt="fancy_grid"))
    return(table)
  else:
    return None
  
#get delay api
@app.route("/api/get-delay")
async def get_delay():
  return(str(len(live_player_status.items()) / 2))

#live status api
@app.route("/api/live/del/<id>", methods=["post"])
async def del_live_status(id):
  global live_player_status
  live_player_status.pop(id)
  return({})

@app.route("/api/live/get/<id>", methods=["get"])
async def get_live_status(id):
  player_info = live_player_status[id]
  return(player_info)

@app.route("/api/live/update/<id>", methods=["post"])
async def update_live_status(id):
  global live_player_status
  info = request.json
  live_player_status[id] = info
  return({})

#home website
@app.route('/')
async def home():
  return render_template("index.html")

#home osu website
@app.route('/osu')
async def osu_home():
  return render_template("osu/index.html")

#start console interface
@app.route("/start")
async def start():
  await console_interface_crap.main_process()
  return redirect(f"{client.public_url}/matches")

@app.route("/osu/players")
async def players():

  players_dict = {}
  
  with open("player_data.json") as f:
    player_data = json.load(f)
    
  for id in player_data.keys():

    name = player_data[id]["user data"]["name"]
    score = player_data[id]["user data"]["score"]
    avatar = player_data[id]["user data"]["avatar url"]
    background = player_data[id]["user data"]["background url"]
    profile_link = player_data[id]["user data"]["profile url"]
    tags = player_data[id]["user tags"]
    playcount = player_data[id]["user data"]["playcount"]
    playcount = ("{:,}".format(playcount))
    score_formatted = ("{:,}".format(score))
      
    players_dict[name] = [score, avatar, background, profile_link, tags, playcount, score_formatted]

    players_sorted = dict(sorted(players_dict.items(), key=lambda x: x[1], reverse=True))

  return render_template(
    'osu/players.html',  # Template file
    players = players_sorted
  )

@app.route("/osu/matches/<match_name>/<graph_view>")
async def match(match_name, graph_view):

  players = {}

  print(match_name) 

  #match_name = urllib.parse.unquote(match_name)

  with open(f"matches/{match_name}") as joe:
    match_data = json.load(joe)

  with open("player_data.json", "r") as kfc:
    player_data = json.load(kfc)

  if match_data["mode"] == "ffa":
    player_score_data = {}
    
    for id in match_data["users"]:

      player = player_crap.player_match_constructor(id, match_data)

      players[player[0]] = player[1]
      #players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))
      player_score_data[player[0]] = player[1][0]
    
    '''#normal graph data updater
    score_data = match_data["match score history"]["overall score"]
    score_data[f"{dt.date.today()}"] = dict(sorted(player_score_data.items()))
    match_data["match score history"]["overall score"] = score_data
    
    #daily score graph data updater
    score_data = match_data["match score history"]["daily score"]
    player_score_data = {}
    
    dates = list(match_data["match score history"]["overall score"].keys())
    for user in match_data["match score history"]["overall score"][dates[-1]]:
      player_score_data[user] = match_data["match score history"]["overall score"][dates[len(dates) - 1]][user] - match_data["match score history"]["overall score"][dates[len(dates) - 2]][user]
      score_data[f"{dt.date.today()}"] = player_score_data
      match_data["match score history"]["daily score"] = score_data
      
    
    if graph_view == "normal":
      biggest_score_step1 = list(match_data["match score history"]["overall score"][f"{dt.date.today()}"].values())
      biggest_score = sorted(biggest_score_step1, reverse=True)[0]
    elif graph_view == "daily-score-gain":
      biggest_score_step1 = list(match_data["match score history"]["daily score"][f"{dt.date.today()}"].values())
      biggest_score = sorted(biggest_score_step1, reverse=True)[0]
    else:
      biggest_score_step1 = list(match_data["match score history"]["daily playcount"][f"{dt.date.today()}"].values())
      biggest_score = sorted(biggest_score_step1, reverse=True)[0]'''

    with open(f"matches/{match_name}", "w") as file:
        json.dump(match_data, file, indent = 4, sort_keys = False)

    with open(f"matches/{match_name}", "r") as file:
      match_data = json.load(file)
      
    def get_key_of(score, dict):
        for key, value in dict.items():
            if score == value:
                return key
      
    def previous_score_segment(playername, iteration):
      dates = []
      
      if graph_view == "normal":
        for date in match_data["match score history"]["overall score"]:
          dates.append(date)
      elif graph_view == "daily-score-gain":
        for date in match_data["match score history"]["daily score"]:
          dates.append(date)
      else:
        for date in match_data["match score history"]["daily playcount"]:
          dates.append(date)
        
      if iteration <= 1:
        return 0
      
      elif iteration > 1:
        if graph_view == "normal":
          return match_data["match score history"]["overall score"][dates[iteration - 2]][playername]
        elif graph_view == "daily-score-gain":
          try:
            return match_data["match score history"]["daily score"][dates[iteration - 2]][playername]
          except:
            return 0
        else:
          return match_data["match score history"]["daily playcount"][dates[iteration - 2]][playername]
          

    return render_template(
    'osu/Current.html',  # Template file
    #recent = player_recent,
    math = math,
    #biggest_score = biggest_score,
    time = time,
    match_data = match_data,
    previous_score_segment = previous_score_segment,
    get_key_of = get_key_of,
    #players = players_sorted,
    players = players,
    match_name = match_name,
    graph_view = graph_view,
    get_data = player_crap.user_data_grabber,
    live_status = live_player_status
  )
    
  else:
    teams = {}
    score_data = match_data["match score history"]
    team_score_data = {}
    
    for team in match_data["team metadata"]:
      new_team = Teams(team, match_name)
      teams[team] = [("{:,}".format(new_team.score)), new_team.users]
      team_score_data[team] = ("{:,}".format(new_team.score))

    score_data[f"{dt.date.today()}"] = dict(sorted(team_score_data.items()))
    score_data[f"{dt.date.today()}"] = team_score_data
    match_data["match score history"] = score_data
    biggest_score_step1 = list(match_data["match score history"][f"{dt.date.today()}"].values())
    biggest_score = sorted(biggest_score_step1, reverse=False)[0]
    
    if biggest_score == 0:
      biggest_score = 1

    with open(f"matches/{match_name}", "w") as file:
        json.dump(match_data, file, indent = 4, sort_keys = False)

    with open(f"matches/{match_name}", "r") as file:
      match_data = json.load(file)  
      
    def get_key_of(score, dict):
        for key, value in dict.items():
            if score == value:
                return key
      
    def previous_score_segment(playername, iteration):
      dates = []
      
      for date in match_data["match score history"]:
        dates.append(date)
        
      if iteration <= 1:
        return 0
      
      elif iteration > 1:
        return match_data["match score history"][dates[iteration - 2]][playername]

    return render_template(
      'osu/Current.html',  # Template file
      time = time,
      match_data = match_data,
      teams = teams,
      previous_score_segment = previous_score_segment,
      get_key_of = get_key_of,
      biggest_score = biggest_score,
      get_data = player_crap.user_data_grabber
    )

#work on future old matches
@app.route("/osu/matches/old/<match_name>")
def old_match(match_name):
  players = {}
  print(match_name)
  global match_data
  
  with open(f"match_history/{match_name}") as joe:
    match_data = json.load(joe)

  with open("player_data.json", "r") as kfc:
    player_data = json.load(kfc)

  if match_data["mode"] == "ffa":
    for id in match_data["users"]:
      player = player_crap.player_match_constructor(id, match_data)
      players[player[0]] = player[1]
      players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))
  
    return render_template(
    'osu/old_match.html',  # Template file
    #recent = player_recent
    time = time,
    match_data = match_data,
    players = players_sorted,
    get_data = player_crap.user_data_grabber
    )
    
  else:
    teams = {}
    score_data = match_data["match score history"]
    team_score_data = {}
    
    for team in match_data["team metadata"]:
      new_team = Teams(team, match_name)
      teams[team] = [new_team.score, new_team.users]
      team_score_data[team] = new_team.score

    score_data[f"{dt.date.today()}"] = dict(sorted(team_score_data.items()))
    teams_sorted = dict(sorted(teams.items(), key=lambda x: x[0], reverse=True))
    score_data[f"{dt.date.today()}"] = team_score_data
    match_data["match score history"] = score_data

    return render_template(
      'Current.html',  # Template file
      #recent = player_recent
      time = time,
      match_data = match_data,
      teams = teams_sorted,
      get_data = player_crap.user_data_grabber
    )
   
@app.route("/osu/matches")
async def matches():

  current_matches = []

  previous_matches = []

  for match in os.listdir("matches/"):
    current_matches.append(match)

  for match in os.listdir("match_history/"):
    previous_matches.append(match)
    

  return render_template(
    'osu/matches.html',
    match_data = match_crap.get_match_data,
    player_data = player_crap.user_data_grabber,
    random_number = function_crap.randnum,
    current_matches = current_matches,
    previous_matches = previous_matches
  )

@app.route("/refresh/<player_name>")
async def web_player_refresh(player_name):
  if player_name == "all":
    await player_crap.refresh_all_players()
  else:
    try:
      int(player_name) + 0
    except:
      player_name = player_crap.user_data_grabber(name=f"{player_name}", specific_data=["id"])[0]
    
    await player_crap.player_refresh(player_name)

  return redirect(f"{client.public_url}/osu/matches")

#tests
@app.route("/tests/<test_num>")
async def tests(test_num):
  return render_template(
    f"tests/{test_num}.html",
    test_num = test_num
  )
  
@app.route("/tests/create")
async def test_create():
  test_new_id = len(os.listdir("templates/tests"))
  template = open("templates/tests/test-template.html", "r")
  f = open(f"templates/tests/test{test_new_id}.html", "w+")
  for line in template:
    f.write(line)
  f.close()
  return render_template(f"tests/test{test_new_id}.html")

#website control
@app.route("/control")
async def web_control():
  return render_template("control.html")
  
@app.route("/osu/info")
async def warning_info():
  return render_template("info.html")

@app.route("/osu/client")
async def client_webpage():
  return render_template("osu/client.html")

@app.route("/minecraft")
async def minecraft():
  return render_template("minecraft/index.html")

if __name__ == "__main__":  # Makes sure this is the main process
  app.run(
    host='0.0.0.0',  # Establishes the host, required for repl to detect the site
    port=80,# Randomly select the port the machine hosts on.
    debug=True)
