'''
Created on Sep 12, 2014

@author: alexwyler
'''
from urllib import parse, request
TWITCH_ACCESS_TOKEN = '4x0axpb122pjsartbzar50pcg93ityz'
TWITCH_BASE_URL = 'https://api.twitch.tv/kraken'
TWITCH_CHANNEL_NAME = 'LCS247'

def update_channel_title( title ):
    url = TWITCH_BASE_URL + '/channels/{0}'.format(TWITCH_CHANNEL_NAME) + '?' + parse.urlencode({'oauth_token': TWITCH_ACCESS_TOKEN})
    data = parse.urlencode({'channel[status]': title}).encode()
    req = request.Request(url, data=data)
    req.add_header('Accept', 'application/vnd.twitchtv.v2+json')
    req.get_method = lambda: 'PUT'
    request.urlopen(req).read()