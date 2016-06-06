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

def sendCommand():
	global leftKeyCounter
	leftKeyCounter = 0

	global rightKeyCounter
	leftKeyCounter = 0

	global frontKeyCounter
	leftKeyCounter = 0

	global backKeyCounter
	leftKeyCounter = 0

	#print "left : %d , right : %d , front : %d , back : %d" % (leftKeyCounter, rightKeyCounter, frontKeyCounter, backKeyCounter)
	return (leftKeyCounter, rightKeyCounter, frontKeyCounter, backKeyCounter)
	print "back to 0"


schedule.every(5).seconds.do(sendCommand)

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
