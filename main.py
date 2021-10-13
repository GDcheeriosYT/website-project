import os  #making sure pip is always up to date
from os import system
import os

#system('pip install --upgrade pip')
#system('')

#securing
secret = "8Bb9FnS8pvjZcRXbMd3HXrbvRq1n9u9b3e454XcM"
api_key = "952f25aee05178bd249c6781a88e98a098afa08b"
extra_api_key = "6a5de2f4b1a29f26710a2a48759c463f9bef68e2"
public_url = "http://localhost"
client_id = "9545"
map_url = "1563044"

#packages
import requests
import aiohttp
import asyncio
import slider
import numpy
import scipy
import re
from flask import Flask, redirect, url_for, request, render_template
from threading import Timer
import math
import match_data
import importlib
import lxml
from lxml import html
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
teamFile = open("team_metadata.py", "a+")
teamFile.close()
import team_metadata
from dataclasses import dataclass
from typing import List
from collections import OrderedDict
import json
import time
import sqlite3

difficulty_list = ["beginner", "easy", "normal", "medium", "hard", "insane"]

difficulty_amount = len(difficulty_list)

global mode

#leveling_system
def levels_creation(difficulty):
  level_limit = 300

  global levels

  levels = []

  print("grabbing level difficulty configuration...\n")

  if difficulty == difficulty_list[0]:
    level_expenential_growth_modifier = 1.00
    leveling_start = 50000
    level_number_change = 100000
    exponential_change = 0.03

  elif difficulty == difficulty_list[1]:
    level_expenential_growth_modifier = 1.00
    leveling_start = 100000
    level_number_change = 250000
    exponential_change = 0.04

  elif difficulty == difficulty_list[2]:
    level_expenential_growth_modifier = 1.00
    leveling_start = 100000
    level_number_change = 250000
    exponential_change = 0.07

  elif difficulty == difficulty_list[3]:
    level_expenential_growth_modifier = 1.00
    leveling_start = 500000
    level_number_change = 1000000
    exponential_change = 0.04

  elif difficulty == difficulty_list[4]:
    level_expenential_growth_modifier = 1.00
    leveling_start = 1000000
    level_number_change = 2000000
    exponential_change = 0.04

  elif difficulty == difficulty_list[5]:
    level_expenential_growth_modifier = 1.00
    leveling_start = 1000000
    level_number_change = 2500000
    exponential_change = 0.07

  x = 1

  while x <= level_limit:

    levels.append(leveling_start)

    #time.sleep(0.1)

    x = x + 1
    leveling_start = int(leveling_start + level_number_change * level_expenential_growth_modifier)
    
    level_expenential_growth_modifier = level_expenential_growth_modifier + level_expenential_growth_modifier * exponential_change

x = 1

'''for level in levels:
  print(f"level {x} {level}")
  x = x + 1'''

api_info = slider.client.Client("", str(api_key), api_url='https://osu.ppy.sh/api')

api_info_scoreboard = slider.client.Client("", str(extra_api_key),api_url='https://osu.ppy.sh/api')

#classes
#making the library
slider.library.Library("")


#team class
class clans:
  def __init__(self, name, score, accuracy):

    self.name = name

    self.score = score

    self.accuracy = accuracy


#team in a match class
class Teams:
  def __init__(self, team_name):

    self.team_name = team_name

    self.users = match_data.team_metadata[team_name]


