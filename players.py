'''
Created on Sep 12, 2014

@author: alexwyler
'''
import collections
import sqlite3
import util
import os

POPULAR_PLAYERS = collections.OrderedDict()
global DB_PATH

def lazy_init():
    global DB_PATH
    DB_PATH = os.path.dirname(__file__) + os.sep + 'players.db'
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personalities'")
    if not cursor.fetchone():
        init_data()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
    if not cursor.fetchone():
        init_data()
    
def decay_hype():
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute("UPDATE personalities SET hype = max(hype / 2 - 1, 0)")
    conn.commit()
    conn.close()
    
def hype_standards():
    for personality_name in PLAYERS:
        hype_personality(personality_name, 5)

def create_personality(name, region='NA'):
    if isinstance(name, str):
        region = 'NA'
    else:
        name, region = name
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO personalities (name, hype) VALUES (?, 0)", (name,))
    cursor.execute("INSERT INTO accounts (clean_name, display_name, region, personality_name) VALUES (?, ?, ?, ?)", (util.to_clean_name(name), name, region, name))
    conn.commit()
    conn.close()

'''
Given a personality name or account name, hype that personality
'''
def hype_personality( name, amount ):
    if isinstance(name, str):
        region = 'NA'
    else:
        name, region = name

    personality = get_personality((name, region))

    if not personality:
        create_personality((name, region))
        hype_personality((name, region), amount)
    else:
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
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    return conn

def get_personality(name):
    if isinstance(name, str):
        region = 'NA'
    else:
        name, region = name
    
    personality = get_personality_for_name(name)
    if not personality:
        personality = get_personality_for_account_name((name, region))
    return personality

def get_personality_for_account_name(account_name):
    if isinstance(account_name, str):
        name = account_name
        region = 'NA'
    else:
        name, region = account_name
    
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute("SELECT name, hype FROM personalities as p inner join accounts as a on p.name = a.personality_name where a.clean_name = ? and a.region = ?", (util.to_clean_name(name), region))
    personality = cursor.fetchone()
    conn.close()
    return personality

def get_personality_for_name(name):
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute("SELECT name, hype FROM personalities where name = ?", (name,))
    personality = cursor.fetchone()
    conn.close()
    return personality

def get_personalities_by_hype():
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM personalities WHERE hype > 0 ORDER BY hype DESC")
    personalities = cursor.fetchall()
    conn.close()
    return personalities

def get_accounts_with_hype():
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute("SELECT a.clean_name, a.region FROM accounts AS a INNER JOIN personalities AS p ON a.personality_name = p.name where p.hype > 0")
    accounts = cursor.fetchall()
    conn.close()
    return [(account['clean_name'], account['region']) for account in accounts]
    
PLAYERS = collections.OrderedDict()

PLAYERS['Imaqtpie'] = ['Imaqtpie', 'qtpie', 'Zstinkloser430Z', 'LMQ Tc Tabe', 'Jessica Lynn', 'adsafadfdsafdasf']
PLAYERS['Shiptur'] = ['Shiphtur', 'mMe Shiphtur', 'Chapanya', 'CST Shiponya', 'Pawn Dog', 'Apdo Dog']
PLAYERS['Voyboy'] = ['Voyboy', 'Crs Vooby', 'Crs Voyboy', 'Nihilmatic']
PLAYERS['Dexter'] = ['dexter', 'GoldPoro2', 'LDdexter', 'OPOP174AMHA195', 'CIJL963PFPA447B', 'CLGsavior', 'CHIMPERATOR']
PLAYERS['PorpoisePops'] = ['PorpoisePops', 'vVv PorpoisePops']
PLAYERS['Slooshi'] = ['Slooshi', 'aL Slooshi', 'Slooshi8']
PLAYERS['frommaplestreet'] = ['frommaplestreet', 'Velocity Maple']
PLAYERS['Dodo8'] = ['Dodo8']
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
PLAYERS['Dyrus'] = ['Dyrus', 'Insert Smurf Here', 'I DIED TO WOLVES', 'superpaladin98', ('suryd', 'KR'), ('TSM suryD', 'KR'), ('WORST CALLS NA', 'EUW'), ('1 800 MICROWAVE', 'EUW'), ('WORST CALLS LOL', 'EUW')]
PLAYERS['Amazing'] = ['Amazing', 'AmaZiinG94', 'AL Amazing', 'Acer Amazing', 'p Amazing', ('CW Amazing', 'EUW'), 'TSM Amazingprox', ('TSM Amazingx', 'KR')]
PLAYERS['Bjergsen'] = ['Bjergsen', 'I am BjergerKing', 'Bjerg', 'magickiller45', 'BJ3RGR1F1C', 'NiP Bjergsen', 'NiP Derpsen', 'mcdonalds185', 'King Bjergsen NA', 'DIG Chapanya', ('TSM Bjergtheking', 'EUW'), 'Rust', 'Kingmidmidmid', 'Bjergermelon', ('TSM BjergsenMid', 'KR')]
PLAYERS['WildTurtle'] = ['WildTurtle', 'TSM CAT', 'Turtle the Cat', 'kT Turtle', 'Quantic Turtle', 'Leaf Turtle', 'WildTurtl', ('YuNg TuRtLe', 'KR')]
PLAYERS['LustBoy'] = [('CJ Entus 장식', 'KR'), ('Azubu B Lustboy', 'KR'), ('MiG Lustboy', 'KR'), 'Lustnation', ('AKA The Reason', 'KR')]

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
        for account_details in PLAYERS[personality_name]:
            if isinstance(account_details, str):
                account = account_details
                region = 'NA'
            else:
                account, region = account_details
            c.execute("INSERT INTO accounts (clean_name, display_name, region, personality_name) VALUES (?, ?, ?, ?)", (util.to_clean_name(account), account, region, personality_name))
    conn.commit()
    conn.close()

lazy_init()

def test():
    print(get_personality('Voyboy'))
    hype_personality("Voyboy", 5)
    print(get_personality_for_account_name('crs vooby'))
    if not get_personality('grraffe'):
        create_personality('grraffe')
    hype_personality('grraffe', 1)
    print(get_personality('grraffe'))
    
    hype_standards()
    
    print(get_accounts_with_hype())
    decay_hype()
    print(get_personality('Voyboy'))
    print(get_accounts_with_hype())
    
    decay_hype()
    print(get_personality('Voyboy'))
    print(get_accounts_with_hype())

if __name__ == "__main__":
    test()
