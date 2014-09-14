'''
Created on Sep 14, 2014

@author: alexwyler
'''

def safe_str(string):
    if isinstance(string, str):
        return string
    
    try:
        return str(string.encode('utf-8'))
    except TypeError:
        return str(string)
    

def get_player_position( account, running_game_info ):
    team_1 = running_game_info['game']['teamOne']['array']
    team_2 = running_game_info['game']['teamTwo']['array']
    return find_player_by_name( account, team_1, team_2 )

def to_clean_name(account_name):
    return account_name.replace(" ", "").lower()

#returns is found on team 1 and position
def find_player_by_name( name, team_1, team_2 ):
    internal_name = to_clean_name(name)
    index = 0
    for player in team_1:
        if player['summonerInternalName'] == internal_name:
            return True, index
        index += 1
    
    index = 0
    for player in team_2:
        if player['summonerInternalName'] == internal_name:
            return False, index
        index += 1
    pass