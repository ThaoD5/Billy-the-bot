import socket
s_global = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_global.bind(("127.0.0.1", 9091))
backlog = 0xFF
s_global.listen(backlog)
s_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_local.bind(("192.168.1.58", 5555))
s_local.listen(backlog)