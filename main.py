import os

#securing / importing flask variables
import Client_Credentials as client

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
import importlib
import lxml
from lxml import html
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from dataclasses import dataclass
from typing import List
from collections import OrderedDict
import json
import time
import sqlite3
import urllib
import asyncio
import shutil
import datetime as dt

#variable to call requests with the slider module
api_info = slider.client.Client("", str(client.api_key), api_url='https://osu.ppy.sh/api')

#making the library for slider
slider.library.Library("")

#classes
#clan class
class clans:
  def __init__(self, name, score, accuracy):
    self.name = name
    self.score = score
    self.accuracy = accuracy


#team in a match class
class Teams:
  def __init__(self, team_name, match_data):
    self.team_name = team_name
    self.users = match_data["team metadata"][team_name]


#user block class
class user_block:
  def __init__(self, id):
    self.id = id
    self.request_profile = requests.get(f"https://osu.ppy.sh/api/v2/users/{self.id}/osu", headers = {"Authorization": f'Bearer {access_token}'}).json()
    
    print(self.request_profile['username'])
    
    
    #if user isn't found construct a "ghost" user
    try:
      self.name = self.request_profile['username']
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
    
    #user main info
    self.name = self.request_profile['username']
    self.play_count = self.request_profile['statistics']['play_count']
    self.request_scores = requests.get(f"https://osu.ppy.sh/api/v2/users/{self.id}/scores/recent", params = {"include_fails": "0", "mode": "osu", "limit": "1", "offset": "0"}, headers = {"Authorization": f'Bearer {access_token}'}) 
    self.score = self.request_profile["statistics"]["total_score"]
    self.avatar = self.request_profile['avatar_url']    
    self.background = self.request_profile['cover_url']
    self.link = (f"https://osu.ppy.sh/users/{self.id}")
    
    #recent map info
    #all except are for if recent map is not found
    
    #recent score from map played
    try:
      self.recent_score = (json.loads(self.request_scores.text)[0]["score"])
    except IndexError:
      self.recent_score = 0

    #recent map background
    try:
      self.map_cover = (json.loads(self.request_scores.text)[0]["beatmap"]["beatmapset_id"])
      self.map_cover = f"https://assets.ppy.sh/beatmaps/{self.map_cover}/covers/cover.jpg"
    except IndexError:
      self.map_cover = "https://data.whicdn.com/images/100018401/original.gif"

    #recent map url
    try:
      self.map_url = (json.loads(self.request_scores.text)[0]["beatmap"]["url"])
    except IndexError:
      self.map_url = "https://osu.ppy.sh/beatmapsets"

    #recent map difficulty
    try:
      self.map_difficulty = (json.loads(self.request_scores.text)[0]["beatmap"]["difficulty_rating"])
    except IndexError:
      self.map_difficulty = "0"

    #recent map title
    try:
      self.map_title = (json.loads(self.request_scores.text)[0]["beatmapset"]["title_unicode"])
    except IndexError:
      self.map_title = "not found"

    #recent map mods used
    try:
      self.mods = (json.loads(self.request_scores.text)[0]["mods"])
      if len(self.mods) == 0:
        self.mods = "no mods"
      else:
        self.mods = self.mods
    except IndexError:
      self.mods = ""
      
    #recent map artist
    try:
      self.artist = (json.loads(self.request_scores.text)[0]["beatmapset"]["artist_unicode"])
    except IndexError:
      self.artist = ""

    #recent map accuracy
    try:
      self.accuracy = (json.loads(self.request_scores.text)[0]["accuracy"])
      self.accuracy = round(self.accuracy * 100, 2)
    except IndexError:
      self.accuracy = ""

    #recent map highest combo achieved
    try:
      self.max_combo = (json.loads(self.request_scores.text)[0]["max_combo"])
    except IndexError:
      self.max_combo = ""

    #recent map grade
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
      
    #user tags
    with open("player_data.json")as f:
      player_data = json.load(f)
    
    try:
      self.development_tags = player_data[self.id]["user tags"]["development tags"]
    except KeyError:
      self.development_tags = []
    
    try:
      self.award_tags = player_data[self.id]["user tags"]["award tags"]
    except KeyError:
      self.award_tags = []


