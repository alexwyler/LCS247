'''
Created on Sep 12, 2014

@author: alexwyler
'''
from urllib import parse, request
import os
import players
import json
import platform
import subprocess
import time
import os

RIOT_CLIENT_KEY = "17e7c567-e54e-4995-bf0f-9d1c9dd3722c"
MASHAPE_BASE_URL = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA/"
RIOT_BASE_URL = "https://na.api.pvp.net/api/lol/na"

MAC_LOL_VERSION = "0.0.0.133"
MAC_LOL_CLIENT_VERSION = "0.0.0.144"

PC_LOL_VERSION = "0.0.1.54"
PC_LOL_CLIENT_VERSION = "0.0.1.54"

def os_specific_init():
    if platform.system() != 'Darwin':
        os.chdir(r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\0.0.1.54\deploy")
    pass;

def main():
    
    os_specific_init()
    
    while True:
        print("Searching for next game...")
        player, account, game_info = get_next_game()
        
        if game_info:
            spectate_info = game_info['playerCredentials'];   
            print(player, account, spectate_info)

            if platform.system() != 'Darwin':
                process = open_game_pc(spectate_info)
            else:
                process = open_game_mac(spectate_info)
                
#             while get_active_game(account):
#                 print("Game still in progress.  Waiting 30 seconds...")
#                 time.sleep(30)

            time.sleep(10)
            print("killing process")
            os.system( r'taskkill /F /IM "League of Legends.exe"' )
            
#             process.kill()
        else:
            print("No active games! Continuing to search...")
        
'''
Opens game on mac given the spectate_info and returns a handle on the process
'''
def open_game_mac(spectate_info):
    devnull = open(os.devnull, "w")
    ip_and_port = str(spectate_info['observerServerIp']) + ':' + str(spectate_info['observerServerPort'])
    cmd = '''
    cd /Applications/League\ of\ Legends.app/Contents/LoL/RADS/solutions/lol_game_client_sln/releases/{0}/deploy/LeagueOfLegends.app/Contents/MacOS/
    riot_launched=true "/Applications/League of Legends.app/Contents/LoL/RADS/solutions/lol_game_client_sln/releases/{0}/deploy/LeagueOfLegends.app/Contents/MacOS/LeagueofLegends" 8394 LoLLauncher "/Applications/League of Legends.app/Contents/LoL/RADS/projects/lol_air_client/releases/{1}/deploy/bin/LolClient" "spectator {2} {3} {4} {5}"
    '''.format(MAC_LOL_VERSION, MAC_LOL_CLIENT_VERSION, ip_and_port, spectate_info['observerEncryptionKey'], spectate_info['gameId'], 'NA1')
    
    full_cmd = ["bash", "-c", cmd]
    
    return subprocess.Popen(full_cmd, stderr = devnull)

def open_game_pc(spectate_info):
    ip_and_port = str(spectate_info['observerServerIp']) + ':' + str(spectate_info['observerServerPort'])
    encryption_key = spectate_info['observerEncryptionKey']
    game_id = spectate_info['gameId']
    server = "NA1"
    
    return subprocess.call([r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\{0}\deploy\League of Legends.exe".format(PC_LOL_VERSION),
                "8394",
                "LoLLauncher.exe",
                "",
                "spectator {0} {1} {2} {3}".format( ip_and_port, encryption_key, game_id, server )])
    
'''
Returns tuple of (player, account, game_info) for the most popular current game
'''
def get_next_game():
    for player in players.PLAYERS:
        print("----- Player: " + player + " -----")
        for summoner in players.PLAYERS[player]:
            print("Account: " + summoner)
            next_game = get_active_game(summoner)
            if next_game:
                return (player, summoner, next_game)
    return (None, None, None)
            

def authenticate_mashape_request(req):
    req.add_header("X-Mashape-Key", "RQk9vZZLGQmshgjK5Yg8nsx5rz4Ep1SJ5I5jsneUxclaP4OTJR")
    return req

def get_active_game(summoner_name):
    req = request.Request(MASHAPE_BASE_URL + "/summoner/retrieveInProgressSpectatorGameInfo/{0}".format(summoner_name.replace(" ", "")))
    authenticate_mashape_request(req)
    game_info = get_json(req)
    return game_info if not game_info.get('error') else None

def get_summoner_id(summoner):
    data = get_json(build_api_url("/v1.4/summoner/by-name/" + summoner))
    return data[next(iter(data))]["id"]

def get_json(url, encoding="utf-8"):
    return json.loads(request.urlopen(url).read().decode(encoding))

def build_api_url(path, params=None):
    if not params:
        params = {}
    
    params["api_key"] = RIOT_CLIENT_KEY
    return RIOT_BASE_URL + path + '?' + parse.urlencode(params)

if __name__ == "__main__":
    main()