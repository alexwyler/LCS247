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



def end():
    print("swag2")
    os.system( r'taskkill /F /IM "League of legends.exe"' )
    pass

def os_specific_init():
    if platform.system() != 'Darwin':
        os.chdir( r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\{0}\deploy".format(PC_LOL_CLIENT_VERSION) )
    pass;

def startLeague():
     
    ip_and_port = "95.172.65.26:8088"
    encryption_key = "qBGEz0x+lz6BWehztiPRFoBlBE1aMhEb"
    game_id = "948497185"
    server = "EUN1"
     
    os.spawnl(os.P_DETACH, 
                r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\{0}\deploy\League of Legends.exe".format(PC_LOL_VERSION),
                "8394",
                "LoLLauncher.exe",
                "",
                "spectator {0} {1} {2} {3}".format( ip_and_port, encryption_key, game_id, server ))


    pass

stack = []

def lookupPlayer( player ):
    for summoner in players.PLAYERS[player]:
        res = get_active_game( summoner )
        if res != None:
            stack.append( summoner )
#             print( stack.pop(0) )
            print( summoner )
            print( res )
    pass


def test():
#     with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
#         for x in range(0, 6):
#             future_to_sleep = {executor.submit(sleep) }
#         for future in concurrent.futures.as_completed( future_to_sleep ):
#             data = future.result()
#             print(data)
#         
#     pass

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for player in players.PLAYERS:
            future_to_sleep = {executor.submit(lookupPlayer, player) }
    
#     while not stack:
#         print( stack.index(0) )
#     pass
    
    

# main()
# time.sleep(5)# end()
os_specific_init()
test();