#user block class
class user_block:
  def __init__(self, name):

    self.name = name

    self.request_profile = requests.get(f"https://osu.ppy.sh/api/v2/users/{self.name}/osu", headers = {"Authorization": f'Bearer {access_token}'}).json()

    try:
      self.id = self.request_profile['id']
    except KeyError:
      self.id = "unknown"
      self.name = (f"{name} (BANNED)")
      self.play_count = 0
      self.score = 0
      self.avatar = "https://data.whicdn.com/images/100018401/original.gif"
      self.background = "https://data.whicdn.com/images/100018401/original.gif"
      self.link = "https://data.whicdn.com/images/100018401/original.gif"
      self.recent_score = 0
      self.map_cover = "https://data.whicdn.com/images/100018401/original.gif"
      self.map_url = "https://data.whicdn.com/images/100018401/original.gif"
      self.map_difficulty = 0
      self.mods = "unknown"
      self.map_title = "unknown"
      self.artist = "unknown"
      self.accuracy = 0
      self.max_combo = 0
      self.rank = "F"
      self.rank_color = "red"
      return None

    self.play_count = self.request_profile['statistics']['play_count']

    self.request_scores = requests.get(f"https://osu.ppy.sh/api/v2/users/{self.id}/scores/recent", params = {"include_fails": "0", "mode": "osu", "limit": "1", "offset": "0"}, headers = {"Authorization": f'Bearer {access_token}'})

    #self.weekly_map_score_get = requests.get(f"https://osu.ppy.sh/api/v2/beatmaps/{map_url}/scores/users/{self.id}", params = {"mode":"osu"}, headers = {"Authorization": f'Bearer {access_token}'}).json()

    #self.weekly_map_score = self.weekly_map_score_get["score"]

    #print(self.weekly_map_score_get)
 
    self.score = self.request_profile["statistics"]["total_score"]

    self.avatar = self.request_profile['avatar_url']
    
    self.background = self.request_profile['cover_url']

    self.link = (f"https://osu.ppy.sh/users/{self.id}")

    #print(json.loads(self.request_scores.text))
    
    try:
      self.recent_score = (json.loads(self.request_scores.text)[0]["score"])
    except IndexError:
      self.recent_score = 0

    try:
      self.map_cover = (json.loads(self.request_scores.text)[0]["beatmap"]["beatmapset_id"])
      self.map_cover = f"https://assets.ppy.sh/beatmaps/{self.map_cover}/covers/cover.jpg"
    except IndexError:
      self.map_cover = "https://data.whicdn.com/images/100018401/original.gif"

    try:
      self.map_url = (json.loads(self.request_scores.text)[0]["beatmap"]["url"])
    except IndexError:
      self.map_url = "https://osu.ppy.sh/beatmapsets"

    try:
      self.map_difficulty = (json.loads(self.request_scores.text)[0]["beatmap"]["difficulty_rating"])
    except IndexError:
      self.map_difficulty = "0"

    try:
      self.map_title = (json.loads(self.request_scores.text)[0]["beatmapset"]["title_unicode"])
    except IndexError:
      self.map_title = "not found"

    try:
      self.mods = (json.loads(self.request_scores.text)[0]["mods"])
      if len(self.mods) == 0:
        self.mods = "no mods"
      else:
        self.mods = self.mods
    except IndexError:
      self.mods = ""

    try:
      self.artist = (json.loads(self.request_scores.text)[0]["beatmapset"]["artist_unicode"])
    except IndexError:
      self.artist = ""

    try:
      self.accuracy = (json.loads(self.request_scores.text)[0]["accuracy"])
      self.accuracy = round(self.accuracy * 100, 2)
    except IndexError:
      self.accuracy = ""

    try:
      self.max_combo = (json.loads(self.request_scores.text)[0]["max_combo"])
    except IndexError:
      self.max_combo = ""

    try:
      self.rank = (json.loads(self.request_scores.text)[0]["rank"])
      if self.rank == "XH":
        self.rank = "SS+"
        self.rank_color = "grey"
      elif self.rank == "SH":
        self.rank = "S+"
        self.rank_color = "grey"
      elif self.rank == "S":
        self.rank_color = "yellow"
      elif self.rank == "X":
        self.rank = "SS"
        self.rank_color = "yellow"
      elif self.rank == "A":
        self.rank_color = "green"
      elif self.rank == "B":
        self.rank_color = "blue"
      elif self.rank == "C":
        self.rank_color = "purple"
      elif self.rank == "D":
        self.rank_color = "red"
    except IndexError:
      self.rank = "F"
      self.rank_color = "red"

