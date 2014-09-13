'''
Created on Sep 12, 2014

@author: alexwyler
'''
from urllib import parse, request
import players
import json

RIOT_CLIENT_KEY = "17e7c567-e54e-4995-bf0f-9d1c9dd3722c"
MASHAPE_BASE_URL = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA/"
RIOT_BASE_URL = "https://na.api.pvp.net/api/lol/na"

def main():
    (player, account, game_info) = get_next_game()
    print(player, account, game_info['playerCredentials'])

'''
Returns tuple of (player, account, game_info) for the most popular current game
'''
def get_next_game():
    for player in players.PLAYERS:
        for summoner in players.PLAYERS[player]:
            next_game = get_active_game(summoner)
            if next_game:
                return (player, summoner, next_game)
    return None
            

def authenticate_mashape_request(req):
    req.add_header("X-Mashape-Key", "RQk9vZZLGQmshgjK5Yg8nsx5rz4Ep1SJ5I5jsneUxclaP4OTJR")
    return req

def get_active_game(summoner_name):
    req = request.Request(MASHAPE_BASE_URL + "/summoner/retrieveInProgressSpectatorGameInfo/{0}".format(summoner_name))
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