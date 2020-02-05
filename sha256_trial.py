from hashlib import sha256

nonce = 0
msg = str("some data in 2nd block"+str(nonce)+"13:23:57"+'00885fa00190d22a676b591d14d888c6d4b613445542fa3712e4745c3848c1b8')
print (msg)
mh = sha256(str(msg).encode('utf-8')).hexdigest()

while(mh[:2]!='00'):
    nonce+=1
    msg = str("time.strftime('%d/%m/%Y - %H:%M:%S')data in 3rd block"+str(nonce)+"6767"+'00e5bb668b5a847807464f0ed374076e8882b70b962878216834e6c6f93dfdd1')
    mh = sha256(str(msg).encode('utf-8')).hexdigest()
    print (nonce)


msg = msg + str(nonce)

print (mh,nonce)

# class tr:
#     def __init__(self,toadd,fromadd,amount):
#         self.fromadd=fromadd
#         self.toadd=toadd
#         self.amount=amount
#
# t1 = tr('2352435w41','2342442ewq3',34)
# t2 = tr('345435wrte','34564345334',78)
#
#
