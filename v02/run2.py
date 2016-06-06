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
#arduino config
availableArduino = False # Debugging without an Arduino  
#testSerial = False # Debugging without Twitter connection  
arduinoPort = '/dev/cu.usbmodem1421' # USB port address for the Arduino  
arduinoBaud = '250000' # Baud for serial communication  
arduinoWaitTime = 3 # The length of time Python wait before attemping to issue commands to the Arduino  
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
if availableArduino:  
    ser = Serial(arduinoPort, arduinoBaud, timeout=3)

s = openSocket()
joinRoom(s)
readbuffer = ""

def calculateWinner(d):
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
    	print (results[0])
    	print (len(movementsMade))
    	if len(movementsMade) == 5 :
    		print (movementsMade)
    		#delete last
    		del movementsMade[0]
    		print (movementsMade)
    		# add newest
    		movementsMade.append(results[0])
    		print (movementsMade)
    	else: 
    		movementsMade.append(results[0])
    		print (movementsMade)
        return results[0]
        else:
    	   print ('TIE')
            return 'TIE', results

def reinitScore():
	#launches this function every (5) seconds asynchronously
	threading.Timer(5, reinitScore).start()
	#globaling for changing the content
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
		print ("back to 0")

reinitScore()
sendcommand()
while True:
	readbuffer = readbuffer + s.recv(1024)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()
    # this will block until at least one socket is ready
    ready_socks,_,_ = select.select(socks, [], []) 
    for sock in ready_socks:
        data, addr = sock.recvfrom(1024) # This is will not block
        print ("received message:", data)

	for line in temp:
			print(line)
			if "PING" in line:
				s.send(line.replace("PING", "PONG"))
				break

			user = getUser(line)
			message = getMessage(line)
			print (user + " typed :" + message)

			if (sum(pattern in message for pattern in wordPattern) == 1): 
				if (message.rstrip() == wordPattern[0]):
					leftKeyCounter = leftKeyCounter + 1
					print ("left : %s" % leftKeyCounter)
				if (message.rstrip() == wordPattern[1]):
					rightKeyCounter = rightKeyCounter + 1
					print ("right : %s" % rightKeyCounter)
				if (message.rstrip() == wordPattern[2]):
					frontKeyCounter = frontKeyCounter + 1
					print ("front : %s" % frontKeyCounter)
				if (message.rstrip() == wordPattern[3]):
					backKeyCounter = backKeyCounter + 1
					print ("back : %s" % backKeyCounter)
