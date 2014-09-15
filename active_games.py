'''
Created on Sep 12, 2014

@author: alexwyler
'''
import concurrent.futures
import threading
import time
import util
import datetime
import config
import traceback

import api
import players

GAME_TYPES = ['Normal 5v5', 'Ranked Solo 5v5']
MAX_START_TIME = 10 * 60
ACTIVE_PERSONALITIES = {}
ACTIVE_ACCOUNTS = {}
lock = threading.Lock()

SEARCH_DELAY = 5

def get_tracked_list():
    tracked_list = [];
    for player in players.PLAYERS:
        for summoner in players.PLAYERS[player]:
            tracked_list.append(summoner)
    
    return tracked_list

def lookup_account( personality, account ):
    try:
#         print( "Looking up: " + account )
        game = api.get_game_info_from_lolnexus( account )
        personality_name = personality['name']
        lock.acquire()
        try:
            # initialize dict
            if not personality_name in ACTIVE_ACCOUNTS:
                ACTIVE_ACCOUNTS[personality_name] = {}
            
            accounts_to_games = ACTIVE_ACCOUNTS[personality_name]
            if game:
                duration = str(datetime.timedelta(seconds=int(int(time.time() - game.start_time))))
                if account not in accounts_to_games:
                    print("[ search ]\t New game, " + personality_name + ", " + game.type + ", " + duration)
                    accounts_to_games[account] = (account, time.time(), game)
            else:
                if account in accounts_to_games:
                    print("[ search ]\t Deleting game, " + personality_name )
                    accounts_to_games.pop(account, None)
        finally:
            lock.release()
    except Exception as e:
        pass
        print(account)
        print('[ search ]\t Error looking up game: ' + str(e))
        traceback.print_exc()

#             

        
#         lock.acquire()
#         try:
#             print("inside try")
#         if personality not in ACTIVE_PERSONALITIES:
#             print( "------Found: " + personality + " in " + account )
#             ACTIVE_PERSONALITIES[personality] = (account, (name, game_info) )
#         else:
#             print( account + " already in active personalities" )
#         finally:
#             print("finally")
#             lock.release()

def get_personality_from_account( account_name ):
    for personality in players.PLAYERS:
        for summoner in players.PLAYERS[personality]:
            if account_name == summoner:
                return personality
            
def update():
    hyped_accounts = players.get_accounts_with_hype()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [ executor.submit( lookup_account, players.get_personality_for_account_name(account), account ) 
                   for account in  hyped_accounts]
                     
        concurrent.futures.wait( futures )
        
        lock.acquire()
        try:
            for personality_name in ACTIVE_ACCOUNTS:
                has_game = False
                for account in ACTIVE_ACCOUNTS[personality_name]:
                    has_game = True
                    ACTIVE_PERSONALITIES[personality_name] = ACTIVE_ACCOUNTS[personality_name][account]
                if not has_game:
                    ACTIVE_PERSONALITIES.pop(personality_name, None)
            pass
        finally:
            lock.release()
        
        
#         for completed in result.done:
#             print( completed )
#        print("Completed scan of " + str(len(hyped_players)) + " hyped players. " + str(len(ACTIVE_PERSONALITIES)) + " found in game...")

def update_runner():
    print('[ search ]\t Searching for active games...')
    while True:
        update()
        time.sleep(SEARCH_DELAY)
        
        
def get_suitable_games_in_order():
    personalities_by_hype = players.get_personalities_by_hype()
    suitable_games = []
    lock.acquire()
    try:
        for personality in personalities_by_hype:
            personality_name = personality['name']
            active_game_info = ACTIVE_PERSONALITIES.get(personality_name)
            if not active_game_info:
                continue
            (account, _, game) = active_game_info
            time_since_start = time.time() - game.start_time
            
            if time_since_start < util.SPECTATOR_DELAY or time_since_start > MAX_START_TIME:
#                print(personality_name + " game not close enough to start! " + str(time_since_start / 60) + " minutes in.")
                continue
        
            if game.type not in GAME_TYPES and config.CONTEXT_UTIL.get("enforce_solo_queue"):
#                print(personality_name + " game not ranked 5s!")
                continue
            
            suitable_games.append((personality_name, account, personality['hype'], game))
            
    finally:
        lock.release()
    
    return suitable_games        

def init():
    
    update_thread = threading.Thread( target=update_runner )
    update_thread.start()
    
    
    pass

if __name__ == "__main__":
    init();
    
    
    
    
    
    
    
    
    
    
    
    
    
    