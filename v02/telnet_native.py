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


s = openSocket()
joinRoom(s)
readbuffer = ""

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
