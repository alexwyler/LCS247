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
import config
import active_games

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
        print('Searching for suitable games...')
        selected_game_details = get_best_suitable_game()
        if not selected_game_details:
            pass
        else:
            personality_name, account, game_info = selected_game_details
            spectate_info = game_info['playerCredentials'];
            print(personality_name, account, spectate_info)
            team, position = util.get_player_position(account, game_info)
            team_str = str(team).join(str(team).split()).lower()
            print( "Position found: " + team_str + ", " + str(position) )
 
            print( update_twitch_channel(personality_name, account, game_info) )
             
            league_runner.open_game(spectate_info, team_str, position)
             
            print("Waiting for game to end...")
            while True:
                try:
                    if not api.get_active_game(account): 
                        break
                except Exception:
                    pass
                time.sleep(IN_GAME_PING_FREQUENCY)
             
            print("Game complete. Waiting for spectator delay...")
            time.sleep(SPECTATOR_DELAY)
             
            print("Killing game..")
            league_runner.kill_game()
        time.sleep(20)

def get_best_suitable_game():
    personalities_by_hype = players.get_personality_names_ordered_by_hype()
    active_games.lock.acquire()
    try:
        for personality_name in personalities_by_hype:
            active_game_info = active_games.ACTIVE_PERSONALITIES.get(personality_name)
            if not active_game_info:
                continue
            (account, start_time, game_info) = active_game_info
            time_since_start = time.time() - start_time
            time_since_init = time.time() - START_TIME
            CHECK_FOR_FULL_GAMES = False
            if (CHECK_FOR_FULL_GAMES and time_since_init > 3 * 60 and time_since_start < 3 * 60) or time_since_start > 10 * 60:
                print(personality_name + " game not close enough to start! " + str(time_since_start / 60) + " minutes in.")
                continue
        
#             if game_info['game']['queueTypeName'] != 'RANKED_SOLO_5x5':
#                 print(personality_name + " game not ranked 5s!")
#                 continue
            
            return (personality_name, account, game_info)
            
            break
    finally:
        active_games.lock.release()

def update_twitch_channel(player, account, game_info):
    champ_name = champion.get_champion_name_from_game_info(account, game_info)
    title = 'LCS Players 24/7: {0} Playing {1}'.format(player, champ_name)
    twitch.update_channel_title(title)

if __name__ == "__main__":
    main()