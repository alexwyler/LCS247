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

GAME_TYPES = ['RANKED_SOLO_5x5']

IN_GAME_PING_FREQUENCY = 5
SPECTATOR_DELAY = 3 * 60

def init():
    irc_bot.init()
    active_games.init()

def main():
    init()
    
    while True:
        print('Searching for suitable games...')
        active_games.lock.acquire()
        selected_game_details = None
        for personality_name in active_games.ACTIVE_PERSONALITIES:
            selected_game_details = active_games.ACTIVE_PERSONALITIES[personality_name]
            break
        active_games.lock.release()
        if not selected_game_details:
            print('No suitable games found...')
        else:
            account, _, game_info = selected_game_details
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
                    if api.get_active_game(account): 
                        break
                except Exception:
                    pass
                time.sleep(IN_GAME_PING_FREQUENCY)
             
            print("Game complete. Waiting for spectator delay...")
            time.sleep(SPECTATOR_DELAY)
             
            print("Killing game..")
            league_runner.kill_game()
        time.sleep(10)

'''
Returns tuple of (player, account, game_info) for the most popular current game
'''
def get_next_game():
    for player in players.PLAYERS:
        print("Player: " + player)
        for summoner in players.PLAYERS[player]:
            try:
                next_game = api.get_active_game(summoner)
                if next_game and next_game['game']['queueTypeName'] in GAME_TYPES:
                    return (player, summoner, next_game)
            except Exception as e:
                print('For '  + util.safe_str(summoner) + ': ', e)
    return (None, None, None)

def update_twitch_channel(player, account, game_info):
    champ_name = champion.get_champion_name_from_game_info(account, game_info)
    title = 'LCS Players 24/7: {0} Playing {1}'.format(player, champ_name)
    twitch.update_channel_title(title)

if __name__ == "__main__":
    main()