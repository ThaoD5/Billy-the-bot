import socket, select, string, sys
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom

import threading

#arduino needed
import time  
from time import sleep
import struct
import os  
from serial import Serial

def reinitScore():
    threading.Timer(5, reinitScore).start()
    s.send('PING')
    print 'PING'
#words you want to check
wordPattern = [
    r"left",
    r"right",
    r"front",
    r"back"
]
#counters for the democracy
leftKeyCounter = 0
rightKeyCounter = 0
frontKeyCounter = 0
backKeyCounter = 0
#trap method
movementsMade = []

os.system('cls' if os.name == 'nt' else 'clear')

# Arduino serial communication

s = openSocket()
joinRoom(s)
readbuffer = ""
if __name__ == "__main__":
    if(len(sys.argv) < 3) :
    	print 'Usage : python telnet.py hostname port'
    	sys.exit()
    
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host'
    reinitScore()

	while True :
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()

		for line in temp:
				print(line)
				if "PING" in line:
					s.send(line.replace("PING", "PONG"))
					break

				user = getUser(line)
				message = getMessage(line)
				print user + " typed :" + message

		socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print 'Connection closed'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)


