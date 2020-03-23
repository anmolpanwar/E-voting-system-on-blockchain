import socket
while True:
    try:
        c = socket.socket()
        c.connect(('192.168.0.152',9998))
        name = input()
        c.send(bytes(name,'utf-8'))
        print(c.recv(1024).decode())

    except KeyboardInterrupt:
        pass
