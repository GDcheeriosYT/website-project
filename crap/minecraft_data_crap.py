import nbtlib
from nbtlib.tag import Int
import os
import json
import requests
import re
#from flask import Flask, redirect, render_template, request


def player_data():
  players = []

  class Player:
    def __init__(self, name, avatar_url, health, hunger):
      self.name = name
      self.avatar_url = avatar_url
      self.health = health
      self.hunger = hunger
      
  for file in os.listdir("minecraft/world/playerdata"):
    if re.search("\.\w+", file).group() != ".cosarmor":
      dict_thing = {}
      dict_thing["data"] = nbtlib.load(f"minecraft/world/playerdata/{file}")
      player_info = requests.get(f"https://playerdb.co/api/player/minecraft/{file[:-4]}").json()
      dict_thing["username"] = player_info["data"]["player"]["username"]
      dict_thing["avatar"] = player_info["data"]["player"]["avatar"]
      players.append(dict_thing)
      print(len(players))

  updated_players = []
  for player in players:
    e = Player(player['username'], player['avatar'], player['data']['']['Health'] + player['data']['']['AbsorptionAmount'], player['data']['']["foodLevel"])
    updated_players.append({'username' : e.name, 'avatar' : e.avatar_url, 'health' : int(e.health), 'hunger' : int(re.search("\d+", str(e.hunger)).group())})
  
  print(json.dumps(updated_players, indent=4))
  
  return(updated_players)