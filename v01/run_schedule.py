import string
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom

#arduino needed
import schedule
import time  
from time import sleep
import struct
import os  
from serial import Serial
#arduino config
availableArduino = True # Debugging without an Arduino  
testSerial = False # Debugging without Twitter connection  
arduinoPort = '/dev/cu.usbmodem1421' # USB port address for the Arduino  
arduinoBaud = '250000' # Baud for serial communication  
arduinoWaitTime = 3 # The length of time Python wait before attemping to issue commands to the Arduino  

PATT = [
    r"right",
    r"left",
    r"front",
    r"back"
]

leftKey = "left";
rightKey = "right";
frontKey = "front";
backKey = "back";

leftKeyCounter = 0
rightKeyCounter = 0
frontKeyCounter = 0
backKeyCounter = 0

os.system('cls' if os.name == 'nt' else 'clear')

# Arduino serial communication
if availableArduino:  
    ser = Serial(arduinoPort, arduinoBaud, timeout=3)

s = openSocket()
joinRoom(s)
readbuffer = ""

def calcuate_winner(d):
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
        return results[0]
    else:
    	print 'TIE'
        return 'TIE', results

def reinitScore():
	global leftKeyCounter
	global rightKeyCounter
	global frontKeyCounter
	global backKeyCounter
	
	values = {'left' : leftKeyCounter, 'right' : rightKeyCounter, 'front' : frontKeyCounter, 'back' : backKeyCounter}
	calcuate_winner(values)

	leftKeyCounter = 0
	rightKeyCounter = 0
	frontKeyCounter = 0
	backKeyCounter = 0

	print "back to 0"


schedule.every(5).seconds.do(reinitScore)

while True:

	schedule.run_continuously()
	

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

			if (sum(pattern in message for pattern in PATT) == 1): 
				if (message.rstrip() == leftKey):
					leftKeyCounter = leftKeyCounter + 1
					print "left : %s" % leftKeyCounter
				if (message.rstrip() == rightKey):
					rightKeyCounter = rightKeyCounter + 1
					print "right : %s" % rightKeyCounter
				if (message.rstrip() == frontKey):
					frontKeyCounter = frontKeyCounter + 1
					print "front : %s" % frontKeyCounter
				if (message.rstrip() == backKey):
					backKeyCounter = backKeyCounter + 1
					print "back : %s" % backKeyCounter
