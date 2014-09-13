'''
Created on Sep 12, 2014

@author: alexwyler
'''
from urllib import parse, request
import players

RIOT_CLIENT_KEY = "17e7c567-e54e-4995-bf0f-9d1c9dd3722c"
RIOT_BASE_URL = "https://na.api.pvp.net/api/lol/na/v1.4"

def main():
    
    for player in players.PLAYERS:
        for summoner in players.PLAYERS[player]:
            print(request.urlopen(build_api_url("/summoner/by-name/" + summoner)).read())


def build_api_url(path, params=None):
    if not params:
        params = {}
    
    params["api_key"] = RIOT_CLIENT_KEY
    return RIOT_BASE_URL + path + '?' + parse.urlencode(params)

if __name__ == "__main__":
    main()