#read player data
def player_list():
  with open("player_data.json") as f:
    player_data = json.load(f)
  
  players = []
  x = 0
  
  for id in player_data:
    players.append(player_data[id]["user data"]["name"])
    print(x+1, player_data[id]["user data"]["name"])
    
  selection = input("which player?\n")
  return(players[selection])


#refresh player values
async def player_refresh(id):
  
  #open player_data and read all the data
  with open("player_data.json") as player_data:
    player_data = json.load(player_data)
    
  if id == "all":
    for userid in player_data:
      print(f"loading user {userid}'s data")
      time.sleep(2) #add delay to not request too quick
      player = user_block(userid)
      name = player.name
      playcount = player.play_count
      score = player.score
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
      development_tags = player.development_tags
      award_tags = player.award_tags

      #make sure recent map has a grade color
      try:
        rank_color = player.rank_color
      except AttributeError:
        rank_color = "red"

      if score == 0:
        recent_score = "0"
      else:
        recent_score = player.recent_score
        recent_score = ("{:,}".format(recent_score))
      
      
      #create player_data dict
      user_data = {"name" : name, "score" : score, "playcount" : playcount, "avatar url" : avatar, "background url" : background, "profile url" : link}
      recent_map_data = {"map title" : map_title, "map difficulty" : map_difficulty, "map url" : map_url, "map background url" : map_background, "mods" : mods, "artist" : artist, "accuracy" : accuracy, "max combo" : max_combo, "map grade" : rank, "rank color" : rank_color, "recent score" : recent_score}
      user_tags = {"development tags" : development_tags, "award tags" : award_tags}
      player_data[userid] = {"user data" : user_data, "recent map data" : recent_map_data, "user tags" : user_tags} #[score, avatar, background, link, recent_score, 0, 0, map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount]

      #overwrite player_data.json with player_data dict
      with open("player_data.json", "w") as file:
        json.dump(player_data, file, indent = 4, sort_keys = False)
    
  else:
    
    print(f"loading user {id}'s data")
    time.sleep(2) #add delay to not request too quick
    player = user_block(id)
    name = player.name
    playcount = player.play_count
    score = player.score
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
    development_tags = player.development_tags
    award_tags = player.award_tags

    #make sure recent map has a grade color
    try:
      rank_color = player.rank_color
    except AttributeError:
      rank_color = "red"

    if score == 0:
      recent_score = "0"
    else:
      recent_score = player.recent_score
      recent_score = ("{:,}".format(recent_score))
    
    
    #create player_data dict
    user_data = {"name" : name, "score" : score, "playcount" : playcount, "avatar url" : avatar, "background url" : background, "profile url" : link}
    recent_map_data = {"map title" : map_title, "map difficulty" : map_difficulty, "map url" : map_url, "map background url" : map_background, "mods" : mods, "artist" : artist, "accuracy" : accuracy, "max combo" : max_combo, "map grade" : rank, "rank color" : rank_color, "recent score" : recent_score}
    user_tags = {"development tags" : development_tags, "award tags" : award_tags}
    player_data[id] = {"user data" : user_data, "recent map data" : recent_map_data, "user tags" : user_tags} #[score, avatar, background, link, recent_score, 0, 0, map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount]

    #overwrite player_data.json with player_data dict
    with open("player_data.json", "w") as file:
      json.dump(player_data, file, indent = 4, sort_keys = False)


