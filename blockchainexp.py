from hashlib import *
import time
zeros = 2

class transaction:
    def __init__(self,fromadd,toadd,amount):
        self.fromadd=fromadd
        self.toadd=toadd
        self.amount=amount
        self.time = time.strftime('%d/%m/%Y - %H:%M:%S')

        self.transobj = {'Sender_Address':self.fromadd,'Recipient_Address':self.toadd,'Amount':self.amount,'Time':self.time}
        Blockchain.pendingtrans.append(self.transobj)

class Block:
    blockindex = 1
    def __init__(self,ts,data,prevhash='0'):
        self.index=Block.blockindex
        Block.blockindex+=1
        self.ts = ts
        self.data=data
        self.nonce=0
        self.prevhash=prevhash
        self.hash=self.pow()

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
    def __init__(self):
        self.chain = []

    def genesis(self):
        return Block(time.strftime('%d/%m/%Y - %H:%M:%S'),'data in genesis')

    def addGenesis(self): #addBlock vale method me if length of chain is 0 --> add genesis block se ho sakta tha but...
        self.chain.append(self.genesis()) #baar baar block add karne pe ek if condition bar bar execute hoti faltu me

    def load_trans_in_block(self,index):
        pass


    def addBlock(self,newBlock):

        newBlock.prevhash=self.chain[len(self.chain)-1].hash
        newBlock.hash=newBlock.pow()
        self.chain.append(newBlock)

    def valid(self):
        for i in range(1,len(self.chain)):
            if self.chain[i].hash!=self.chain[i].calcHash():
                return False
            if self.chain[i-1].hash!=self.chain[i].prevhash:
                return False

        return True

    def displayChain(self):
        for i in range(len(self.chain)):
            self.chain[i].blockData()


chain = Blockchain()
chain.addGenesis()
b2 = Block(time.strftime('%d/%m/%Y - %H:%M:%S'),'some data in 2nd block')
b3 = Block(time.strftime('%d/%m/%Y - %H:%M:%S'),'data in 3rd block')
chain.addBlock(b2)
chain.addBlock(b3)

chain.displayChain()
t1 = transaction('234523','23543etr',34)
t2 = transaction('234523eafd','23543etadffdvsafsr',878)
t3 = transaction('2dsfa34523','23dsg543etr',324)
t4 = transaction('2svb34523eafd','23543ecbtafdvsafsr',885)
t5 = transaction('234bd523','235cbv43etr',364)
t6 = transaction('234dg523eafd','23543bcvetafdvsafsr',288)
t7 = transaction('2345gdf23','23543bcetr',344)
t8 = transaction('2345gd23eafd','23543ecbtafd5vsafsr',588)
print(Blockchain.pendingtrans)
