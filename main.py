import os
from crap.team_crap import Teams

#packages
from flask import Flask, redirect, request, render_template
import math
import json
import time
import shutil
import asyncio
import datetime as dt

#osu packages
import Client_Credentials as client

#my packages
from crap import authentication_crap, match_crap, player_crap, function_crap, console_interface_crap

#flask set up
app = Flask(  # Create a flask app
  __name__,
  template_folder='templates', # Name of html file folder
  static_folder='static' # Name of directory for static files
)
    
#home website
@app.route('/')
async def home():
  return render_template("index.html")

#start console interface
@app.route("/start")
async def start():
  await console_interface_crap.main_process()
  return redirect(f"{client.public_url}/matches")

@app.route("/players")
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
    'players.html',  # Template file
    players = players_sorted
  )

@app.route("/matches/<match_name>")
async def match(match_name):

  players = {}

  print(match_name) 

  #match_name = urllib.parse.unquote(match_name)

  with open(f"matches/{match_name}") as joe:
    match_data = json.load(joe)

  with open("player_data.json", "r") as kfc:
    player_data = json.load(kfc)

  if match_data["mode"] == "ffa":
    
    score_data = match_data["match score history"]
      
    player_score_data = {}

    for id in match_data["users"]:

      player = player_crap.player_match_constructor(id, match_data)

      players[player[0]] = player[1]
      players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))
      player_score_data[player[0]] = player[1][0]

    score_data[f"{dt.date.today()}"] = dict(sorted(player_score_data.items()))

    match_data["match score history"] = score_data
    
    biggest_score_step1 = list(match_data["match score history"][f"{dt.date.today()}"].values())
    
    biggest_score = sorted(biggest_score_step1, reverse=True)[0]

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
    'Current.html',  # Template file
    #recent = player_recent,
    math = math,
    biggest_score = biggest_score,
    time = time,
    match_data = match_data,
    previous_score_segment = previous_score_segment,
    get_key_of = get_key_of,
    players = players_sorted
    #teamcount = teamcount
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
    teams_sorted = dict(sorted(teams.items(), key=lambda x: x[1], reverse=True))
    score_data[f"{dt.date.today()}"] = team_score_data
    match_data["match score history"] = score_data
    biggest_score_step1 = list(match_data["match score history"][f"{dt.date.today()}"].values())
    biggest_score = sorted(biggest_score_step1, reverse=True)[0]
    
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
      'Current.html',  # Template file
      #recent = player_recent
      time = time,
      match_data = match_data,
      teams = teams_sorted,
      previous_score_segment = previous_score_segment,
      get_key_of = get_key_of,
      biggest_score = biggest_score,
    )

