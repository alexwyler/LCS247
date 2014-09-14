'''
Created on Sep 12, 2014

@author: alexwyler
'''
from operator import itemgetter, attrgetter
import collections
import main
import sqlite3

POPULAR_PLAYERS = collections.OrderedDict()
PLAYERS = collections.OrderedDict()

PLAYERS['Shiptur'] = ['Shiphtur', 'mMe Shiphtur', 'Chapanya', 'CST Shiponya', 'Pawn Dog', 'Apdo Dog']
PLAYERS['Voyboy'] = ['Voyboy', 'Crs Vooby', 'Crs Voyboy', 'Nihilmatic']
PLAYERS['Dexter'] = ['dexter', 'GoldPoro2', 'LDdexter', 'OPOP174AMHA195', 'CIJL963PFPA447B', 'CLGsavior', 'CHIMPERATOR']
PLAYERS['PorpoisePops'] = ['PorpoisePops', 'vVv PorpoisePops']
PLAYERS['Slooshi'] = ['Slooshi', 'aL Slooshi', 'Slooshi8']
PLAYERS['frommaplestreet'] = ['frommaplestreet', 'Velocity Maple']
PLAYERS['Dodo8'] = ['Dodo8']
PLAYERS['Imaqtpie'] = ['Imaqtpie', 'qtpie', 'looking2sub4lcs', 'Zstinkloser430Z', 'LMQ Tc Tabe', 'Jessica Lynn', 'adsafadfdsafdasf']
PLAYERS['Pobelter'] = ['Pobelter', 'intero', 'imPobelter', 'Crs Pobelt', 'xPobelter', 'Crs Pobelter', 'Apdo Dog1', 'Wizikx']
PLAYERS['ZionSpartan'] = ['ZionSpartan'];
PLAYERS['Altec'] = ['Altec', 'xiaomx', 'AItecX', 'illustic', 'Crs Altec', 'scarraru', 'AItecRu', 'AltecX', 'C9 Altec']
PLAYERS['Aphromoo'] = ['Aphromoo', 'FeaRAphromoo', 'Veinzx', 'nJoyDrop', 'Neruma', 'TheycallmeZorro', 'LegitJJ', 'v8Aphromoo', 'Daphro', 'Zebuum', 'Zeemeeandye', 'CLGAphromoo']
PLAYERS['DoubleLift'] = ['Doublelift', 'Triplelift', 'Quadralift', 'Pentalift', 'LiftLift', 'Peng Yiliang']
PLAYERS['Balls'] = ['BalIs', 'C9 Squirtle', 'C9 Balls']
PLAYERS['Hai'] = ['hai', 'C9 HyperX Diego', 'C9 Hai', 'AndrossiBaam', 'C9 Hairo']
PLAYERS['Meteos'] = ['Meteos', 'C10 Meteos', 'C9 Meteos', 'Short Dog', 'Long Dong', 'C9 Axel']
PLAYERS['Sneaky'] = ['Sneaky', 'C9 StealthBomber', 'C9 Sneaky', 'd SnEaKyCaStRo', 'SnEaKyCaStRoO', 'Pulse CaStRo', 'Heathers Suka', 'AL SnEaKyCaStRo']
PLAYERS['LemonNation'] = ['LemonNation', 'C9 BananaNation', 'C9 HyperX Dora', 'C9 LemonNation', 'Nom Nom Lemon', 'Quantic Lemon NT', 'oRb LemonNation', 'ShawnOfTheDead', 'LemonBoy']
PLAYERS['Krepo'] = ['Kreported', 'CLG SkumbagKrepo', 'Busdriver', 'MockingBeard', 'CLG SkumbagKrepo']
PLAYERS['Crumbz'] = ['Crumbz', 'd Crumbz', 'Crumblina', 'SiAseeTnoAevilN', 'Phd Mundo', 'Sin Pact', 'Prof Crumbledore']
PLAYERS['KiWiKiD'] = ['KiWiKiD', 'Snazero8', 'TheShyOne', 'KiwiKid', 'd KiWiKid', 'WORST BOWLHAVIOR']
PLAYERS['Innox'] = ['Innox']
PLAYERS['Helios'] = ['Helios', 'QBR9WQFWE0']
PLAYERS['Seraph'] = ['Seraph', 'anik']
PLAYERS['LiNk'] = ['LiNk', 'LiNk115', 'scarra115', 'MidLink', 'linkkk', 'kTLink', 'kTZelda', 'CLGzelda']
PLAYERS['Quas'] = ['Quas', 'Crs Quas', 'gg Quas', 'nwe Quas', 'Dr Quas', 'Quasmire']
PLAYERS['Cop'] = ['Cop', 'Crs Cop', 'v8 Cop', 'EU Cop', 'David Roberson', 'KingWill84', 'crs goompa', 'bootybutts66']
PLAYERS['XPecial'] = ['Xpecial', 'TSM Xpec']

