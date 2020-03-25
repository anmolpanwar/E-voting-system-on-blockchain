import socket

def connect_to_peer(host,port,data):
    c = socket.socket()
    c.connect((host,port))
    try:
        c.send(bytes(data,'utf-8'))
        if not c.recv(1024).decode()=='ACKD':
            raise ConnectionError

    except KeyboardInterrupt:
        pass
