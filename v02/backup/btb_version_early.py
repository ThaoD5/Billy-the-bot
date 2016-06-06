import string
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom

#arduino needed
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

os.system('cls' if os.name == 'nt' else 'clear')

# Arduino serial communication
if availableArduino:  
    ser = Serial(arduinoPort, arduinoBaud, timeout=3)

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

			#test if there is more than one result
			if(sum(pattern in message for pattern in PATT) == 1):
				sendMessage(s, "One match, Ok !")

				#debugging for the arduino / computer serial exchange
                if testSerial:
                    print "On"
                    #serial writing to the arduino, then wait.
                    ser.write(bytes(1))
                    sleep(arduinoWaitTime)
                    print "Off"
                    #serial writing to the arduino, then wait.
                    ser.write(bytes(0))
                    sleep(arduinoWaitTime)
                else:  
                        # Checks if text within the stream item is populated and issues a command to the Arduino
                    if availableArduino:
                        if (message.rstrip() == leftKey):
                            ser.write("left".encode())
                            print "left sent"

                        elif (message.rstrip() == rightKey):
                            ser.write("right".encode())
                            print "right sent"

                        elif (message.rstrip() == frontKey):
                            ser.write("front".encode())
                            print "front sent"

                        elif (message.rstrip() == backKey):
                            ser.write("back".encode())
                            print "back sent"
                        else:
                            print "not sent"

			time.sleep(0.05)
