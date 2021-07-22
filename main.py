import os#making sure pip is always up to date
from os import system
import os

system('pip install --upgrade pip')
system('')

#securing
secret = os.environ['secret']
api_key = os.environ['api']
extra_api_key = os.environ['extra_api_key']

#packages
import random
from osuapi import OsuApi, AHConnector, ReqConnector
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

api_info = slider.client.Client("", str(api_key), api_url='https://osu.ppy.sh/api')

api_info_scoreboard = slider.client.Client("", str(extra_api_key), api_url='https://osu.ppy.sh/api')

#classes
#making the library
slider.library.Library("")

#team class
class team:

  def __init__(self, name, score, accuracy):
    
    self.name = name

    self.score = score

    self.accuracy = accuracy

#user block class
class user_block_scoreboard:

  def __init__(self, name):
    
    self.name = name

    self.username = api_info_scoreboard.user(user_name=str(name)).user_name

    self.id = api_info_scoreboard.user(user_name=str(name)).user_id

    self.score = api_info_scoreboard.user(user_name=str(name)).total_score

    self.site_url = ("https://osu.ppy.sh/users/%s" % (self.id))

    page = self.site_url

    driver = webdriver.Firefox()

    driver.get(page)

    self.background = driver.find_element_by_id("header-v4__bg")


#user block class
class user_block_match:

  def __init__(self, name):
    
    self.name = name

    self.username = api_info.user(user_name=str(name)).user_name

    self.id = api_info.user(user_name=str(name)).user_id

    self.score = api_info.user(user_name=str(name)).total_score

    self.site_url = ("https://osu.ppy.sh/users/%s" % (self.id))

    page = requests.get(self.site_url)

    tree = html.fromstring(page.content)

    self.background = tree.xpath('//div[@id="header-v4__bg"]/label()')

#f = open("debug.txt", "w")
#f.write(page)

with open("players.db", "r") as f:
  
    player_list = f.read().splitlines()

def match_start(mode):


  #the variable which will show which mode it is
  global game_mode

  game_mode = mode

  #a list of all the players playing
  global players_selected

  players_selected = []

  #will check to see if teams or ffa is wanted
  if mode == ("teams"):

    #how many teams will there be?
    print("\nhow many teams would you like there to be?\n")

    team_amount = int(input(""))

    #repeats the process of team editing until satisfied
    while True:

      x = 0

      #dictionary will store data of team and users like team num: username, username
      teams = {}

      while x < team_amount:

        teams["team %s" % (x + 1)] = 1

        x = x + 1
      
      print("\nalright!\nwho will be on which team?\nselect a team to edit\n")

      x = 0

      #display teams
      while x < team_amount:
        
        print("team %s" % (x + 1))

        x = x + 1

      team_selector = input("")

      x = 0

      #display player list
      while x < len(player_list):

        print("\n", x, player_list[x])

        x = x + 1

      player_selector = int(input(""))

      if player_list[player_selector] not in players_selected:

        players_selected.append(player_list[player_selector])

      else:

        print("%s is already imported" % (player_list[player_selector]))



  else:
  
    while True:

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

          print("debug:", players_selected)
        
      global initial_score

      initial_score = []
      
      for player in players_selected:

        initial_score.append(api_info.user(user_name=str(player)).total_score)



new_game = str(input("start new game?\ny/n\n"))

if new_game == "y":

  f = open("match_data.py", "w+")

  game_mode = str(input("teams or free for all\n1.teams\n2.free for all\n"))

  if game_mode == ("1"):

    mode = "teams"

    match_start(mode)

  else:

    mode = "ffa"

    match_start(mode)

elif new_game == "n":
  print("alright continuing the game")
  #joe = user_block("btmc")
  #print(joe.background)

else:
  print("...")

#starting the game current version
def match_start():
  


new_game = str(input("start new game?\ny/n\n"))

if new_game == "y":

  f = open("match_data.py", "w+")

elif new_game == "n":
  print("alright continuing the game")
  #joe = user_block("btmc")
  #print(joe.background)

else:
  print("...")

