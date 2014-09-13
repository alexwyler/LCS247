'''
Created on Sep 12, 2014

@author: alexwyler
'''
'''
RIOT_CLIENT_KEY = "17e7c567-e54e-4995-bf0f-9d1c9dd3722c"
RIOT_BASE_URL = "https://na.api.pvp.net/api/lol/na/v1.4"
'''

import os
import shlex
import subprocess
import time
from tkinter.tix import Shell
from urllib import parse, request


LAUNCHER_PATH = "C:\\Riot Games\\League of Legends\\lol.launcher.exe"
LAUNCHER_PATH2 = '"start "" /D "C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\0.0.1.54\deploy" "League of Legends.exe" "8394" "LoLLauncher.exe" "" "spectator 216.133.234.17:8088 xVMNoFp3dgt9TnhJFZtnhZTKtVqQVQes 1538864923 NA1""'
# "8394" "LoLLauncher.exe" "" "spectator spectator.na.lol.riotgames.com:8088 5GHjwNvZajaYWIjCtxTX+xEofQhMNObY 1538820789 NA1"

LAUNCHER_BASE = "C:\\Riot Games\\League of Legends\\RADS\\solutions\\lol_game_client_sln\\releases\\0.0.1.54\\deploy\\League of Legends.exe"
PROCESS_NAME = "League of legends.exe"



def main():
    print("swag")
    subprocess.call([r""+LAUNCHER_PATH + " \"8394\" \"LoLLauncher.exe\" \"\" \"spectator spectator.na.lol.riotgames.com:8088 5GHjwNvZajaYWIjCtxTX+xEofQhMNObY 1538820789 NA1\""])
    pass

def end():
    print("swag2")
    os.system( r'taskkill /F /IM "League of legends.exe"' )
    pass

def startLeague():
    subprocess.call( LAUNCHER_PATH2  )
    pass
    

# main()
# time.sleep(5)# end()
startLeague()