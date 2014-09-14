'''
Created on Sep 12, 2014

@author: alexwyler
'''
from urllib import parse, request
import players
import json
import platform
import subprocess
import time
import os
import threading
import champion
import irc_bot
import twitch
from pstats import Stats

RIOT_CLIENT_KEY = "17e7c567-e54e-4995-bf0f-9d1c9dd3722c"
MASHAPE_BASE_URL = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA/"
RIOT_BASE_URL = "https://na.api.pvp.net/api/lol/static-data/na"

GAME_TYPES = ['RANKED_SOLO_5x5']

MAC_LOL_VERSION = "0.0.0.133"
MAC_LOL_CLIENT_VERSION = "0.0.0.144"

PC_LOL_VERSION = "0.0.1.54"
PC_LOL_CLIENT_VERSION = "0.0.1.54"

IN_GAME_PING_FREQUENCY = 5
SPECTATOR_DELAY = 3 * 60

def init():
    irc_bot.init()
    if platform.system() != 'Darwin':
        os.chdir(r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\0.0.1.54\deploy")
    pass;

def main():
    init()
    
    while True:
        print("Searching for next game...")
        player, account, game_info = get_next_game()
        
        if game_info:
            spectate_info = game_info['playerCredentials'];   
            print(player, account, spectate_info)
            team, position = get_player_position(account, game_info)
            team_str = str(team).join(str(team).split()).lower()
            print( "Position found: " + team_str + ", " + str(position) )

            print( update_twitch_channel(player, account, game_info) )
            
            if platform.system() != 'Darwin':
                game_thread = threading.Thread( target=open_game_pc, args = (spectate_info,) )
                game_thread.start()
                ahk_thread = threading.Thread( target=startAutohotkey, args = (team_str,str(position),) )
                ahk_thread.start()
            else:
                open_game_mac(spectate_info)
                pass
            
            print("Waiting for game to end...")
            while get_active_game(account):
                time.sleep(IN_GAME_PING_FREQUENCY)
            
            print("Game complete. Waiting for spectator delay...")
            time.sleep(SPECTATOR_DELAY)
            
            print("Killing game..")
            if platform.system() != 'Darwin':
                kill_game_pc()
            else:
                kill_game_mac()

        else:
            print("No active games!")
    
    pass

def get_player_position( account, running_game_info ):
    team_1 = running_game_info['game']['teamOne']['array']
    team_2 = running_game_info['game']['teamTwo']['array']
    return find_player_by_name( account, team_1, team_2 )

            
#returns is found on team 1 and position
def find_player_by_name( name, team_1, team_2 ):
    internal_name = stripSpaceAndLower(name)
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

def stripSpaceAndLower( raw ):
    return raw.replace(" ", "").lower()


'''player locator
'''
def startAutohotkey( is_team_1, index):
    
    subprocess.call([r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
                     r"C:\Users\Aleesa\Documents\GitHub\LCS247\Autohotkey\SpectatorHelper.ahk",
                     is_team_1,
                     index])
    pass

            
'''
OS Specific ways of killing shit
'''
def kill_game_mac():
    os.system("killall -9 LeagueofLegends");
    pass

def kill_game_pc():
    os.system( r'taskkill /F /IM "League of Legends.exe"' );
    pass

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
        print("Player: " + player)
        for summoner in players.PLAYERS[player]:
            try:
                next_game = get_active_game(summoner)
                if next_game and next_game['game']['queueTypeName'] in GAME_TYPES:
                    return (player, summoner, next_game)
            except Exception as e:
                print('For '  + safe_str(summoner) + ': ', e)
    return (None, None, None)

def update_twitch_channel(player, account, game_info):
    champ_name = champion.get_champion_name_from_game_info(account, game_info)
    title = 'LCS Players 24/7: {0} Playing {1}'.format(player, champ_name)
    twitch.update_channel_title(title)

def authenticate_mashape_request(req):
    req.add_header("X-Mashape-Key", "RQk9vZZLGQmshgjK5Yg8nsx5rz4Ep1SJ5I5jsneUxclaP4OTJR")
    return req

def get_active_game(summoner_name):
    req = request.Request(MASHAPE_BASE_URL + "/summoner/retrieveInProgressSpectatorGameInfo/{0}".format(safe_str(summoner_name).replace(" ", "")))
    authenticate_mashape_request(req)
    game_info = get_json(req)
    return game_info if not game_info.get('error') else None

def get_summoner_id(summoner):
    data = get_json(build_api_url("/v1.4/summoner/by-name/" + summoner))
    return data[next(iter(data))]["id"]

def get_json(url, encoding="utf-8"):
    return json.loads(request.urlopen(url).read().decode(encoding))

def safe_str(string):
    if isinstance(string, str):
        return string
    
    try:
        return str(string.encode('utf-8'))
    except TypeError:
        return str(string)

def build_api_url(path, params=None):
    if not params:
        params = {}
    
    params["api_key"] = RIOT_CLIENT_KEY
    return RIOT_BASE_URL + path + '?' + parse.urlencode(params)

def build_static_api_url(path, params=None):
    if not params:
        params = {}
    
    params["api_key"] = RIOT_CLIENT_KEY
    return RIOT_BASE_URL + path + '?' + parse.urlencode(params)

if __name__ == "__main__":
    main()