with open("players.db", "r") as f:

  player_list = f.read().splitlines()

def level_difficulty_selector():

  x = 0

  while x < difficulty_amount:

    print(f"{x} {difficulty_list[x]}")

    x += 1

  while True:
  
    selection = int(input("what level difficulty would you like?"))

    try:
      selection + 0
    except ValueError:
      print("number please!")
    
    if selection > difficulty_amount:
      print("too big!")

    elif selection < 0:
      print("too small!")
    
    else:
      return(difficulty_list[selection])

  

def match_start(mode):

  #the variable which will show which mode it is
  global game_mode

  game_mode = mode

  #a list of all the players playing
  global players_selected

  players_selected = []

  #will check to see if teams or ffa is wanted
  if mode == ("teams"):

    #team mode setup
    global teams

    teams = {}

    '''global teams_score

    teams_score = {}'''
    
    #create teams
    print("\ncreate a team by typing a name\n")

    x = 0

    is_creating = True

    while is_creating == True:

      team_players = []

      team_player_score = []

      team_name = input("team name:\n")

      if team_name == "done":
        break

      #pick players
      while True:

        x = 0
        
        #display player list
        while x < len(player_list):

          print("\n", x, player_list[x])

          x = x + 1

        try:
          player_selector = int(input(""))
        except ValueError:
          break

        if player_list[player_selector] not in players_selected:

          players_selected.append(player_list[player_selector])

        if player_list[player_selector] not in team_players:

          team_players.append(f"{player_list[player_selector]}")

          team_player_score.append(f"{api_info.user(user_name=player_list[player_selector]).total_score}")

      teams[team_name] = team_players

      #teams_score[team_name] = team_player_score
      

  else:

    while True:

      teams = {}

      x = 0

      print("\nwho would you like to add to this match?\ntype done to accept players")

      while x < len(player_list):

        print(x, player_list[x])

        x = x + 1

      pick_user = input("")

      if str(pick_user) == "done":

        break

      elif int(pick_user) > len(player_list):

        print("\ntoo big!\n")

      elif int(pick_user) < len(player_list) - len(player_list):

        print("\ntoo small!\n")

      else:

        if player_list[int(pick_user)] not in players_selected:

          players_selected.append(player_list[int(pick_user)])

          print(player_list[int(pick_user)], "has been added to the list!\n")

          print("debug:", players_selected)

        else:
          print("this character is already selected!\n")

          print("current list of players:", players_selected)

  global initial_score

  initial_score = []

  global initial_playcount

  initial_playcount = []

  for player in players_selected:

    initial_playcount.append(api_info.user(user_name=str(player)).play_count)

    initial_score.append(api_info.user(user_name=str(player)).total_score)


new_game = str(input("start new game?\ny/n\n"))

if new_game == "y":

  f = open("match_data.py", "w+")

  match_name = input("match name ")

  game_mode = str(input("teams or free for all\n1.teams\n2.free for all\n"))

  if game_mode == ("1"):

    mode = "teams"

    match_start(mode)

  else:

    mode = "ffa"

    match_start(mode)
  
  f.write(f"users = {players_selected}\nmatch_name = \"{match_name}\"\ninitial_score = {initial_score}\ninitial_playcount = {initial_playcount}\nmode = \"{mode}\"\nteam_metadata = {teams}\nlevel_difficulty = \"{level_difficulty_selector()}\"")

  f.close()

elif new_game == "n":
  mode = match_data.mode
  print("alright continuing the game")
  #joe = user_block("btmc")
  #print(joe.background)
  
else:
  print("...")

#list variable to store which players are participating in the current match
players_in_match = []


def user_list():
  with open("players.db", "r") as f:
    player_list = f.read().splitlines()

#making the api ['connector

extra_api_key = str(extra_api_key)

get_the_key = f"https://osu.ppy.sh/oauth/authorize/client_id={client_id}&redirect_uri={public_url}"

#flask set up
app = Flask(  # Create a flask app
  __name__,
  template_folder='templates',  # Name of html file folder
  static_folder='static'  # Name of directory for static files
)

