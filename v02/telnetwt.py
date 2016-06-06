# telnet program example
import socket, select, string, sys
import threading
#main function

def reinitScore():
    threading.Timer(5, reinitScore).start()
    stelnet.send('PING')
    print 'PING'

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
    reinitScore()
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