import socket
import simplejson as json
import csv

s = socket.socket()
print('socket created')
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('192.168.0.135',9999))

s.listen(5)

print('waiting')

while True:
    try:
        c,addr = s.accept()
        print('conn esbd: ',addr)
        msg = c.recv(8192).decode()
        msg = json.loads(msg)
        if type(msg)==dict:
            vpk = bytes(msg['voter_public_key'],'utf-8')
            ls = [vpk.decode('unicode-escape').encode('ISO-8859-1'), msg['data'], msg['key']]
            # with open('temp/votefile.csv','a',newline="") as votefile:
            #     writer = csv.writer(votefile)
            #     writer.writerow(ls)
            print('Pudipeddi mac says:',msg)
            c.send(bytes('ACKD','utf-8'))
        else:
            with open('temp/result.csv','w',newline="") as votefile:
                writer = csv.writer(votefile)
                writer.writerow(msg)

    except BrokenPipeError:
        pass
