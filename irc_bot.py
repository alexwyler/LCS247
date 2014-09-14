import sys
import socket
import string
import threading
 
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
 
def init():

    def process():
        readbuffer = ""
        irc = socket.socket()
        irc.connect((server, 6667)) #connects to the server
        
        #sends variables for connection to twitch chat
        irc.send(b'PASS ' + password + b'\r\n')
        irc.send(b'USER ' + nick + b' 0 * :' + bot_owner + b'\r\n')
        irc.send(b'NICK ' + nick + b'\r\n')
        irc.send(bytes("JOIN #lcs247\r\n", "UTF-8"));
        irc.send(bytes("PRIVMSG %s :Hello Master\r\n" % 'alexwyler', "UTF-8"))
        while True:
            readbuffer = readbuffer+irc.recv(1024).decode("UTF-8")
            temp = str.split(readbuffer, "\n")
            readbuffer=temp.pop( )
            
            for line in temp:
                print('data: ' + line)
                 
    t = threading.Thread(target=process)
    t.start()
    
if __name__ == '__main__':
    init()