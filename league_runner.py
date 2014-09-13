'''
Created on Sep 12, 2014

@author: alexwyler
'''
'''
RIOT_CLIENT_KEY = "17e7c567-e54e-4995-bf0f-9d1c9dd3722c"
RIOT_BASE_URL = "https://na.api.pvp.net/api/lol/na/v1.4"
'''

import os
import platform
import shlex
from subprocess import check_call
import subprocess
import time
from tkinter.tix import Shell
from urllib import parse, request




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

# def startLeague():
#     
#     ip_and_port = str(spectate_info['observerServerIp']) + ':' + str(spectate_info['observerServerPort'])
#     encryption_key = spectate_info['observerEncryptionKey']
#     game_id = spectate_info['gameId']
#     server = "NA1"
#     
#     subprocess.call([r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\{0}\deploy\League of Legends.exe".format(PC_LOL_VERSION),
#                 "8394",
#                 "LoLLauncher.exe",
#                 "",
#                 "spectator {0} {1} {2} {3}".format( ip_and_port, encryption_key, game_id, server )])
# 
#     
#     pass
    

# main()
# time.sleep(5)# end()
os_specific_init()
end();