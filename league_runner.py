'''
Created on Sep 12, 2014

@author: alexwyler
'''
from inspect import stack
'''
RIOT_CLIENT_KEY = "17e7c567-e54e-4995-bf0f-9d1c9dd3722c"
RIOT_BASE_URL = "https://na.api.pvp.net/api/lol/na/v1.4"
'''

import concurrent.futures
from concurrent.futures.thread import ThreadPoolExecutor
import os
import platform
import shlex
from subprocess import check_call
import subprocess
import time
from tkinter.tix import Shell
from urllib import parse, request

from main import get_active_game
import main
import players

PC_LOL_VERSION = "0.0.1.54"
PC_LOL_CLIENT_VERSION = "0.0.1.54"



def test2():
    url = main.build_static_api_url(r"/v1.2/champion/103")
    print( url )
    print( main.get_json(url) )
    
#     player, account, game_info = main.get_next_game()
#     id = get_champion_id_by_name( "cRs voyboy", game_info['game']['playerChampionSelections']['array'] )
#     if id:
#         print( str(id) )
    pass

def get_champion_id_by_name( name, team ):
    
    internal_name = main.stripSpaceAndLower(name)
    for player in team:
        if player['summonerInternalName'] == internal_name:
            return player['championId']
    return None

def get_champion_name_by_id( id ):
     url = main.build_static_api_url(r"/v1.2/champion/103")
     print( main.get_json(url) )

test2();