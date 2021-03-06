import socket
import threading
import time
import players
import active_games
import traceback
import re
import plog
import subprocess
import config
 
# sets variables for connection to twitch chat
bot_owner = b'LCS247'
nick = b'LCS247'
server = b'irc.twitch.tv'
password = b'oauth:qgom5va0n9l2gim7kb5fzzer3xpvqmi'
 
MESSAGE_PATTERN = re.compile(':(.*)!(.*)@(.*).tmi.twitch.tv PRIVMSG #lcs247 :(.*)', re.IGNORECASE)
HYPE_COMMAND = re.compile('hype ([^,]*)(,(.*))?', re.IGNORECASE)
SHOW_PLAYERS = re.compile('show players', re.IGNORECASE)
HYPE_STANDARDS = re.compile('hype_standards', re.IGNORECASE)
SKIP_COMMAND = re.compile('(skip)|(booo*)', re.IGNORECASE)
NEXT_SONG_COMMAND = re.compile('next_song', re.IGNORECASE)

def init(SharedGameDetails):

    def process():
        readbuffer = ""
        irc = socket.socket()
        irc.connect((server, 6667))  # connects to the server
        
        def send_message(msg):
            irc.send(bytes('PRIVMSG #lcs247 :{0}\r\n'.format(msg), 'UTF-8'))
        
        # sends variables for connection to twitch chat
        irc.send(b'PASS ' + password + b'\r\n')
        irc.send(b'USER ' + nick + b' 0 * :' + bot_owner + b'\r\n')
        irc.send(b'NICK ' + nick + b'\r\n')
        irc.send(bytes("JOIN #lcs247\r\n", "UTF-8"));
        log('Listening for commands...')
        while True:
            try:
                readbuffer = readbuffer + irc.recv(1024).decode("UTF-8")
                temp = str.split(readbuffer, "\n")
                readbuffer = temp.pop()
                
                for line in temp:
                                        
                    m = MESSAGE_PATTERN.match(line)
                    if m:
                        user, message = m.group(1, 4)
                        hype_m = HYPE_COMMAND.search(message)
                        if hype_m:
                            player = hype_m.group(1).strip()
                            region = (hype_m.group(3) or 'NA').strip()
                            players.hype_personality((player, region), 1) 
                            personality = players.get_personality(player)
                            message = "{0} hypes {1} to {2}!".format(user, personality['name'], personality['hype'])
                            log(message)
                            send_message(message)
                        
                        show_m = SHOW_PLAYERS.search(message)
                        if show_m:
                            potential_games = active_games.get_potential_games_in_order()
                            if potential_games:
                                send_message("--- Players in Game ---")
                                for suitable_game in potential_games:
                                    personality_name, account, score, game = suitable_game
                                    if game.is_within_spectator_delay():
                                        waiting = ', waiting to begin'
                                    else:
                                        waiting = ''
                                    message = "({0}{3}) {1} on {2} {4}".format(score, personality_name, game.get_champion(account[0]), waiting, game.get_timestamp_since_start())
                                    send_message(message)
                            else:
                                send_message("No potential games!")
                        
                        if user == 'lcs247' and HYPE_STANDARDS.search(message):
                            log('Hyping standard players...')
                            players.hype_standards()
                        
                        if user == 'lcs247' and NEXT_SONG_COMMAND.search(message):
                            log('SKipping song...')
                            send_message('Skipping song...')
                            subprocess.call([config.CONTEXT_UTIL['ahk_path'],
                                             config.CONTEXT_UTIL['ahk_next_song_path']])
                            
                        if (SKIP_COMMAND.search(message)):
                            selected_game_details = SharedGameDetails.selected_game
                            if selected_game_details:
                                personality_name, account, _, game = selected_game_details
                                players.hype_personality(personality_name, -1)
                                personality = players.get_personality(personality_name)
                                if personality['hype'] <= 0:
                                    send_message('Skipping current game!')
                                    SharedGameDetails.selected_game = None
                                else:
                                    send_message("De-hyping {0} to {1}. Get him to 0 to skip".format(personality_name, personality['hype']))
                            else:
                                send_message("No active game...")
                    else:
                        if line.find ('PING') != -1:
                            irc.send (bytes('PONG ' + line.split() [ 1 ] + '\r\n', 'UTF-8'))
                        else:
                            log(line)
    
                time.sleep(1)
            except Exception as e:
                log(str(e))
                traceback.print_exc()
            
        log('Exiting loop!')

    t = threading.Thread(target=process)
    t.start()
    
def log(message):
    plog.log('irc bot', message)

if __name__ == '__main__':
    init(None)
