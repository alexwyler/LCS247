'''
Created on Sep 15, 2014

@author: alexwyler
'''

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
        
    def __str__(self):
        return str(self.__dict__)