@app.route('/')
def home():
  return render_template(
    'index.html',  # Template file
  )


@app.route('/code_grab')
def code_grab() :

  code = request.query_string

  name_verify = str(code).split('code=')[1]
  name_verify = re.search(r"\w+", name_verify)
  #print(name_verify.group())
  
  '''random_file = open("code.txt", "w+")
  random_file.write(name_verify.group())
  random_file.close()'''

  response = requests.post("https://osu.ppy.sh/oauth/token", json = { 'client_id':int(client_id), 'client_secret':secret, 'grant_type':'client_credentials', 'scope':'public'}, headers={'Accept':'application/json', 'Content-Type':'application/json'})

  token_thing = response.json()

  global access_token

  access_token = token_thing["access_token"]

  test_user_thing = user_block("GDcheerios")

  #f = open("debug.txt", "w")
  #f.write(f"{access_token}")
  #f.close

  #print(test_user_thing.request_profile)

  #print(test_user_thing.request_scores)

  return redirect(f"{public_url}/refresh")

@app.route("/login.html",methods = ['POST', 'GET'])

def login():

  return redirect(f"https://osu.ppy.sh/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={public_url}/code_grab&scope=public")

@app.route("/refresh")
def refresh():

  levels_creation(match_data.level_difficulty)

  players = {}

  #players_weekly = {}

  teams = {}

  x = 0

  def level(playerscore):
      
      x = 0

      for level_num, level_xp in enumerate(levels, start=1):

        if level_xp > playerscore:

          global player_level_up_percent

          previous_level_score = levels[x - 1]

          player_level_up_percent1 = levels[x] - previous_level_score
      
          player_level_up_percent2 = playerscore - previous_level_score

          player_level_up_percent = player_level_up_percent2 / player_level_up_percent1 

          break

        x = x + 1

      global player_current_level

      player_current_level = level_num - 1

      global player_levelup_percent

      try:

        #leveling_start + level_number_change * level_expenential_growth_modifier

        player_levelup_percent = int(player_level_up_percent * 100)
      except ZeroDivisionError:
        player_levelup_percent = int(player_level_up_percent * 100)

      except NameError:
        player_levelup_percent = "???"

      #print(f'Level: {player_current_level}.')

      #print(f'Progress to next level: {player_levelup_percent}%.')

  def team_score(team):
    
    score_counting = 0

    counting_var = 0

    print("--------------")

    print("adding up team score...")

    for user in match_data.users:

      if user in match_data.team_metadata.get(team):

        time.sleep(1)

        score_counting += api_info.user(user_name=user).total_score - match_data.initial_score[counting_var]

        #print(score)
      
      counting_var += 1

    return score_counting

  def team_players(team):

    players = {}

    print("--------------")

    print("getting player info...")

    for name in match_data.team_metadata[team]:

      time.sleep(2)

      user_pos = match_data.users.index(name)

      player = user_block(name)

      playcount = player.play_count - match_data.initial_playcount[user_pos]

      playcount = ("{:,}".format(playcount))

      score = player.score - match_data.initial_score[user_pos]

      score_formatted = ("{:,}".format(score))

      avatar = player.avatar

      background = player.background

      link = player.link

      map_background = player.map_cover

      map_title = player.map_title

      map_difficulty = player.map_difficulty

      map_url = player.map_url

      mods = player.mods

      artist = player.artist
      
      accuracy = player.accuracy

      max_combo = player.max_combo

      rank = player.rank

      #weekly_map_score = player.weekly_map_score

      #weekly_map_score_formated = ("{:,}".format(weekly_map_score))
      
      try:
        rank_color = player.rank_color
      except AttributeError:
        rank_color = "red"

      if score == 0:

        recent_score = 0

      else:
        
        recent_score = player.recent_score

        recent_score = ("{:,}".format(recent_score))
    
      level(score)

      players[name] = [score, avatar, background, link, recent_score, player_current_level, player_levelup_percent, map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount]

      players = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))

    return players

  if match_data.mode == "teams":

    for team in match_data.team_metadata.keys():

      team_data = Teams(team)
      
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
  
  else:

    players = {}
    
    x = 0

    for name in match_data.users:

      time.sleep(2)

      player = user_block(name)

      playcount = player.play_count - match_data.initial_playcount[x]

      playcount = ("{:,}".format(playcount))

      score = player.score - match_data.initial_score[x]

      score_formatted = ("{:,}".format(score))

      avatar = player.avatar

      background = player.background

      link = player.link

      map_background = player.map_cover

      map_title = player.map_title

      map_difficulty = player.map_difficulty

      map_url = player.map_url

      mods = player.mods

      artist = player.artist
      
      accuracy = player.accuracy

      max_combo = player.max_combo

      rank = player.rank

      #weekly_map_score = player.weekly_map_score

      #weekly_map_score_formated = ("{:,}".format(weekly_map_score))
      
      try:
        rank_color = player.rank_color
      except AttributeError:
        rank_color = "red"

      if score == 0:

        recent_score = 0

      else:
        
        recent_score = player.recent_score

        recent_score = ("{:,}".format(recent_score))
    
      level(score)

      players[name] = [score, avatar, background, link, recent_score, player_current_level, player_levelup_percent, map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount]

      x = x + 1

      print(f"{x + 1} players refreshed")

  global players_sorted

  players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))

  global teams_sorted

  teams_sorted = dict(sorted(teams.items(), key=lambda x: x[1][0], reverse=True))

  #print(f"teams_sorted loc: {team}")

  #players_sorted_weekly = dict(sorted(players_weekly.values(), key=lambda x: x[20], reverse=True))

  print("all player data refreshed!")

  return redirect(f'{public_url}/Current.html')