PLAYERS['DaBox'] = ['dabox']
PLAYERS['Annie Bot'] = ['anniebot']
PLAYERS['Hi Im Gosu'] = ['hi im gosu']
PLAYERS['TheOddOne'] = ['theoddone']
PLAYERS['SexyCan'] = ['sexycan']
PLAYERS['Tossum'] = ['tossum']
PLAYERS['Much Glorf Wow'] = ['muchglorfwow']
PLAYERS['Bwas'] = ['bwas']
PLAYERS['LattMan'] = ['lattman']

TABLE_PLAYER_HYPE = "player_hype"

class Player:
    def __init__(self, hype, clean_name, nicks):
        self.hype = hype
        self.clean_name = clean_name
        self.nicks = nicks
    def __repr__(self):
        return repr((self.hype, self.clean_name, self.nicks))
    
    def init_from_db(self, hype, clean_name, encoded_nicks ):
        self.hype = hype
        self.clean_name = clean_name
        self.nicks = decode_nicks(encoded_nicks)
        
    
def encode_nicks( player ):
    return ",".join( player.nicks )

def decode_nicks( encoded_nicks ):
    return encoded_nicks.split(",")


'''
Hypes a player in the popular player dictionary, creates an enty if the player does not exist
stores the player as the clean version (lower case, space stripped) contains a list of nicknames
that were used to create the clean version

'''
  
def hypePlayer( player ):
    clean_name = main.stripSpaceAndLower(player)
     
    if( clean_name not in POPULAR_PLAYERS.keys() ):
        newPlayer = Player(1, clean_name, [player])
        POPULAR_PLAYERS.setdefault(clean_name, newPlayer)
    else:
        oldPlayer = POPULAR_PLAYERS[clean_name]
        if player not in oldPlayer.nicks:
            oldPlayer.nicks.append(player)
        oldPlayer.hype += 1
        POPULAR_PLAYERS[clean_name] = oldPlayer
    pass

def get_sorted_list():
    return sorted( POPULAR_PLAYERS, key= lambda x:POPULAR_PLAYERS[x].hype, reverse = True )

def insert_player( player ):
    encoded_nicks = encode_nicks(player)
    
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    
    ins = 'INSERT INTO '+TABLE_PLAYER_HYPE+' VALUES '+"('"+str(player.hype)+"','"+str(player.clean_name)+"','"+str(encoded_nicks)+"');"
    c.execute( ins )
    
    conn.commit()
    conn.close()
    pass

def get_player_hype_list():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    get = 'SELECT * FROM ' + TABLE_PLAYER_HYPE + ";"
    c.execute( get )
     
    for s in c.fetchall():
        print("---")
        print( s )
        
#     for db_player in 
#     print( type(user), user.name, user.password )
    
    conn.close()
     
    pass

def test():
    
    for player in PLAYERS:
        for summoner in PLAYERS[player]:
            hypePlayer(summoner)

    hypePlayer( "Imaqtpie" )
    hypePlayer( "ImaqtpIe" )
    hypePlayer( "ImAqtpIe" )
    hypePlayer( "new player" )
    hypePlayer( "Quas" )
    hypePlayer( "quaS" )
    hypePlayer( "quAs" )
    hypePlayer( "QuAs" )
    hypePlayer( "qUaS" )
    
#     insert_player( POPULAR_PLAYERS[get_sorted_list()[0]] )
    
#     conn = sqlite3.connect('players.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE player_hype(hype int, clean_name text, nicks text)''')
    
    
#     insert_player( POPULAR_PLAYERS[get_sorted_list()[1]] )
     
#     for player in get_sorted_list():
#         print(POPULAR_PLAYERS[player])
#         print( ",".join(POPULAR_PLAYERS[player].nicks) )
#     pass

    get_player_hype_list()


if __name__ == "__main__":
    test();
    
    
    
    
    
    
    
    
    
    
    
    
    
    