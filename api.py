'''
Created on Sep 14, 2014

@author: alexwyler
'''
from urllib import request, parse
from game import Game
import json
import util
import re

RIOT_API_KEY = "28d9db1d-f4cc-41ff-b3d1-7e75687cd723"
RIOT_BASE_URL = 'https://na.api.pvp.net/api/lol'

# 1 - game start time
GAME_TIME_RE = re.compile('data-game-time="(.*)"')

# 1 - server
# 2 - port
# 3 - key
# 4 - game_id
# 5 - region
# 6 - version
SPECTATOR_DATA_RE = re.compile('href="lrf://spectator (.*):(.*) (.*) (.*) (.*) (.*)"')

# 1 - account name
PLAYER_RE = re.compile('\\.op\\.gg/summoner/userName=(.*)" target="outbound"')
CHAMPION_NAME_RE = re.compile('<span>(.*)\r\\s+\\(<b class="num-games tip"')
QUEUE_RE = re.compile("Summoner&#x27;s Rift, (.*) - ")

MASHAPE_BASE_URL = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA"

def authenticate_mashape_request(req):
    req.add_header("X-Mashape-Key", "RQk9vZZLGQmshgjK5Yg8nsx5rz4Ep1SJ5I5jsneUxclaP4OTJR")
    return req

def get_active_game(summoner_name):
    req = request.Request(MASHAPE_BASE_URL + "/summoner/retrieveInProgressSpectatorGameInfo/{0}".format(util.to_clean_name(summoner_name)))
    authenticate_mashape_request(req)
    game_info = get_json(req)
#     print( str(game_info) )
    return game_info if not game_info.get('error') else None

def get_json(url_or_req, encoding="utf-8"):
#     print(url)
    return json.loads(request.urlopen(url_or_req).read().decode(encoding))

def build_api_url(path, params=None):
    if not params:
        params = {}
    
    params["api_key"] = RIOT_API_KEY
    return RIOT_BASE_URL + path + '?' + parse.urlencode(params)

def get_game_info_from_lolnexus(account):
    if account[1] == 'KR':
        return None
    data = parse.urlencode({'name': account[0]}).encode('utf-8')
    req = request.Request('http://www.lolnexus.com/ajax/get-game-info/{0}.json?name={1}'.format(account[1], account[0]), data=data)
    response = get_json(req)
    if not response.get('successful'):
        return None
    
    html = response['html']
    
#     f1 = open('./testfile', 'w+', encoding='utf-8')
#     f1.write(html)
        
    match = QUEUE_RE.search(html)
    if not match:
        return None
    game_type = match.group(1)
    
    match = GAME_TIME_RE.search(html)
    if not match:
        return None
    start_time = int(match.group(1))
    
    match = SPECTATOR_DATA_RE.search(html)
    if not match:
        return None
    
    (server, port, key, game_id, region, version) = match.group(1, 2, 3, 4, 5, 6)
    
    blue_team = []
    purple_team = []
    
    player_matches = re.findall(PLAYER_RE, html)
    champion_matches = re.findall(CHAMPION_NAME_RE, html)
    
    for i in range(5):
        blue_team.append({
            'account': player_matches[i],
            'champion': champion_matches[i]
        })
        purple_team.append({
            'account': player_matches[i + 5],
            'champion': champion_matches[i + 5]
        })
    
    game = Game()
    game.server = server
    game.port = port
    game.key = key
    game.game_id = game_id
    game.region = region
    game.version = version
    game.start_time = start_time
    game.blue_team = blue_team
    game.purple_team = purple_team
    game.type = game_type
    
    return game
    
if __name__ == '__main__':
    print(get_game_info_from_lolnexus(('Imaqtpie', 'NA')))
    
