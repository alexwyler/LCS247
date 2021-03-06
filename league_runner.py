'''
Created on Sep 12, 2014

@author: alexwyler
'''
import threading
import os
import platform
import subprocess
import util
import config

MAC_LOL_VERSION = "0.0.0.133"
MAC_LOL_CLIENT_VERSION = "0.0.0.144"

PC_LOL_VERSION = "0.0.1.55"
PC_LOL_CLIENT_VERSION = "0.0.1.55"

def kill_game():
    if platform.system() != 'Darwin':
        kill_game_pc()
    else:
        kill_game_mac()

'''
OS Specific ways of killing shit
'''
def kill_game_mac():
    os.system("killall -9 LeagueofLegends");
    pass

def kill_game_pc():
    os.system( r'taskkill /F /IM "League of Legends.exe"' );
    pass

def open_game(game, team_str, position):
    if platform.system() != 'Darwin':
        open_game_pc(game, team_str, position)
    else:
        open_game_mac(game, team_str, position)

'''
Opens game on mac given the spectate_info and returns a handle on the process
'''
def open_game_mac(game, team_str, position):
    devnull = open(os.devnull, "w")
    ip_and_port = str(game.server) + ':' + str(game.port)
    cmd = '''
    cd /Applications/League\ of\ Legends.app/Contents/LoL/RADS/solutions/lol_game_client_sln/releases/{0}/deploy/LeagueOfLegends.app/Contents/MacOS/
    riot_launched=true "/Applications/League of Legends.app/Contents/LoL/RADS/solutions/lol_game_client_sln/releases/{0}/deploy/LeagueOfLegends.app/Contents/MacOS/LeagueofLegends" 8394 LoLLauncher "/Applications/League of Legends.app/Contents/LoL/RADS/projects/lol_air_client/releases/{1}/deploy/bin/LolClient" "spectator {2} {3} {4} {5}"
    '''.format(MAC_LOL_VERSION, MAC_LOL_CLIENT_VERSION, ip_and_port, game.key, game.game_id, game.region)
    
    full_cmd = ["bash", "-c", cmd]
    
    return subprocess.Popen(full_cmd, stderr = devnull)

'''
player locator
is_team_1 and index must be strings
'''
def startAutohotkey( is_team_1, index):
    
    subprocess.call([config.CONTEXT_UTIL['ahk_path'],
                     config.CONTEXT_UTIL['ahk_spectator_path'],
                     is_team_1,
                     index])
    pass

def open_game_pc(game, team_str, position):
    os.chdir(r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\{0}\deploy".format(PC_LOL_VERSION))
    def open_game(game):
        ip_and_port = str(game.server) + ':' + str(game.port)
        encryption_key = game.key
        game_id = game.game_id
        server = "NA1"
    
        return subprocess.call([r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\{0}\deploy\League of Legends.exe".format(PC_LOL_VERSION),
                "8394",
                "LoLLauncher.exe",
                "",
                "spectator {0} {1} {2} {3}".format( ip_and_port, encryption_key, game_id, server )])
    
    game_thread = threading.Thread( target=open_game, args = (game,) )
    game_thread.start()
    ahk_thread = threading.Thread( target=startAutohotkey, args = (team_str,str(position),) )
    ahk_thread.start()
    
def get_champion_id_by_name( name, team ):
    
    internal_name = util.to_clean_name(name)
    for player in team:
        if player['summonerInternalName'] == internal_name:
            return player['championId']
    return None


# if __name__ == "__main__":
#     config.init()
#     startAutohotkey(str("false"), str(3))