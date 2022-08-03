import nbtlib
from nbtlib.tag import Int
import os
import json
import requests
import re
import random
#from flask import Flask, redirect, render_template, request

class Player:
  def __init__(self, name, avatar_url, health, hunger, level, xp, pos):
    self.name = name
    self.avatar_url = avatar_url
    self.health = health
    self.hunger = hunger
    self.level = level
    self.xp = xp
    self.pos = pos

def give_num(value):
  return(int(re.search("\d+", str(value)).group()))
  
def player_data(get_players):
  if get_players == True:
    print("updating data")
    player_data = json.load(open("minecraft/player_data.json", "r+"))
    print(player_data)
    players = []
    uuids = []
    
    for file in os.listdir("minecraft/world/playerdata"):
      if re.search("\.\w+", file).group() != ".cosarmor" and re.search("\.\w+", file).group() != ".dat.tmp":
        try:
          dict_thing = {}
          dict_thing["data"] = nbtlib.load(f"minecraft/world/playerdata/{file}")
          player_info = requests.get(f"https://playerdb.co/api/player/minecraft/{file[:-4]}").json()
          dict_thing["username"] = player_info["data"]["player"]["username"]
          dict_thing["avatar"] = player_info["data"]["player"]["avatar"]
          players.append(dict_thing)
          uuids.append(file[:-4])
        except:
          print("error")

    updated_players = []
    for player in players:
      e = Player(player['username'], player['avatar'], player['data']['Health'] + player['data']['AbsorptionAmount'], player['data']['foodLevel'], player['data']['XpLevel'], player['data']['Score'], player['data']['Pos'])
      updated_players.append({'username' : e.name, 'avatar' : e.avatar_url, 'health' : int(e.health), 'hunger' : give_num(e.hunger), 'level' : e.level, 'score' : give_num(e.xp), 'position' : f"X:{give_num(e.pos[0])}, Y:{give_num(e.pos[1])}, Z:{give_num(e.pos[2])}"})
      if uuids[players.index(player)] not in player_data.keys():
        player_data[uuids[players.index(player)]] = updated_players[players.index(player)]
    
    json.dump(player_data, open("minecraft/player_data.json", "w"), indent=4)
    
  else:
    print("getting data")
    player_data = json.load(open("minecraft/player_data.json", "r+"))
    players = []
    for player in player_data.items():
      player_game_data = nbtlib.load(f"minecraft/world/playerdata/{player[0]}.dat")
      e = Player(player[1]["username"], player[1]["avatar"], player_game_data['Health'] + player_game_data['AbsorptionAmount'], player_game_data['foodLevel'], player_game_data['XpLevel'], player_game_data['Score'], player_game_data['Pos'])
      players.append({'username' : e.name, 'avatar' : e.avatar_url, 'health' : int(e.health), 'hunger' : give_num(e.hunger), 'level' : e.level, 'score' : give_num(e.xp), 'position' : f"X:{give_num(e.pos[0])}, Y:{give_num(e.pos[1])}, Z:{give_num(e.pos[2])}"})

    return(players)