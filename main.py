'''
Created on Sep 12, 2014

@author: alexwyler
'''
from urllib import parse, request
import players
import json
import platform
import league_runner
import time
import threading
import champion
import irc_bot
import twitch

#
# mock active_games module
#
class active_games:
    LOCK = threading.RLock()
    ACTIVE_PERSONALITIES = {}

RIOT_CLIENT_KEY = "17e7c567-e54e-4995-bf0f-9d1c9dd3722c"
MASHAPE_BASE_URL = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA/"
RIOT_BASE_URL = "https://na.api.pvp.net/api/lol/static-data/na"

GAME_TYPES = ['RANKED_SOLO_5x5']

IN_GAME_PING_FREQUENCY = 5
SPECTATOR_DELAY = 3 * 60

def init():
    irc_bot.init()

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
            
            league_runner.open_game(spectate_info, team_str, position)
            if platform.system() != 'Darwin':
                league_runner.open_game_pc()
            else:
                league_runner.open_game_mac(spectate_info, team_str, position)
                pass
            
            print("Waiting for game to end...")
            while True:
                try:
                    if get_active_game(account): 
                        break
                except Exception:
                    pass
                time.sleep(IN_GAME_PING_FREQUENCY)
            
            print("Game complete. Waiting for spectator delay...")
            time.sleep(SPECTATOR_DELAY)
            
            print("Killing game..")
            league_runner.kill_game()

        else:
            print("No active games!")
    
    pass

def get_player_position( account, running_game_info ):
    team_1 = running_game_info['game']['teamOne']['array']
    team_2 = running_game_info['game']['teamTwo']['array']
    return find_player_by_name( account, team_1, team_2 )

            
#returns is found on team 1 and position
def find_player_by_name( name, team_1, team_2 ):
    internal_name = players.to_clean_name(name)
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