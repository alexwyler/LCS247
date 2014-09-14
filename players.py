'''
Created on Sep 12, 2014

@author: alexwyler
'''
import collections
import sqlite3

POPULAR_PLAYERS = collections.OrderedDict()

def lazy_init():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personalities'")
    if not cursor.fetchone():
        init_data()

def hype_account( account_name, amount ):
    personality = get_personality_for_account_name(account_name)
    if personality:
        conn = get_conn()
        cursor=conn.cursor()
        cursor.execute("UPDATE personalities SET hype = hype + ? where name = ?", (amount, personality['name']))
        conn.commit()
        conn.close()

def dict_factory(cursor, row):
    d = {}   
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
        
def get_conn():
    conn = sqlite3.connect('players.db')
    conn.row_factory = dict_factory
    return conn

def to_clean_name(account_name):
    return account_name.replace(" ", "").lower()

def get_personality_for_account_name(account_name):
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute("SELECT name, hype FROM personalities as p inner join accounts as a on p.name = a.personality_name where a.clean_name = ?", (to_clean_name(account_name),))
    personality = cursor.fetchone()
    conn.close()
    return personality

def get_personality(name):
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute("SELECT name, hype FROM personalities where name = ?", (name,))
    personality = cursor.fetchone()
    conn.close()
    return personality

def get_sorted_list():
    return sorted( POPULAR_PLAYERS, key= lambda x:POPULAR_PLAYERS[x].hype, reverse = True )
    
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

def init_data():
    conn = get_conn()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS personalities")
    c.execute("CREATE TABLE personalities(name varchar, hype int(11))")
    c.execute("DROP TABLE IF EXISTS accounts")
    c.execute("CREATE TABLE accounts(clean_name varchar, display_name varchar, region varchar, personality_name varchar)")
    conn.commit()
    for personality_name in PLAYERS:
        c.execute("INSERT INTO personalities (name, hype) VALUES (?, 0)", (personality_name,))
        for account_name in PLAYERS[personality_name]:
            c.execute("INSERT INTO accounts (clean_name, display_name, region, personality_name) VALUES (?, ?, 'NA', ?)", (to_clean_name(account_name), account_name, personality_name))
    conn.commit()
    conn.close()

lazy_init()

def test():
    print(get_personality('Voyboy'))
    hype_account("Voyboy", 1)
    print(get_personality_for_account_name('crs vooby'))
    
if __name__ == "__main__":
    test();
    
    
    
    
    
    
    
    
    
    
    
    
    
    