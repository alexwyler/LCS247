'''
Created on Sep 12, 2014

@author: alexwyler
'''
import collections
import concurrent.futures
import threading
import time
import traceback

import api
import players


ACTIVE_PERSONALITIES = collections.OrderedDict()
lock = threading.Lock()

def get_tracked_list():
    tracked_list = [];
    for player in players.PLAYERS:
        for summoner in players.PLAYERS[player]:
            tracked_list.append(summoner)
    
    return tracked_list

def lookup_account( personality, account ):
    try:
        #print( "Looking up: " + account )
        game_info = api.get_active_game( account )
        personality_name = personality['name']
        if game_info:
            #print( "account: " + account )
            #print( "game info: " + str(game_info))
            #print( "personality:" + personality['name'] )
            
            if personality_name not in ACTIVE_PERSONALITIES:
                print("--- Adding " + personality_name )
                ACTIVE_PERSONALITIES[personality_name] = (account, time.time(), game_info)
        else:
            #print("--- Delete" + personality_name )
            ACTIVE_PERSONALITIES.pop(personality_name, None)
    except Exception as e:
        #print('Error looking up game: ' + str(e))
        #traceback.print_exc()
        pass
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [ executor.submit( lookup_account, players.get_personality_for_account_name(account), account ) 
                   for account in players.get_accounts_with_hype() ]
                     
        result = concurrent.futures.wait( futures )
        
#         for completed in result.done:
#             print( completed )
             
        #print( "size: " + str(len(ACTIVE_PERSONALITIES)))

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    