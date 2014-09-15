'''
Created on Sep 12, 2014

@author: alexwyler
'''
import collections
import concurrent.futures
import threading
import time

import api
import players

ACTIVE_PERSONALITIES = {}
ACTIVE_ACCOUNTS = {}
lock = threading.Lock()

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
        # initialize dict
        lock.acquire()
        try:
            if not personality_name in ACTIVE_ACCOUNTS:
                ACTIVE_ACCOUNTS[personality_name] = {}
            
            accounts_to_games = ACTIVE_ACCOUNTS[personality_name]
            if game:
                print( "account: " + account )
                print( "personality:" + personality['name'] )
                if account not in accounts_to_games:
                    print("--- New Game --- " + personality_name )
                    accounts_to_games[account] = (account, time.time(), game)
            else:
                if account in accounts_to_games:
                    print("--- Deleting Game --- " + personality_name )
                    accounts_to_games.pop(account, None)
        finally:
            lock.release()
    except Exception as e:
        pass
        print('Error looking up game: ' + str(e))
        #traceback.print_exc()

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
    hyped_players = players.get_accounts_with_hype()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [ executor.submit( lookup_account, players.get_personality_for_account_name(account), account ) 
                   for account in  hyped_players]
                     
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
        print("Completed scan of " + str(len(hyped_players)) + " hyped players. " + str(len(ACTIVE_PERSONALITIES)) + " found in game...")

def update_runner():
    while True:
        update()
        time.sleep(1)
        
def init():
    
    update_thread = threading.Thread( target=update_runner )
    update_thread.start()
    
    
    pass

if __name__ == "__main__":
    init();
    
    
    
    
    
    
    
    
    
    
    
    
    
    