async def match_start(mode):
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
    
    #create teams
    print("\ncreate a team by typing a name\n")
    x = 0 #counting variable
    while True:
      team_players = [] #holds players for this team
      team_name = input("team name:\n") #create a name for this team
      if team_name == "done":
        break #stop creating teams for this match
        
      #pick players
      while True:
        x = 0 #coounting variable
        #display player list
        while x < len(player_list):
          print("\n", x, player_list[x])
          x = x + 1

        #ends creation if value is not a number
        try:
          player_selector = int(input(""))
        except ValueError:
          break

        if player_list[player_selector] not in players_selected:
          players_selected.append(player_list[player_selector])
          
        if player_list[player_selector] not in team_players:
          team_players.append(f"{player_list[player_selector]}")
          
      teams[team_name] = team_players
      
  
  #ffa match creation
  else:
    while True:
      teams = {} #don't ask
      x = 0 #counting variable
      print("\nwho would you like to add to this match?\ntype done to accept players")
      
      while x < len(player_list):
        print(x, player_list[x])
        x = x + 1
        
      pick_user = input("")
      
      #end player picking process
      if str(pick_user) == "done":
        break

      #check if input is too big
      elif int(pick_user) > len(player_list):
        print("\ntoo big!\n")

      #check if input
      elif int(pick_user) < len(player_list) - len(player_list):
        print("\ntoo small!\n")

      #goto next process
      else:
        #check if this player has not been selected
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
  
  #get player info and append them
  for player in players_selected:
    initial_playcount.append(api_info.user(user_name=str(player)).play_count)
    initial_score.append(api_info.user(user_name=str(player)).total_score)


#initialize the match
async def match_initialization():
  match_name = input("match name ")
  game_mode = str(input("teams or free for all\n1.teams\n2.free for all\n"))

  if game_mode == ("1"):
    mode = "teams"
    await match_start(mode)

  else:
    mode = "ffa"
    await match_start(mode)
  
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

#flask set up
app = Flask(  # Create a flask app
  __name__,
  template_folder='templates', # Name of html file folder
  static_folder='static' # Name of directory for static files
)

#home website
@app.route('/')
def home():
  return render_template("index.html")

#redirect code grab for getting token
@app.route('/code_grab')
def code_grab() :

  code = request.query_string #getting the url
  name_verify = str(code).split('code=')[1] #getting the code from the url
  name_verify = re.search(r"\w+", name_verify)
  response = requests.post("https://osu.ppy.sh/oauth/token", json = { 'client_id':int(client.client_id), 'client_secret':client.secret, 'grant_type':'client_credentials', 'scope':'public'}, headers={'Accept':'application/json', 'Content-Type':'application/json'}) #send code in return for a access token
  token_thing = response.json() #grab the token
  global access_token
  access_token = token_thing["access_token"] #access token
  return redirect(f"{client.public_url}/") #redirect

