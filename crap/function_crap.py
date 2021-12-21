#packages
import math
import random
    
levels = []

for current_lvl in range(1, 1000):
    xp_to_next_level = math.floor(2000 * (current_lvl ** 3) + 100000 * current_lvl)
    #print(current_lvl, xp_to_next_level)
    levels.append(xp_to_next_level)
    
def level(score, output):
    '''
    Constructor for levels in matches
    :score: player score
    :output: which output it will return
    '''
    
    def for_loop():
        x = 0
        for level_num, level_xp in enumerate(levels, start=1):
            x = x + 1
            if level_xp > score:
                previous_level_score = levels[x - 1]
                player_level_up_percent1 = levels[x] - previous_level_score
                player_level_up_percent2 = score - previous_level_score
                return(player_level_up_percent2 / player_level_up_percent1, level_num)
    
    essential_variable = for_loop()

    player_current_level = essential_variable[1] - 1
    player_levelup_percent = int(essential_variable[1] * 100)
    if output == "level":
        return(player_current_level)
    elif output == "testing":
        return(player_current_level, player_levelup_percent)
    else:
        return(player_levelup_percent)
    
def randnum(min, max):
    '''
    returns a random number
    '''
    
    return(random.randint(min, max))
    