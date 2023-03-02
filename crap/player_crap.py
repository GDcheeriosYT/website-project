#packages
import json
import time
import requests
from crap import authentication_crap, function_crap

player_data = None

def update_player_data():
    global player_data
    #open player_data and read all the data
    with open("player_data.json") as player_data:
        player_data = json.load(player_data)


#user crap class
class UserConstructor:
  #open player_data and read all the data
  with open("player_data.json") as player_data:
    player_data = json.load(player_data)
    
  def __init__(self, id):
    '''
    constructs a player data object
    
    returns
    
    a player object
    
    Parameters
    
    id : int
      user id to request data from osu api
    '''
    self.id = id
    self.request_profile = requests.get(f"https://osu.ppy.sh/api/v2/users/{self.id}/osu", headers = {"Authorization": f'Bearer {authentication_crap.access_token}'}).json()
    time.sleep(1)
    
    #if user isn't found construct a "ghost" user
    try:
      self.name = self.request_profile['username']
    except KeyError:
      self.id = "unknown"
      self.name = (f"Unknown")
      self.rank = max()
      self.play_count = 0
      self.score = 0
      self.avatar = "https://data.whicdn.com/images/100018401/original.gif"
      self.background = "https://data.whicdn.com/images/100018401/original.gif"
      self.link = "http://gdcheerios.com/osu/players"
      return None
    
    #user main info
    self.name = self.request_profile['username']
    if self.request_profile['statistics']['global_rank'] != None:
      self.rank = self.request_profile['statistics']['global_rank']
    else:
      self.rank = 999999999
    self.play_count = self.request_profile['statistics']['play_count']
    self.score = self.request_profile["statistics"]["total_score"]
    self.avatar = self.request_profile['avatar_url']    
    self.background = self.request_profile['cover_url']
    self.link = (f"https://osu.ppy.sh/users/{self.id}")
      
    #user tags
    with open("player_data.json")as f:
      player_data = json.load(f)
    
    try:
      self.development_tags = player_data[self.id]["user tags"]["development tags"]
    except:
      self.development_tags = []
    
    try:
      self.award_tags = player_data[self.id]["user tags"]["award tags"]
    except:
      self.award_tags = []




def user_data_grabber(id=0, name=None, pull_user_data=False, pull_recent_map_data=False, pull_user_tags=False, specific_data=[]):
  #open player_data and read all the data
  with open("player_data.json") as player_data:
    player_data = json.load(player_data)
    
  '''
  grab user data
  
  :id: users id to specift data from a player with that id
  :name: users name to specift data from a player with that name
  :pull_user_data: if True will return a dictionary of all the items in user data
  :pull_recent_map_data: if True will return a dictionary of all the items in recent map data
  :pull_user_tags: if True will return a dictionary of all the items in user tags
  :specific_data: input as list, each value should be a string will return the specified data found in the list
  '''
  if id == "done":
    return()
  
  if id != 0:
    id = str(id)
    if id in player_data:
      if len(specific_data) != 0:
        data_list = [] #list containing the specified data
        for data in specific_data:
          for key in player_data[id]:
            for value in player_data[id][key]:
              if data == value:
                data_list.append(player_data[id][key][value])
        return(data_list)
      else:
        return(player_data[id])
    else:
      return(f"No player with such id {id} was found...")
  
  if name != None:
    if len(specific_data) != 0:
      data_list = [] #list containing the specified data
      for data in specific_data:
        if data == "id":
          for id in player_data:
            if player_data[id]["user data"]["name"] == name:
              data_list.append(id)
        for id in player_data:
          for key in player_data[id]:
            if key == data:
              data_list.append(player_data[id][key])
            for value in player_data[id][key]:
              if value == data:
                data_list.append(player_data[id][key][value])
      return(data_list)
    else:
      for id in player_data:
        if player_data[id]["name"] == name:
          return(player_data[id])
  else:
    return(f"No player with such name {name} was found...")
  
  if pull_user_data == True:
    if id != 0:
      return(player_data[id]["user data"])
    
    if name != None:
      for userid in player_data:
        if name == player_data[userid]["user data"]["name"]:
          return(player_data[userid]["user data"])
        else:
          return(f"No player with such name {name} was found...")
  
  if pull_user_tags == True:
    if id != 0:
      return(player_data[id]["user tags"])
    
    if name != None:
      for userid in player_data:
        if name == player_data[userid]["user tags"]["name"]:
          return(player_data[userid]["user tags"])
        else:
          return(f"No player with such name {name} was found...")