#start console interface
@app.route("/start")
async def main_process():
  while True:
    #ask user what they want to do
    task = input("1.create new match\n2.end match\n3.edit match\n4.test async interface\n5.refresh\n6.exit\n")
    
    #start match
    if task == "1":
      await match_initialization()

    #end match
    elif task == "2":
      i = 0 #counting variable
      player_playcount = []
      player_score = []
      matches = []
      
      #append all matches into matches
      for match in os.listdir("matches/"):
        matches.append(match)
        print(f"{i} {match[:-5]}")
        i += 1

      match_end = int(input("\nwhich match will you end?\n")) #pick the match to end

      with open(f"matches/{matches[match_end]}") as file: # Open the file in read mode
        ending_match = json.load(file) # Set the variable to the dict version of the json file
      # The file is now closed

      with open("player_data.json")as player_data:
        player_data = json.load(player_data) #

      for user in ending_match["users"]:
        user_pos = ending_match["users"].index(user)
                
        player_playcount.append(player_data[user]["playcount"])
        player_score.append(player_data[user]["score"])

      ending_match["final playcount"] = player_playcount
      ending_match["final score"] = player_score

      with open(f"matches/{matches[match_end]}", "w") as file: # Open the file in write mode
        json.dump(ending_match, file, indent = 4, sort_keys = False) # Write the variable out to the file, json formatted
      # The file is now closed
      
      try:
        shutil.move(f"matches/{matches[match_end]}", f"match_history/")
      except FileNotFoundError:
        print("\nfile not found...")

    elif task == "3":

      i = 0

      matches = []

      for match in os.listdir("matches/"):
        matches.append(match)
        print(f"{i} {match[:-5]}")
        i += 1

      match_end = int(input("\nwhich match will you edit?\n"))

      print(matches[match_end])

      task2 = input("1.add user\n2.remove user\n3.edit match name\n4.change level difficulty\n")
      
      if task2 == "1": #add player

        with open(f"matches/{matches[match_end]}") as match_edit:
          match_edit = json.load(match_edit)

        x = 0

        while x < len(player_list):

          print(x, player_list[x])

          x = x + 1

        pick_user = input("\n")

        match_edit["users"].append(player_list[int(pick_user)])
        match_edit["initial score"].append(api_info.user(user_name=player_list[int(pick_user)]).total_score)
        match_edit["initial playcount"].append(api_info.user(user_name=player_list[int(pick_user)]).play_count)

        with open(f"matches/{matches[match_end]}", "w") as file:
          json.dump(match_edit, file, indent = 4, sort_keys = False)

      elif task2 == "2": #remove player

        with open(f"matches/{matches[match_end]}") as match_edit:
          match_edit = json.load(match_edit)

        x = 0

        for user in match_edit["users"]:

          print(f"{x} {user}")

          x += 1
        
        task3 = int(input("who to remove?\n"))

        match_edit["users"].pop(task3)
        match_edit["initial score"].pop(task3)
        match_edit["initial playcount"].pop(task3)

        with open(f"matches/{matches[match_end]}", "w") as file:
          json.dump(match_edit, file, indent = 4, sort_keys = False)

      elif task2 == "3": #change match name
        
        with open(f"matches/{matches[match_end]}") as match_edit:
          match_edit = json.load(match_edit)

        task3 = input("new match name?\n")

        match_edit["match name"] = task3
        

        with open(f"matches/{matches[match_end]}", "w") as file:
          json.dump(match_edit, file, indent = 4, sort_keys = False)
        
        os.rename(f"matches/{matches[match_end]}", f"matches/{task3}.json")
      
      else:

        print("I don't know...")

    elif task == "4":
      print("testing")

    elif task == "5":

      task2 = input("1.refresh all data\n2.refresh certain player data\n3.refresh all users in a match\n")

      if task2 == "1":

        print("refreshing player data...\n")
        await player_refresh("all")
      
      if task2 == "2":

        x = 0

        while x < len(player_list):

          print(x, player_list[x])

          x = x + 1

        pick_user = input("\n")

        await player_refresh(player_list[int(pick_user)])
      
      if task2 =="3":
        
        i = 0

        matches = []

        for match in os.listdir("matches/"):
          matches.append(match)
          print(f"{i} {match[:-5]}")
          i += 1
          
        match_refresh = int(input("\nwhich match's users will you refresh?\n"))
        
        with open(f"matches/{matches[match_refresh]}") as match_data:
          match_data = json.load(match_data)
          
        for user in match_data["users"]:
          
          await(player_refresh(user))

    elif task == "6":
      os.exit()
    
    else:
      print("I don't know...")

@app.route("/login",methods = ['POST', 'GET'])

def login():

  return redirect(f"https://osu.ppy.sh/oauth/authorize?response_type=code&client_id={client.client_id}&redirect_uri={client.public_url}/code_grab&scope=public")

#@app.route("/Teams")
def teams_web():
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

