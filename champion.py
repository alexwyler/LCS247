'''
Created on Sep 12, 2014

@author: alexwyler
'''

import main

#Can format the name in any sort of way
def get_champion_name_from_game_info( player_name, game_info ):
    id = get_champion_id_by_name( player_name, game_info['game']['playerChampionSelections']['array'] )
    if id:
        return get_champion_name_by_id( id )
    pass

def get_champion_id_by_name( name, team ):
    
    internal_name = main.stripSpaceAndLower(name)
    for player in team:
        if player['summonerInternalName'] == internal_name:
            return player['championId']
    return None

def get_champion_name_by_id( id ):
    json = main.get_json( main.build_static_api_url(r"/v1.2/champion/" + str(id) ) )
    return json['name']

def test():
    player, account, game_info = main.get_next_game()
    name = get_champion_name_from_game_info( player, game_info)
    
    print( name )
    pass

test();
