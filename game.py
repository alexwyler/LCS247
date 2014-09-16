'''
Created on Sep 15, 2014

@author: alexwyler
'''
import util
import time
import datetime

class Game:
    
    def __init__(self):
        self.server = None
        self.port = None
        self.version = None
        self.game_id = None
        self.key = None
        self.region = None
        self.start_time = None
        self.blue_team = None
        self.purple_team = None
        self.type = None
        
    def __str__(self):
        return str(self.__dict__)
    
    def is_within_spectator_delay(self):
        return self.get_time_since_start() < (util.SPECTATOR_DELAY + 30)
    
    def get_time_since_start(self):
        return time.time() - self.start_time
    
    def get_timestamp_since_start(self):
        return str(datetime.timedelta(seconds=int(int(time.time() - self.start_time))))
    
    def get_champion(self, account):
        for player_info in self.blue_team + self.purple_team:
            if util.to_clean_name(player_info['account']) == util.to_clean_name(account):
                return player_info['champion']
            