@app.route("/players")
def players():

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
  
  levels = []
  
  for current_lvl in range(1, 1000):
    xp_to_next_level = math.floor(2000 * (current_lvl ** 3) + 100000 * current_lvl)
    print(current_lvl, xp_to_next_level)
    levels.append(xp_to_next_level)

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

      user_pos = match_data["users"].index(id)
      
      try:
        name = player_data[id]["user data"]["name"]
        playcount = player_data[id]["user data"]["playcount"] - match_data["initial playcount"][user_pos]
        playcount = ("{:,}".format(playcount))
        score = (player_data[id]["user data"]["score"] - match_data["initial score"][user_pos])
        score_formatted = ("{:,}".format(score))
        avatar = player_data[id]["user data"]["avatar url"]
        background = player_data[id]["user data"]["background url"]
        link = player_data[id]["user data"]["profile url"]
        map_background = player_data[id]["recent map data"]["map background url"]
        map_title = player_data[id]["recent map data"]["map title"]
        map_difficulty = player_data[id]["recent map data"]["map difficulty"]
        map_url = player_data[id]["recent map data"]["map url"]
        mods = player_data[id]["recent map data"]["mods"]
        artist = player_data[id]["recent map data"]["artist"]
        accuracy = player_data[id]["recent map data"]["accuracy"]
        max_combo = player_data[id]["recent map data"]["max combo"]
        rank = player_data[id]["recent map data"]["map grade"]
        
        try:
          rank_color = player_data[id]["recent map data"]["rank color"]
        except AttributeError:
          rank_color = "red"

        if score == 0:
          recent_score = "0"

        else:
          recent_score = player_data[id]["recent map data"]["recent score"]

        level(score)
      except:
        name = "Unknown User"
        playcount = 0
        score = 0
        score_formatted = 0
        avatar = "https://data.whicdn.com/images/100018401/original.gif"
        background = "https://data.whicdn.com/images/100018401/original.gif"
        link = "https://data.whicdn.com/images/100018401/original.gif"
        map_background = "https://data.whicdn.com/images/100018401/original.gif"
        map_title = "Unkown"
        map_difficulty = 0
        map_url = "https://data.whicdn.com/images/100018401/original.gif"
        mods = []
        artist = "Unknown"
        accuracy = 0
        max_combo = 0
        rank = "F"
        rank_color = "red"
        recent_score = 0
        
        level(score)


      players[name] = [score, avatar, background, link, recent_score, player_current_level, player_levelup_percent, map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount]

      players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))

      player_score_data[name] = score

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
    
    teams_score_data = {}

    def team_score(team):
    
      score_counting = 0

      print("--------------")

      print("adding up team score...")

      for user in match_data["users"]:

        user_pos = match_data["users"].index(user)

        if user in match_data["team metadata"].get(team):

          #time.sleep(1)

          score_counting += player_data[user][0] - match_data["initial score"][user_pos]

          #print(score)

      return score_counting

    def team_players(team):

      players = {}

      for user in match_data["team metadata"][team]:

        user_pos = match_data["users"].index(user)

        playcount = player_data[user][18] - match_data["initial playcount"][user_pos]

        playcount = ("{:,}".format(playcount))

        score = player_data[user][0] - match_data["initial score"][user_pos]

        score_formatted = ("{:,}".format(score))

        avatar = player_data[user][1]

        background = player_data[user][2]

        link = player_data[user][3]

        map_background = player_data[user][7]

        map_title = player_data[user][8]

        map_difficulty = player_data[user][9]

        map_url = player_data[user][10]

        mods = player_data[user][11]

        artist = player_data[user][12]
        
        accuracy = player_data[user][13]

        max_combo = player_data[user][14]

        rank = player_data[user][15]

        try:
          rank_color = player_data[user][16]
        except AttributeError:
          rank_color = "red"

        if score == 0:

          recent_score = "0"

        else:
          
          recent_score = player_data[user][4]

        level(score)

        players[user] = [score, avatar, background, link, recent_score, player_current_level, player_levelup_percent, map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount, score_data]

      players_sorted = dict(sorted(players.items(), key=lambda x: x[1], reverse=True))

      return players_sorted

    for team in match_data["team metadata"].keys():

      team_data = Teams(team, match_data)
      
      team_users = team_data.users

      teams[team] = [team_score(team), team_players(team)]
      
      teams_score_data[team] = team_score(team)

      #print(f"users: {players.keys()}")

      print("===============")

      print(f"team users: {team_users}")

      time.sleep(0.3)

      print(f"team: {team}")

      time.sleep(0.3)

      print(f"team score: {teams[team][0]}")
      
      print("===============")

    teams_sorted = dict(sorted(teams.items(), key=lambda x: x[0], reverse=True))
    
    score_data[f"{dt.date.today()}"] = teams_score_data

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

@app.route("/changelog.html")
def changelog():

  return render_template(
    'changelog.html'
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
    current_matches = current_matches,
    previous_matches = previous_matches
  )

@app.route("/refresh/<player_name>")
async def web_player_refresh(player_name):
  await player_refresh(player_name)

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