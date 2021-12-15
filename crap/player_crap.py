#packages
import json
import time
import requests
from crap import authentication_crap, function_crap

#open player_data and read all the data
with open("player_data.json") as player_data:
  player_data = json.load(player_data)

#user crap class
class UserConstructor:
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
    self.request_scores = requests.get(f"https://osu.ppy.sh/api/v2/users/{self.id}/scores/recent", params = {"include_fails": "0", "mode": "osu", "limit": "1", "offset": "0"}, headers = {"Authorization": f'Bearer {authentication_crap.access_token}'}) 
    time.sleep(1)
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




def user_data_grabber(id=0, name=None, pull_user_data=False, pull_recent_map_data=False, pull_user_tags=False, specific_data=[]):
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
  
  if pull_recent_map_data == True:
    if id != 0:
      return(player_data[id]["recent map data"])
    
    if name != None:
      for userid in player_data:
        if name == player_data[userid]["recent map data"]["name"]:
          return(player_data[userid]["recent map data"])
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
  '''
  refreshes a player's data
  
  :id: the user id
  '''
    
  authentication_crap.check_access()
  
  print(f"loading user {id}'s data")
  time.sleep(2) #add delay to not request too quick
  player = UserConstructor(id)
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

    print(json.dumps(player_data[userid], indent=4, sort_keys=False))

    #overwrite player_data.json with player_data dict
    with open("player_data.json", "w") as file:
      json.dump(player_data, file, indent = 4, sort_keys = False)
        



#read player data
def player_list():
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
  
  if input == "done":
    return("done")
  
  return(players[int(selection)])




def player_match_constructor(id, match_data):
  '''
  will return a list of the players stats
  
  id : int
    user id
  
  match_data : JSON
    specifying the match_data
  '''
  
  player_thing = []
  
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

  return(name, [score, avatar, background, link, recent_score, function_crap.level(score, "level"), function_crap.level(score, "leveluppercent"), map_background, map_title, map_difficulty, map_url, mods, artist, accuracy, max_combo, rank, rank_color, score_formatted, playcount])