#@app.route("/Teams.html")
def teams():
  team1_users = ["GDcheerios", "BirdPigeon", "kokuren"]
  team_score = []
  team_acc = []

  for user in team1_users:
    team_score.append(api_info.user(user_name=user).total_score)
    team_acc.append(api_info.user(user_name=user).accuracy)

    def listToString(seq):
      return ''.join(seq)
      
    team_avg = sum(team_acc) / len(team_acc)

  total_team_score = sum(team_score)
    
  team1 = team("طفل محرج", total_team_score, team_avg)

  team1_users_string = listToString(team1_users)

  print(team)
  
  return render_template(
    'Teams.html',  # Template file
    team1 = team1,
    team1_users = team1_users,
    team_score = team_score,
    total_team_score = total_team_score,
    team_acc = team_acc,
    api_info = api_info
  )

#@app.route("/players.html")
def players():

  players = {}

  for name in player_list:
    score_block = user_block(f"{name}")
    name = score_block.username
    avatar = ("https://a.ppy.sh/%s" % (score_block.id))
    background = requests.get(f"https://osu.ppy.sh/api/v2/users/{name}", headers = {"Authorization": f'Bearer {access_token}'}).json()
    background = background["cover_url"]
    score = score_block.score
    players[name] = [score, avatar, background]

  players = sorted(players.items(), key=lambda x: x[1], reverse=True)

  return render_template(
    'players.html',  # Template file
    api_info_scoreboard = api_info_scoreboard,
    name = name,
    avatar = avatar,
    score = score,
    players = players_sorted
  )

@app.route("/Current.html")
def current():

  match_title = match_data.match_name
  
  return render_template(
    'Current.html',  # Template file
    #recent = player_recent
    current_mode = mode,
    time = time,
    match_data = match_data,
    players = players_sorted,
    teams = teams_sorted
    #teamcount = teamcount
  )

@app.route("/changelog.html")
def changelog():

  return render_template(
    'changelog.html'
  )


if __name__ == "__main__":  # Makes sure this is the main process
  app.run( # Starts the site
    host='0.0.0.0',  # Establishes the host, required for repl to detect the site
    port=80,# Randomly select the port the machine hosts on.
    debug=True

  )
