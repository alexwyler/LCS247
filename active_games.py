'''
Created on Sep 12, 2014

@author: alexwyler
'''
import collections
import concurrent.futures
import concurrent
import time
from turtle import done

import main
from players import Player
import players


ACTIVE_PERSONALITIES = collections.OrderedDict()

def get_tracked_list():
    tracked_list = [];
    for player in players.PLAYERS:
        for summoner in players.PLAYERS[player]:
            tracked_list.append(summoner)
    
    return tracked_list

def lookup_account( personality, account ):
#   do something to get the name
    name = account
    print( "Looking up: " + name )
    game_info = main.get_active_game(name)
    if game_info:
#         print( game_info )
        ACTIVE_PERSONALITIES.setdefault(personality, (name, game_info) )
    pass

def get( accounts ):
    
#    get the personality by account
    
    pass

def get_personality_from_account( account_name ):
    for personality in players.PLAYERS:
        for summoner in players.PLAYERS[personality]:
            if account_name == summoner:
                return personality
    pass

def testSimple( amount, name ):
    time.sleep( amount );
    print("done with: " + name)
    return name

def testPool():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        for x in range(0, 30):
            future1 = executor.submit( testSimple, 2, "f"+str(x) );
        
#         print( future1.result() )
#         print( future2.result() )
#         print( future3.result() )
    
    pass

def testTime():
    
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [ executor.submit( lookup_account, get_personality_from_account(account), account ) for account in get_tracked_list() ]
            
        results = concurrent.futures.wait( futures )
       
#         for completed in results.done:
#             print(   )
        
        end = time.time()
        print( end-start )
        print("\n")
        
        for personality in ACTIVE_PERSONALITIES:
            print( personality + " - " + str(ACTIVE_PERSONALITIES[personality]))
        
        
#             res = lookup_account( account )
#             if res:
#                 personality = get_personality_from_account( account )
#                 print( personality )
#     #             ACTIVE_PERSONALITIES.setdefault(key, default)
#                 print(res)
    
    
    pass

if __name__ == "__main__":
    testTime();
    
    
    
    
    
    
    
    
    
    
    
    
    
    