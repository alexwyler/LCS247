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


ACTIVE_PERSONALITIES = collections.OrderedDict()
lock = threading.Lock()

def get_tracked_list():
    tracked_list = [];
    for player in players.PLAYERS:
        for summoner in players.PLAYERS[player]:
            tracked_list.append(summoner)
    
    return tracked_list

def lookup_account( personality, account ):
    print( "Looking up: " + account )
    game_info = api.get_active_game( account )
    if game_info:
        print( "account: " + account )
        print( "game info: " + str(game_info))
        ACTIVE_PERSONALITIES[personality['name']] = (account, game_info)
        
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
    
    players.hype_personality("nightblue3", 1)
    
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [ executor.submit( lookup_account, players.get_personality_for_account_name(account), account ) 
                   for account in players.get_accounts_with_hype() ]
#             
        results = concurrent.futures.wait( futures )
#        
# #         for completed in results.done:
# #             print(   )
#         
        end = time.time()
        print( end-start )
        print("\n")
        
        print( "size: " + str(len(ACTIVE_PERSONALITIES)))
         
        for personality in ACTIVE_PERSONALITIES:
            print( personality )
#         
#         
# #             res = lookup_account( account )
# #             if res:
# #                 personality = get_personality_from_account( account )
# #                 print( personality )
# #     #             ACTIVE_PERSONALITIES.setdefault(key, default)
# #                 print(res)
    
    
    pass

if __name__ == "__main__":
    testTime();
    
    
    
    
    
    
    
    
    
    
    
    
    
    