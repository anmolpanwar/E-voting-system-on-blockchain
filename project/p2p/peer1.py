import socket

s = socket.socket()
print('socket created')

s.bind(('localhost',9998))

s.listen(1)

print('waiting')

while True:
    c,addr = s.accept()
    name = c.recv(1024).decode()
    print('Connected with:', addr,name)
    c.send(bytes('Hi'+name,'utf-8'))
    c.close()
