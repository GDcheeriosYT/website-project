'''from os import system
import os
import random
'''
system('pip install --upgrade pip')
system('')
'''

#packages
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
import PyV8

#actual code
#starting a new instance
#determining how many players

player_count = input("how many players?\nplease limit to 60\n")

#just a cool line to make the output look more professional lol
print("===================================")

#determining what the win condition will be
#win_condition = input("what win condition would you like?\n1.score gain\n2.Performance Point gain\n")
print("win condition is a work in progress so for now it is just score gained based")

print("===================================")

#making a file for the players and scores to be stored in
f = open("scores.txt", "a+")

#while loop so that I can put more players in
num = 0
while num < int(player_count):
  #getting the players name
  player_name = input("who's score would you like to get? %s/%s \n" % (num, player_count))

  print("===================================")

  #getting info from a user
  user = api_info.user(user_name=str(player_name))

  #the info to write to the user
  #if win_condition == "1":
  #add a tab when complete
  info_grab = user.total_score
  #else:
    #info_grab = user.pp_raw
  #writing the info to the file
  f.write("%s.%s\n" % (player_name, info_grab))

  num = num + 1

f.close()

#reading the file lines
with open("scores.txt") as f:
  names_scores = f.read().splitlines()

#clearing blank space
#credit to code
#https://stackoverflow.com/questions/4710067/how-to-delete-a-specific-line-in-a-file
with open("scores.txt", "r+") as f:
  d = f.readlines()
  f.seek(0)
  for i in d:
      if i != "":
          f.write(i)
  f.truncate()

#sorting player scores
#code by Vishal Singh
sorted_score = sorted(names_scores, key=lambda x: int(x.rsplit(".", maxsplit=1)[-1]))

print("===================================")

score_info = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#limiting the api requests
#player info to see how much score has been gained
while True:
  player_and_score = []

  sc = open("placement.txt", "w+")
  
  def leaderboard(x, y, z):
    sorted_player_score = sorted(player_and_score, key=lambda x: int(x.rsplit(".", maxsplit=1)[-1]))

    with open("placement.txt") as f:
      placement_info = f.read().splitlines()

    player_and_score.append(x + "." + str(abs(int(y) - int(z))))

    rank = 1
    for chicken in sorted_player_score:
      placement = ("#" + str(rank) + " " + chicken)
      sc.write("%s\n" % (placement))
      
      print(placement)
      rank = rank + 1
    
    sc.close()

    return(placement_info)
  
  

  list_limit = len(names_scores)
  chosen_list_place = 0
  while chosen_list_place < list_limit:
    name = re.search("^\w+", names_scores[int(chosen_list_place) - 1])
    score = re.search("[0-9]+", names_scores[int(chosen_list_place) - 1])

    print("===================================")

    def refresh_data():
      user2 = api_info.user(user_name=str(name.group()))
      print(user2.total_score)
      return(user2.total_score)

    #fake score for testing reasons
    def fake_score():
      fake_score = random.randint(50000, 1000000) + random.randint(50000, 1000000)
      score_info[chosen_list_place] += int(refresh_data())
      print(score_info)
      return score_info[chosen_list_place]

      
    #score calculation

    
    current_score_status = name.group() + " has gained " + str(abs(int(score.group()) - int(refresh_data())))+ " since the match has started"

    print(current_score_status)

    print("===================================")

    print(leaderboard(name.group(), score.group(), refresh_data()))
    
    chosen_list_place = chosen_list_place + 1

  again = input("continue?\ntype end to stop, press enter to continue\npause to keep the data but end the program\n")

  if again == "":
    print("continuing...")
  elif again == "pause":
    break
  else:
    os.remove("scores.txt")
    os.remove("placement.txt")
    break

  print("===================================")

print("===================================")

#which code to be shown
code_input = input("which code do you want to be shown?\n1 for testing code\n2 for actual code\n3 for both\n")

#printing the leaderboard function a bit because it seems broken right now



print("===================================")'''