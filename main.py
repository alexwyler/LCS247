'''
Created on Sep 12, 2014

@author: alexwyler
'''
import league_runner
import time
import irc_bot
import twitch
import api
import util
import active_games
import config
import players
import plog
import os
import traceback

IN_GAME_PING_FREQUENCY = 5
START_TIME = time.time()

class SharedGameDetails:
    selected_game = None

def init():
    irc_bot.init(SharedGameDetails)
    active_games.init()

def main():
    init()
    while True:
        log('Waiting for a suitable game...')
        # reduce search delay while we search for new games
        active_games.SEARCH_DELAY = 10
        while True:
            SharedGameDetails.selected_game = get_best_suitable_game()
            if not SharedGameDetails.selected_game:
                time.sleep(1)
            else:
                break

        # increase search delay while we have a game
        active_games.SEARCH_DELAY = 120
        personality_name, account, _, game = SharedGameDetails.selected_game
        log("Choosing {0} game, playing on {1}...".format(personality_name, account))
        players.hype_personality(personality_name, 10)
        
        team, position = util.get_player_position(account[0], game)
        team_str = str(team).join(str(team).split()).lower()
        
        if not config.CONTEXT_UTIL.get("skip_launch"):
            log("Launching game...")   
            league_runner.open_game(game, team_str, position)
        
        update_twitch_channel(personality_name, account, game)
        update_obs_now_playing(personality_name, account, game)
        log("Waiting for game to end...")
        while True:
            try:
                if not api.get_active_game(account[0]) or not SharedGameDetails.selected_game:
                    break
            except Exception as e:
                log(str(e))
                traceback.print_exc()
                pass
            time.sleep(IN_GAME_PING_FREQUENCY)
        
        if SharedGameDetails.selected_game:
            log("Game complete. Waiting for spectator delay...")
            time.sleep(util.SPECTATOR_DELAY)
         
        log("Killing game...")
        league_runner.kill_game()
        
        log("Decaying hype...")
        
def get_best_suitable_game():
    suitable_games = active_games.get_potential_games_in_order()
    if suitable_games:
        for suitable_game in suitable_games:
            (_, _, score, game) = suitable_game
            if not game.is_within_spectator_delay() and score > 0:
                return suitable_game
    else:
        return None

def update_obs_now_playing(player, account, game):
    champ_name = game.get_champion(account[0])
    now_playing = '{0} Playing {1}'.format(player, champ_name)
    log('Updating now playing to: "{0}"...'.format(now_playing))
    f = open(os.path.join('obs', 'now_playing.txt'), 'w')
    f.write(now_playing)
    f.close()

def update_twitch_channel(player, account, game):
    champ_name = game.get_champion(account[0])
    title = 'LCS Players 24/7: {0} Playing {1}'.format(player, champ_name)
    log('Updating twitch stream to: "{0}"...'.format(title))
    twitch.update_channel_title(title)

def log(message):
    plog.log('main', message)
    
if __name__ == "__main__":
    main()
