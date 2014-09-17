import threading
import time
import os
import active_games

global OBS_PATH

def init():
    global OBS_PATH
    OBS_PATH = os.path.dirname(__file__)
    t = threading.Thread(target=keep_potential_games_up_to_date)
    t.start()

def update_now_playing(player, account, game):
    champ_name = game.get_champion(account[0])
    now_playing = '{0} Playing {1}'.format(player, champ_name)
    f = open(os.path.join(OBS_PATH, 'obs', 'now_playing.txt'), 'w')
    f.write(now_playing)
    f.close()

def keep_potential_games_up_to_date():
    while True:
        f = open(os.path.join(OBS_PATH, 'obs', 'potential_games.txt'), 'w')
        potential_games = active_games.get_potential_games_in_order()
        if potential_games:
            f.write("--- Players in Game ---\n")
            for suitable_game in potential_games:
                personality_name, account, score, game = suitable_game
                if game.is_within_spectator_delay():
                    waiting = ', waiting to begin\n'
                else:
                    waiting = ''
                message = "({0}{3}) {1} on {2} {4}\n".format(score, personality_name, game.get_champion(account[0]), waiting, game.get_timestamp_since_start())
                f.write(message)
        else:
            f.write("No potential games!\n")
        
        f.close()
        time.sleep(5)