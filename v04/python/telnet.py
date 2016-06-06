#fix of keep alive problem. Works fine with this version, code is not super-clean but it works.

# telnet program example
import socket, select, string, sys
import string
import threading
#main function

HOST = "irc.twitch.tv"
PORT = 6667
IDENT = "YOURID"            # your Twitch username, lowercase
PASS = "YOUROAUTHKEY"
CHANNEL = "YOURCHANNEL"
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
keepaliveactive = 0

def openSocket():
	
	s = socket.socket()
	s.connect((HOST, PORT))
	s.send("PASS " + PASS + "\r\n")
	s.send("NICK " + IDENT + "\r\n")
	s.send("JOIN #" + CHANNEL + "\r\n")
	return s
	
def sendMessage(s, message):
	messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
	s.send(messageTemp + "\r\n")
	print("Sent: " + messageTemp)
    
def getUser(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user
def getMessage(line):
	separate = line.split(":", 2)
	message = separate[2]
	return message


def joinRoom(s):
	readbuffer = ""
	Loading = True
	while Loading:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			Loading = loadingComplete(line)
	sendMessage(s, "Successfully joined chat")
	
def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True
	

def calculateWinner(d):
    if (keepaliveactive == 0):
        global keepaliveactive
        keepaliveactive = 1
        keepalive()    

    scores = {}
    high_score = 0
    for key, value in d.items():
        try:
            scores[value].append(key)
        except KeyError:
            scores[value] = [key]
        if value > high_score:
            high_score = value
    results = scores[high_score]
    if len(results) == 1:
    	print results[0]
    	sendMessage(s, "Going " + results[0] + " !")
        stelnet.send(results[0])
        return results[0]
    else:
    	print 'TIE'
        sendMessage(s, "Draw ! I am not moving !")
        return 'TIE', results

def keepalive():
    threading.Timer(30, keepalive).start()
    stelnet.send("go")
    

def reinitScore():
	#launches this function every (1) seconds asynchronously
	threading.Timer(2, reinitScore).start()
	global leftKeyCounter
	global rightKeyCounter
	global frontKeyCounter
	global backKeyCounter
	values = {'left' : leftKeyCounter, 'right' : rightKeyCounter, 'front' : frontKeyCounter, 'back' : backKeyCounter}
	if (leftKeyCounter != 0 or rightKeyCounter != 0 or frontKeyCounter != 0 or backKeyCounter != 0):
		calculateWinner(values)
		leftKeyCounter = 0
		rightKeyCounter = 0
		frontKeyCounter = 0
		backKeyCounter = 0
		print "back to 0"



reinitScore()


s = openSocket()
joinRoom(s)
readbuffer = ""

if __name__ == "__main__":
    
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2]) 
    stelnet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stelnet.settimeout(2)
     
    # connect to remote host
    try :
        stelnet.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host'
    
    while True:
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
                
                if (sum(pattern in message for pattern in wordPattern) == 1): 
                    if (message.rstrip() == wordPattern[0]):
                        leftKeyCounter = leftKeyCounter + 1
                        print "left : %s" % leftKeyCounter
                    if (message.rstrip() == wordPattern[1]):
                        rightKeyCounter = rightKeyCounter + 1
                        print "right : %s" % rightKeyCounter
                    if (message.rstrip() == wordPattern[2]):
                        frontKeyCounter = frontKeyCounter + 1
                        print "front : %s" % frontKeyCounter
                    if (message.rstrip() == wordPattern[3]):
                        backKeyCounter = backKeyCounter + 1
                        print "back : %s" % backKeyCounter
                        
    while 1:
        socket_list = [sys.stdin, stelnet]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == stelnet:
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
                stelnet.send(msg)