import socket

s = socket.socket()
print('socket created')

s.bind(('192.168.0.135',9999))

s.listen(5)

# print('waiting')

while True:
    c,addr = s.accept()
    print('conn esbd: ', addr)
    msg = c.recv(1024).decode()
    print('Pudipeddi mac says:', msg)
    c.send(bytes('ackd','utf-8'))
