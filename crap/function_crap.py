#packages
import math

class levels:
    '''
    Constructor for levels in matches
    :param score: player score
    '''
    
    levels = []
  
    for current_lvl in range(1, 1000):
        xp_to_next_level = math.floor(2000 * (current_lvl ** 3) + 100000 * current_lvl)
        print(current_lvl, xp_to_next_level)
        levels.append(xp_to_next_level)
        
    def __init__(self, score):
        self.score = score
        x = 0
        for level_num, level_xp in enumerate(levels, start=1):
            x = x + 1
            if level_xp > score:
                global player_level_up_percent
            previous_level_score = levels[x - 1]
            player_level_up_percent1 = levels[x] - previous_level_score
            player_level_up_percent2 = score - previous_level_score
            player_level_up_percent = player_level_up_percent2 / player_level_up_percent1 
            break

        global player_current_level
        player_current_level = level_num - 1
        global player_levelup_percent
        player_levelup_percent = int(player_level_up_percent * 100)