#f.write("users = %s\ninitial_score = %s\n mode = %s" % (players_selected, initial_score, mode))

  f.close()





def match_refresh():
  with open("players.db", "r") as f:
    player_list = f.read().splitlines()

  for player in player_list:
    player_stats = api_info.user(user_name=str(player))

def team_refresh():
  None

#list variable to store which players are participating in the current match
players_in_match = []

def user_list():
  with open("players.db", "r") as f:
    player_list = f.read().splitlines()

  for player in player_list:
    player_stats = api_info.user(user_name=str(player))

#making the api ['connector

extra_api_key = str(extra_api_key)

get_the_key = "https://osu.ppy.sh/oauth/authorize/client_id=5679&redirect_uri=https://gdcheerios.com/"

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
  name_verify = re.search("\w+", name_verify)
  print(name_verify.group())
  
  random_file = open("code.txt", "w+")
  random_file.write(name_verify.group())
  random_file.close()

  response = requests.post("https://osu.ppy.sh/oauth/token", json = { 'client_id':5679, 'client_secret':secret, 'redirect_uri':"https://osu-api-crap.minecreeper0913.repl.co", 'code':str(name_verify.group()), 'grant_type':'authorization_code'}, headers={'Accept':'application/x-www-form-urlencoded', 'Content-Type':'application/x-www-form-urlencoded'})

  token_thing = response.text
  file = open("debug.txt", "w+")
  file.write(token_thing)
  file.close()

  return redirect("https://osu-api-crap.minecreeper0913.repl.co/")

#@app.route("/login.html",methods = ['POST', 'GET'])
'''def login():

  f = open("codes.txt", "w+")
  return redirect("https://osu.ppy.sh/oauth/authorize?response_type=code&client_id=5679&redirect_uri=https://osu-api-crap.minecreeper0913.repl.co/code_grab&scope=public")'''
  

@app.route("/Teams.html")
def teams():
  team1_users = ["GDcheerios", "BirdPigeon", "kokuren"]
  team_score = []
  team_acc = []

  for user in team1_users:
    team_score.append(api_info.user(user_name=user).total_score)
    team_acc.append(api_info.user(user_name=user).accuracy)

    def listToString(s):  
    
      # initialize an empty string 
      str1 = ""
      
      # traverse in the string   
      for ele in s:  
          str1 += ele   
      
      # return string   
      return str1  
      
    team_avg = sum(team_acc) / len(team_acc)

  total_team_score = sum(team_score)
    
  team1 = team("طفل محرج", total_team_score, team_avg)

  team1_users_string = listToString(team1_users)
  
  return render_template(
    'Teams.html',  # Template file
    team1 = team1,
    team1_users = team1_users,
    team_score = team_score,
    total_team_score = total_team_score,
    team_acc = team_acc,
    api_info = api_info
  )

@app.route("/players.html")
def players():

  score_block = user_block_scoreboard("GDcheerios")
  name = score_block.username
  avatar = ("https://a.ppy.sh/%s" % (score_block.id))
  background = score_block.background
  score = score_block.score

  return render_template(
    'players.html',  # Template file
    api_info_scoreboard = api_info_scoreboard,
    name = name,
    avatar = avatar,
    background = background,
    score = score
  )

@app.route("/Current.html")
def current():

  debug = open("debug.txt", "w+")
  recent = api_info.user(user_name="GDcheerios")

  print(recent.events)

  html_finder = re.findall(r"\>(\w+).+( achieved rank .\w+ on ).+m=0'>(.*? - .*?\])", str(recent.events))

  def player_recent():
    for each in html_finder:
      return(''.join(each))
  
  return render_template(
    'Current.html',  # Template file
    recent = player_recent,
    current_mode = game_mode
  )

@app.route("/changelog.html")
def changelog():

  return render_template(
    'changelog.html'
  )


if __name__ == "__main__":  # Makes sure this is the main process
  app.run( # Starts the site
    host='0.0.0.0',  # Establishes the host, required for repl to detect the site
    port=5000,# Randomly select the port the machine hosts on.
    debug=True

  )