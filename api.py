'''
Created on Sep 14, 2014

@author: alexwyler
'''
from urllib import request, parse
import json
import util

RIOT_API_KEY = "28d9db1d-f4cc-41ff-b3d1-7e75687cd723"
RIOT_BASE_URL = 'https://na.api.pvp.net/api/lol'

MASHAPE_BASE_URL = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA"

def authenticate_mashape_request(req):
    req.add_header("X-Mashape-Key", "RQk9vZZLGQmshgjK5Yg8nsx5rz4Ep1SJ5I5jsneUxclaP4OTJR")
    return req

def get_active_game(summoner_name):
    req = request.Request(MASHAPE_BASE_URL + "/summoner/retrieveInProgressSpectatorGameInfo/{0}".format(util.safe_str(summoner_name).replace(" ", "")))
    authenticate_mashape_request(req)
    game_info = get_json(req)
#     print( str(game_info) )
    return game_info if not game_info.get('error') else None

def get_json(url, encoding="utf-8"):
#     print(url)
    return json.loads(request.urlopen(url).read().decode(encoding))

def build_api_url(path, params=None):
    if not params:
        params = {}
    
    params["api_key"] = RIOT_API_KEY
    return RIOT_BASE_URL + path + '?' + parse.urlencode(params)