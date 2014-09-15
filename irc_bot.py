import socket
import threading
import time
import players
import re
 
#sets variables for connection to twitch chat
bot_owner = b'LCS247'
nick = b'LCS247'
server = b'irc.twitch.tv'
password = b'oauth:qgom5va0n9l2gim7kb5fzzer3xpvqmi'
 
queue = 0 #sets variable for anti-spam queue functionality
 
#sets variables for !add and !news commands
command = '!notset'
cmdmsg = 'This command is not set yet'
newsmsg = 'No news set'

MESSAGE_PATTERN = re.compile(':(.*)!(.*)@(.*).tmi.twitch.tv PRIVMSG #lcs247 :(.*)', re.IGNORECASE)

HYPE_COMMAND = re.compile('hype (.*)')
SHOW_PLAYERS = re.compile('show players')
HYPE_STANDARDS = re.compile('hype_standards')
    
def init():

    def process():
        readbuffer = ""
        irc = socket.socket()
        irc.connect((server, 6667)) #connects to the server
        
        def send_message(message):
            irc.send(bytes('PRIVMSG #lcs247 :{0}\r\n'.format(message), 'UTF-8'))
        
        #sends variables for connection to twitch chat
        irc.send(b'PASS ' + password + b'\r\n')
        irc.send(b'USER ' + nick + b' 0 * :' + bot_owner + b'\r\n')
        irc.send(b'NICK ' + nick + b'\r\n')
        irc.send(bytes("JOIN #lcs247\r\n", "UTF-8"));
        print('[ irc bot ]\t Listening for commands...')
        while True:
            readbuffer = readbuffer+irc.recv(1024).decode("UTF-8")
            temp = str.split(readbuffer, "\n")
            readbuffer=temp.pop( )
            
            for line in temp:
                m = MESSAGE_PATTERN.match(line)
                if m:
                    user, message = m.group(1, 4)
                    
                    hype_m = HYPE_COMMAND.match(message)
                    if hype_m:
                        player = hype_m.group(1).strip()
                        players.hype_personality(player, 1) 
                        personality = players.get_personality(player)
                        message = "{0} hypes {1} to {2}!".format(user, personality['name'], personality['hype'])
                        print('[ irc bot ]\t {0}'.format(message))
                        send_message(message)
                    
                    show_m = SHOW_PLAYERS.match(message)
                    if show_m:
                        pass
                    
                    if user == 'lcs247' and HYPE_STANDARDS.match(message):
                        print('[ irc bot ]\t {0}'.format("Hyping standard players..."))
                        players.hype_standards()
                        

            time.sleep(1)

    t = threading.Thread(target=process)
    t.start()
    
if __name__ == '__main__':
    init()