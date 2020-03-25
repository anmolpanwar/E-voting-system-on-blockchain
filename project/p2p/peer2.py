import socket

def connect_to_peer(host,port):
    pass


def send_msg(data):
    try:
        c = socket.socket()
        c.connect(('192.168.0.135',9999))
        c.send(bytes(data,'utf-8'))
        if not c.recv(1024).decode()=='ACKD':
            raise ConnectionError
        c.close()

    except KeyboardInterrupt:
        pass

while True:
    send_msg(input())
