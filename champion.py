'''
Created on Sep 12, 2014

@author: alexwyler
'''

import main
import util
import api

#Can format the name in any sort of way
def get_champion_name_from_game_info( player_name, game_info ):
    ident = get_champion_id_by_name( player_name, game_info['game']['playerChampionSelections']['array'] )
    if ident:
        return get_champion_name_by_id( ident )
    pass

def get_champion_id_by_name( name, team ):
    
    internal_name = util.to_clean_name(name)
    for player in team:
        if player['summonerInternalName'] == internal_name:
            return player['championId']
    return None

def get_champion_name_by_id( ident ):
    json = api.get_json( api.build_api_url("/static-data/na/v1.2/champion/" + str(ident) ) )
    return json['name']

def test():
    player, _, game_info = main.get_next_game()
    name = get_champion_name_from_game_info( player, game_info)
    
    print( name )
    pass

if __name__ == "__main__":
    test();