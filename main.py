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

IN_GAME_PING_FREQUENCY = 5
START_TIME = time.time()

def init():
    config.init()
    irc_bot.init()
    active_games.init()

def main():
    init()
    
    while True:
        print('[ main ]\t Searching for suitable games...')
        # reduce search delay while we search for new games
        active_games.SEARCH_DELAY = 10
        while True:
            selected_game_details = get_best_suitable_game()
            if not selected_game_details:
                time.sleep(1)
            else:
                break

        # increase search delay while we have a game
        active_games.SEARCH_DELAY = 120
        personality_name, account, _, game = selected_game_details
        print("[ main ]\t Chose {0} game, playing on {1}...".format(personality_name, account))
        
        team, position = util.get_player_position(account, game)
        team_str = str(team).join(str(team).split()).lower()
        
        if not config.CONTEXT_UTIL.get("skip_launch"):
            print("[ main ]\t Launching game...")
            league_runner.open_game(game, team_str, position)
        
        update_twitch_channel(personality_name, account, game)
        print("[ main ]\t Waiting for game to end...")
        while True:
            try:
                if not api.get_active_game(account): 
                    break
            except Exception:
                pass
            time.sleep(IN_GAME_PING_FREQUENCY)
         
        print("[ main ]\t Game complete. Waiting for spectator delay...")
        time.sleep(util.SPECTATOR_DELAY)
         
        print("[ main ]\t Killing game...")
        league_runner.kill_game()
        
        print("[ main ]\t Decaying hype...")
        
def get_best_suitable_game():
    suitable_games = active_games.get_suitable_games_in_order()
    if suitable_games:
        return suitable_games[0]
    else:
        return None

def update_twitch_channel(player, account, game):
    champ_name = game.get_champion(account)
    title = 'LCS Players 24/7: {0} Playing {1}'.format(player, champ_name)
    print('[ main ]\t Updating twitch stream to: "{0}"...'.format(title))
    twitch.update_channel_title(title)

if __name__ == "__main__":
    main()
