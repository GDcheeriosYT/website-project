#making sure pip is always up to date
from os import system
import os

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

#classes
#making the library
slider.library.Library("")

#team class
class team:
  def __init__(self, name, score, accuracy):
    self.name = name
    self.score = score
    self.accuracy = accuracy

#user class
class users:
  def __init__(self, name, token, score, id):
    self.name = name
    self.token = token
    self.score = score
    self.id = id

#making the api connector

extra_api_key = "6a5de2f4b1a29f26710a2a48759c463f9bef68e2"

get_the_key = "https://osu.ppy.sh/oauth/authorize/client_id=5679&redirect_uri=https://gdcheerios.com/"

api_info = slider.client.Client("", "952f25aee05178bd249c6781a88e98a098afa08b", api_url='https://osu.ppy.sh/api')

joe = requests.get("https://osu.ppy.sh/api/v2/users/3242450/osu", headers={"Authorization" : "Bearer {{952f25aee05178bd249c6781a88e98a098afa08b}}"})

#recent = requests.get("https://osu.ppy.sh/api/v2/users/11339405/scores/recent", json={"include_fails": "0", "mode": "osu", "limit": "1", "offset": "1"}, headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization" : "Bearer {{952f25aee05178bd249c6781a88e98a098afa08b}}"})

print("test log:\n")

print(joe.text)

#print(recent.text)

print("=----------=\n end of log\n")

#opening the players file to read player data

player_rows = []
with open("players.db") as p:
    players = p.read().splitlines()


#[line number][data]
#0 = name
#1 = api_key
#def api_key():
  
  #return None

for line in players:
    data = line.split(",")
    print(data)
    if data[0][0] == "GDcheerios":
      print(data[1])
    else:
      print(data[1])

#print(api_key)
  

  

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

  response = requests.post("https://osu.ppy.sh/oauth/token", json = { 'client_id':5679, 'client_secret':"6NRqh4oEYvWkypWxKBCr0Fu82NYFRhmf2Yj8DKjh", 'redirect_uri':"https://osu-api-crap.minecreeper0913.repl.co", 'code':name_verify.group(), 'grant_type':'authorization_code'}, headers={'Accept':'application/json', 'Content-Type':'application/json'})

  print(response.text)

  return redirect("https://osu-api-crap.minecreeper0913.repl.co/")

@app.route("/login.html",methods = ['POST', 'GET'])
def login():

  f = open("codes.txt", "w+")
  return redirect("https://osu.ppy.sh/oauth/authorize?response_type=code&client_id=5679&redirect_uri=https://osu-api-crap.minecreeper0913.repl.co/code_grab&scope=public")
  

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

  user1 = api_info.user(user_name="GDcheerios")

  user2 = api_info.user(user_name="BirdPigeon")

  user3 = api_info.user(user_name="kokuren")

  user4 = api_info.user(user_name="PeterParkerMj")

  user5 = api_info.user(user_name="monvee")

  user6 = api_info.user(user_name="MargaritaMix08")

  user7 = api_info.user(user_name="Trufflebuttt")

  user8 = api_info.user(user_name="Mcg_Tokyo")

  return render_template(
    'players.html',  # Template file
    api_info = api_info,
    user1 = user1,
    user2 = user2,
    user3 = user3,
    user4 = user4,
    user5 = user5,
    user6 = user6,
    user7 = user7,
    user8 = user8
  )

@app.route("/Current.html")
def current():


  debug = open("debug.txt", "w+")
  recent = api_info.user(user_name="GDcheerios")
  html_finder = re.search("<img.*osu!\W", str(recent.events))
  debug.write(str(recent.events))
  debug.close()

  #recent = requests.get("https://osu.ppy.sh/api/v2/users/GDcheerios/scores/recent", json={"include_fails": "0", "mode": "osu", "limit": "1", "offset": "1",})

  return render_template(
    'Current.html',  # Template file
    recent = recent,
    html_finder = html_finder.group()
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