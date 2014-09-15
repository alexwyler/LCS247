'''
Created on Sep 12, 2014

@author: alexwyler
'''
import players
import league_runner
import time
import champion
import irc_bot
import twitch
import api
import util
import active_games
import config

IN_GAME_PING_FREQUENCY = 5
SPECTATOR_DELAY = 3 * 60
START_TIME = time.time()

def init():
    config.init()
    irc_bot.init()
    active_games.init()

def main():
    init()
    
    while True:
        print('[ main ]\t Searching for suitable games...')
        while True:
            selected_game_details = get_best_suitable_game()
            if not selected_game_details:
                time.sleep(1)
            else:
                break

        personality_name, account, game = selected_game_details
        print("[ main ]\t Chose {0} game, playing on {1}...".format(personality_name, account))
        
        team, position = util.get_player_position(account, game)
        team_str = str(team).join(str(team).split()).lower()
        
        if not config.CONTEXT_UTIL.get("skip_launch"):
            print("[ main ]\t Launching game...")
            league_runner.open_game(game, team_str, position)
         
        print("[ main ]\t Waiting for game to end...")
        while True:
            try:
                if not api.get_active_game(account): 
                    break
            except Exception:
                pass
            time.sleep(IN_GAME_PING_FREQUENCY)
         
        print("[ main ]\t Game complete. Waiting for spectator delay...")
        time.sleep(SPECTATOR_DELAY)
         
        print("[ main ]\t Killing game...")
        league_runner.kill_game()

def get_best_suitable_game():
    personalities_by_hype = players.get_personality_names_ordered_by_hype()
    active_games.lock.acquire()
    try:
        for personality_name in personalities_by_hype:
            active_game_info = active_games.ACTIVE_PERSONALITIES.get(personality_name)
            if not active_game_info:
                continue
            (account, start_time, game) = active_game_info
            time_since_start = time.time() - start_time
            
            if (config.CONTEXT_UTIL.get("enforce_spectator_delay_after_start") and time_since_start < 3 * 60) or time_since_start > 10 * 60:
#                print(personality_name + " game not close enough to start! " + str(time_since_start / 60) + " minutes in.")
                continue
        
            if game.type != 'Ranked Solo 5v5' and config.CONTEXT_UTIL.get("enforce_solo_queue"):
#                print(personality_name + " game not ranked 5s!")
                continue
            
            return (personality_name, account, game)
            
            break
    finally:
        active_games.lock.release()

def update_twitch_channel(player, account, game_info):
    champ_name = champion.get_champion_name_from_game_info(account, game_info)
    title = 'LCS Players 24/7: {0} Playing {1}'.format(player, champ_name)
    print('[ main ]\t Updating twitch stream to: "{0}"...'.format(title))
    twitch.update_channel_title(title)

if __name__ == "__main__":
    main()