#work on future old matches
@app.route("/matches/old/<match_name>")
def old_match(match_name):
  players = {}
  print(match_name)
  global match_data
  
  with open(f"match_history/{match_name}") as joe:
    match_data = json.load(joe)

  with open("player_data.json", "r") as kfc:
    player_data = json.load(kfc)

  if match_data["mode"] == "ffa":
    for user in match_data["users"]:
      user_pos = match_data["users"].index(user)
      playcount = match_data["final playcount"][user_pos] - match_data["initial playcount"][user_pos]
      playcount = ("{:,}".format(playcount))
      score = (match_data["final score"][user_pos] - match_data["initial score"][user_pos])
      score_formatted = ("{:,}".format(score))
      avatar = player_data[user][1]
      background = player_data[user][2]
      link = player_data[user][3]
      players[user] = [score, avatar, background, link, score_formatted, playcount]
      players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))
      
    return render_template(
    'old_match.html',  # Template file
    #recent = player_recent
    time = time,
    match_data = match_data,
    players = players_sorted
    )
    
  else:
    teams = {}
    def team_score(team):
      score_counting = 0
      counting_var = 0
      print("--------------")
      print("adding up team score...")
      for user in match_data["users"]:
        user_pos = match_data["users"].index(user)
        if user in match_data["team metadata"].get(team):
          #time.sleep(1)
          score_counting += match_data["final score"][user_pos] - match_data["initial score"][user_pos]
          #print(score)
        counting_var += 1
      return score_counting

    def team_players(team):

      players = {}

      for user in match_data["team metadata"][team]:

        user_pos = match_data["users"].index(user)

        playcount = match_data["final playcount"][user_pos] - match_data["initial playcount"][user_pos]

        playcount = ("{:,}".format(playcount))

        score = (match_data["final score"][user_pos] - match_data["initial score"][user_pos])

        score_formatted = ("{:,}".format(score))

        avatar = player_data[user][1]

        background = player_data[user][2]

        link = player_data[user][3]

        players[user] = [score, avatar, background, link, score_formatted, playcount]

        players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))

      return players_sorted

    for team in match_data["team metadata"].keys():

      team_data = Teams(team, match_data)
      
      team_users = team_data.users

      teams[team] = [team_score(team), team_players(team)]

      #print(f"users: {players.keys()}")

      print("===============")

      print(f"team users: {team_users}")

      time.sleep(0.3)

      print(f"team: {team}")

      time.sleep(0.3)

      print(f"team score: {teams[team][0]}")
      
      print("===============")
      
    teams_sorted = dict(sorted(teams.items(), key=lambda x: x[0], reverse=True))

    return render_template(
      'old_match.html',  # Template file
      #recent = player_recent
      time = time,
      match_data = match_data,
      teams = teams_sorted,
      players = {}
      #teamcount = teamcount
    )

@app.route("/matches")
async def matches():

  current_matches = []

  previous_matches = []

  for match in os.listdir("matches/"):
    current_matches.append(match)

  for match in os.listdir("match_history/"):
    previous_matches.append(match)
    

  return render_template(
    'matches.html',
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

  return redirect(f"{client.public_url}/matches")

@app.route("/control")
async def web_control():
  return render_template("control.html")

@app.route("/control/start_match")
async def web_control_start_match():
  return render_template("control/start_match.html", player_list = player_list, difficulty_list = difficulty_list)

@app.route('/control/start_match/', methods=['POST'])
def web_control_start_match_name():
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)

@app.route("/control/edit_match")
async def web_control_edit_match():
  return render_template("control/edit_match.html")

@app.route("/control/end_match")
async def web_control_end_match():
  return render_template("control/end_match.html")

@app.route("/control/refresh")
async def web_control_refresh():
  return render_template("control/refresh.html")

@app.route("/control/refresh/specific")
async def web_control_refresh_specific():
  return render_template("control/refresh/specific.html", player_list = player_list)

@app.route("/control/refresh/specific/match-specific")
async def web_control_refresh_specific_match():
  
  matches = []

  for match in os.listdir("matches/"):
    matches.append(match)
  
  return render_template("control/refresh/match_specific.html", matches = matches)

@app.route("/control/refresh/specific/<player>")
async def web_control_refresh_specific_player(player):
  return redirect(f"{client.public_url}/refresh/{player}")

@app.route("/control/refresh/specific/match-specific/<match>")
async def web_control_refresh_specific_match_refresh(match):
  
  with open(f"matches/{match}") as f:
    match_data = json.load(f)
  
  for user in match_data["users"]:
    await player_refresh(user)
  
  return redirect(f"{client.public_url}/control")

@app.route("/control/refresh/<player>")
async def web_control_refresh_player(player):
    return redirect(f"{client.public_url}/refresh/{player}")
  
@app.route("/info")
async def warning_info():
  return render_template("info.html")

@app.route("/client")
async def client_webpage():
  return render_template("client.html")

if __name__ == "__main__":  # Makes sure this is the main process
  app.run( # Starts the site
    host='0.0.0.0',  # Establishes the host, required for repl to detect the site
    port=80,# Randomly select the port the machine hosts on.
    debug=True,
    #ssl_context='adhoc'
  )
