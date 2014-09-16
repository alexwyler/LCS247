import socket
import threading
import time
import players
import active_games
import traceback
import re
import plog
 
# sets variables for connection to twitch chat
bot_owner = b'LCS247'
nick = b'LCS247'
server = b'irc.twitch.tv'
password = b'oauth:qgom5va0n9l2gim7kb5fzzer3xpvqmi'
 
queue = 0  # sets variable for anti-spam queue functionality
 
# sets variables for !add and !news commands
command = '!notset'
cmdmsg = 'This command is not set yet'
newsmsg = 'No news set'

MESSAGE_PATTERN = re.compile(':(.*)!(.*)@(.*).tmi.twitch.tv PRIVMSG #lcs247 :(.*)', re.IGNORECASE)

HYPE_COMMAND = re.compile('hype ([^,]*)(,(.*))?')
SHOW_PLAYERS = re.compile('show players')
HYPE_STANDARDS = re.compile('hype_standards')
SKIP_COMMAND = re.compile('skip')

    
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
                            suitable_games = active_games.get_suitable_games_in_order()
                            if suitable_games:
                                send_message("--- Players in Game ---")
                                for suitable_game in suitable_games:
                                    personality_name, account, score, game = suitable_game
                                    send_message("({0}) {1} on {2}".format(score, personality_name, game.get_champion(account[0])))
                            else:
                                send_message("No players in new games!")
                        
                        if user == 'lcs247' and HYPE_STANDARDS.search(message):
                            log('Hyping standard players...')
                            players.hype_standards()
                            
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
    init()
