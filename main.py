import os#making sure pip is always up to date
from os import system
import os

#securing
secret = os.environ['secret']
api_key = os.environ['api']
extra_api_key = os.environ['extra_api_key']


'''
system('pip install --upgrade pip')
system('')
'''

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

api_info = slider.client.Client("", str(api_key), api_url='https://osu.ppy.sh/api')

#classes
#making the library
slider.library.Library("")

#team class
class team:
  def __init__(self, name, score, accuracy):
    self.name = name
    self.score = score
    self.accuracy = accuracy

#players class
class player:
  def __init__(self, name):
    self.name = name

    self.score = api_info.user(user_name=str(name)).total_score

with open("players.db", "r") as f:
    player_list = f.read().splitlines()

new_game = str(input("start new game?\ny/n\n"))
if new_game == "y":
  for username in player_list:
    f = open("match_scores.txt", "w+")

    user = player(username)

    f.write("%s\n" % (user.score))

  f.close()

elif new_game == "n":
  print("alright continuing the game")

else:
  print("...")

def match_refresh():
  with open("players.db", "r") as f:
    player_list = f.read().splitlines()

  for player in player_list:
    player_stats = api_info.user(user_name=str(player))

def team_refresh():
  None

def 

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

joe = requests.get("https://osu.ppy.sh/api/v2/users/3242450/osu", headers={"Authorization" : "Bearer {{api_key}}"})

#recent = requests.get("https://osu.ppy.sh/api/v2/users/11339405/scores/recent", json={"include_fails": "0", "mode": "osu", "limit": "1", "offset": "1"}, headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization" : "Bearer {{952f25aee05178bd249c6781a88e98a098afa08b}}"})

print("test log:\n")

print(joe.text)

#print(recent.text)

print("=----------=\n end of log\n")

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

  api_info = slider.client.Client("", "6a5de2f4b1a29f26710a2a48759c463f9bef68e2", api_url='https://osu.ppy.sh/api')

  return render_template(
    'players.html',  # Template file
    api_info = api_info,
  )

@app.route("/Current.html")
def current():

  debug = open("debug.txt", "w+")
  recent = api_info.user(user_name="GDcheerios")
  html_finder = re.search("\>(\w+)|( achieved rank .\w+ on )|m=0'>(.*? - .*?\])", str(recent.events))
  debug.write(str(html_finder.group()))
  debug.close()
  
  with open("match_scores.txt", "r") as f:
    initial_scores = f.read().splitlines()

  x = 0
    
  class player_scores:
    def __init__(self, name):
      self.name = name

      self.score = (api_info.user(user_name=str(name)).total_score - int(initial_scores[x - 1]))

  player_ranking = []

  for player in player_list:
    
    player_match_score = player_scores(player)

    player_ranking_info = ("%s %s" % (player, str(player_match_score.score)))

    print(player_ranking_info)

    player_ranking.append(player_ranking_info)

    print(player_ranking)

    x = x + 1

  print()

  #recent = requests.get("https://osu.ppy.sh/api/v2/users/GDcheerios/scores/recent", json={"include_fails": "0", "mode": "osu", "limit": "1", "offset": "1",})

  return render_template(
    'Current.html',  # Template file
    recent = recent,
    user_recent = html_finder.group()
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