from hashlib import *
from time import time
zeros = 2
#pycharm app
class transaction:
    transcount=0
    def __init__(self,fromadd,toadd,amount):
        self.fromadd=fromadd
        self.toadd=toadd
        self.amount=amount
        self.time = time()

        self.transobj = {'Sender_Address':self.fromadd,'Recipient_Address':self.toadd,'Amount':self.amount,'Time':self.time}
        Blockchain.pendingtrans.append(self.transobj)
        transaction.transcount+=1
        self.abc()

    def abc(self):
        if transaction.transcount%4==0:
            return Block(time(),Blockchain.pendingtrans[:transaction.transcount-1:-1])

class Block:
    blockindex = 1
    def __init__(self,ts,data,prevhash='0'):
        self.index=Block.blockindex
        Block.blockindex+=1
        self.ts = ts
        self.data=data
        self.nonce=0
        self.prevhash=Blockchain.chain[len(Blockchain.chain)-1].hash
        self.hash=self.pow()
        Blockchain.chain.append(self)


    def calcHash(self):
        return sha256((str(str(self.data)+str(self.nonce)+str(self.ts)+self.prevhash)).encode('utf-8')).hexdigest()

    def blockData(self):
        print ("Block number: ", self.index)
        print ("Block timestamp: ", self.ts)
        print ("Block data: ", self.data)
        print ("Nonce: ",self.nonce)
        print ("Block previous hash: ", self.prevhash)
        print ("Block hash: ", self.hash,'\n')


    def pow(self,zero=zeros):
        self.nonce=0
        while(self.calcHash()[:zero]!='0'*zero):
            self.nonce+=1
        return self.calcHash()


class Blockchain:
    pendingtrans=[]
    chain = []
    def __init__(self):
        pass

    def genesis(self):
        return Block(time(),'data in genesis')

    def addGenesis(self): #addBlock vale method me if length of chain is 0 --> add genesis block se ho sakta tha but...
        Blockchain.chain.append(self.genesis()) #baar baar block add karne pe ek if condition bar bar execute hoti faltu me

    def load_trans_in_block(self,index):
        pass


    def addBlock(self,newBlock):

        newBlock.prevhash=self.chain[len(self.chain)-1].hash
        newBlock.hash=newBlock.pow()
        self.chain.append(newBlock)

    def valid(self):
        for i in range(1,len(Blockchain.chain)):
            if Blockchain.chain[i].hash!=Blockchain.chain[i].calcHash():
                return False
            if Blockchain.chain[i-1].hash!=Blockchain.chain[i].prevhash:
                return False

        return True

    def displayChain(self):
        for i in range(len(Blockchain.chain)):
            Blockchain.chain[i].blockData()


chain = Blockchain()
chain.addGenesis()
b2 = Block(time(),'some data in 2nd block')
b3 = Block(time(),'data in 3rd block')
chain.addBlock(b2)
chain.addBlock(b3)


t1 = transaction('234523','23543etr',34)
t2 = transaction('234523eafd','23543etadffdvsafsr',878)
t3 = transaction('2dsfa34523','23dsg543etr',324)
t4 = transaction('2svb34523eafd','23543ecbtafdvsafsr',885)
t5 = transaction('234bd523','235cbv43etr',364)
t6 = transaction('234dg523eafd','23543bcvetafdvsafsr',288)
t7 = transaction('2345gdf23','23543bcetr',344)
t8 = transaction('2345gd23eafd','23543ecbtafd5vsafsr',588)
t9 = transaction('2345gdnm23','23543ecvbtr',345)
t10 = transaction('234523vneafd','2354nc3etafdvsafsr',858)
chain.displayChain()