async def player_refresh(id):
  #open player_data and read all the data
  with open("player_data.json") as player_data:
    player_data = json.load(player_data)
  '''
  refreshes a player's data
  
  :id: the user id
  '''
    
  authentication_crap.check_access()
  
  print(f"loading user {id}'s data")
  player = UserConstructor(id)
  name = player.name
  rank = player.rank
  playcount = player.play_count
  score = player.score
  avatar = player.avatar
  background = player.background
  link = player.link
  development_tags = player.development_tags
  award_tags = player.award_tags
  
  #create player_data dict
  user_data = {"name" : name, "rank" : rank, "score" : score, "playcount" : playcount, "avatar url" : avatar, "background url" : background, "profile url" : link}
  user_tags = {"development tags" : development_tags, "award tags" : award_tags}
  player_data[id] = {"user data" : user_data, "user tags" : user_tags} #[score, avatar, background, link, recent_score, 0, 0, map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount]

  print(json.dumps(player_data[id], indent=4, sort_keys=False))
  
  #overwrite player_data.json with player_data dict
  with open("player_data.json", "w") as file:
    json.dump(player_data, file, indent = 4, sort_keys = False)




async def refresh_all_players():
  '''
  refreshes all players data
  '''
  
  authentication_crap.check_access()
  
  for userid in player_data:
    print(f"loading user {userid}'s data")
    time.sleep(2) #add delay to not request too quick
    player = UserConstructor(userid)
    name = player.name
    rank = player.rank
    playcount = player.play_count
    score = player.score
    avatar = player.avatar
    background = player.background
    link = player.link
    development_tags = player.development_tags
    award_tags = player.award_tags
    
    #create player_data dict
    user_data = {"name" : name, "rank" : rank, "score" : score, "playcount" : playcount, "avatar url" : avatar, "background url" : background, "profile url" : link}
    user_tags = {"development tags" : development_tags, "award tags" : award_tags}
    player_data[userid] = {"user data" : user_data, "user tags" : user_tags} #[score, avatar, background, link, recent_score, 0, 0, map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount]

    print(json.dumps(player_data[userid], indent=4, sort_keys=False))

    #overwrite player_data.json with player_data dict
    with open("player_data.json", "w") as file:
      json.dump(player_data, file, indent = 4, sort_keys = False)
        



#read player data
def player_list():
  #open player_data and read all the data
  with open("player_data.json") as player_data:
    player_data = json.load(player_data)
  '''
  returns a list of all the player names
  '''
  with open("player_data.json") as f:
    player_data = json.load(f)
  
  players = []
  x = 0
  
  for id in player_data:
    players.append(id)
    print(x, player_data[id]["user data"]["name"])
    x += 1
    
  selection = input("which player?\n")
  
  try:
    return(players[int(selection)])
  except:
    return("done")
  
  
  
  
def player_list_length():
  with open("player_data.json") as f:
    player_data = json.load(f)
  
  players = []
  
  for id in player_data:
    players.append(id)
  
  return(len(players))
  



def player_match_constructor(id):
  '''
  will return a list of the players stats
  
  id : int
    user id
  
  match_data : JSON
    specifying the match_data
  '''
  
  try:
    name = player_data[id]["user data"]["name"]
    avatar = player_data[id]["user data"]["avatar url"]
    background = player_data[id]["user data"]["background url"]
    link = player_data[id]["user data"]["profile url"]
    player_id = id
      
  except:
    name = "Unknown User"
    avatar = "https://data.whicdn.com/images/100018401/original.gif"
    background = "https://data.whicdn.com/images/100018401/original.gif"
    link = "https://data.whicdn.com/images/100018401/original.gif"
    player_id = 0
    
  return(name, [avatar, background, link,  player_id])