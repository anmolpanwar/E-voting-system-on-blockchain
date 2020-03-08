from hashlib import *
# from cryptography.hazmat.primitives.asymmetric import *
import cryptography
from time import time
from flask import *
import csv
import pickle

difficulty = 2

class vote:

    count = 0

    def __init__(self,candidateID):
        self.candidate = candidateID
        self.time = time()
        vote.count+=1
        self.voteobject = {self.candidate:self.time}

    def signvote(self):
        pass


class Blockchain:

    chain = []

    @classmethod
    def __init__(cls):
        cls.length=len(cls.chain)

    def genesis(self):
        gen = Block(0,"Let the real democracy rule!!", sha256(str("Let the real democracy rule!!").encode('utf-8')).hexdigest(), difficulty, time(),'',pow=0)
        return gen

    def addGenesis(self):
        genesis1 = self.genesis()
        genesis1.nonce = genesis1.pow()
        Blockchain.chain.append(genesis1)

    def display(self):
        # for block in self.chain:
        #     print("Block Height: ", block.height)
        #     print("Data in block: ", block.data)
        #     print("Merkle root: ", block.merkle)
        #     print("Difficulty: ", block.difficulty)
        #     print("Time stamp: ", block.timeStamp)
        #     print("Previous hash: ", block.prevHash)
        #     print("Nonce: ", block.nonce)
        #     print("\t\t\t|\n|\n|\n")
        with open('blockchain.txt','rb') as blockfile:
            data = pickle._load(blockfile)

        return data


class Block:

    def __init__(self,height = 0,data = 'WARNING = SOME ERROR OCCURED',merkle = '0',difficulty = 0,time = 0,prevHash = '0',pow=0):
        self.height = height               #len(Blockchain.chain-1)
        self.data = data                         #loadvote()
        self.merkle = merkle                 #calculateMerkleRoot()
        self.difficulty = difficulty                        #cryptography difficulty
        self.timeStamp = time                             #time()
        self.prevHash = prevHash
        self.nonce = pow                            #proof of work function will find nonce.

    def pow(self,zero=difficulty):                          #proof-of-work method
        self.nonce=0
        while(self.calcHash()[:zero]!='0'*zero):
            self.nonce+=1
        return self.nonce

    def calcHash(self):
        return sha256((str(str(self.data)+str(self.nonce)+str(self.timeStamp)+str(self.prevHash))).encode('utf-8')).hexdigest()


    @staticmethod
    def loadvote():
        votelist = []
        try:
            with open('votefile.csv', mode = 'r') as votepool:
                csvreader = csv.reader(votepool)
                for row in csvreader:
                    votelist.append({'CandidateID':row[0], 'Time':row[1]})
            return votelist

        except(IOError,IndexError):
            pass

        finally:
            print("data loaded in block")


    def merkleRoot(self):
        return 'congrats'

    def mineblock(self):
        self.height = len(Blockchain.chain)                #len(Blockchain.chain-1)
        self.data = self.loadvote()                         #loadvote()
        self.merkle = self.merkleRoot()                #calculateMerkleRoot()
        self.difficulty = difficulty
        self.timeStamp = time()                             #time()
        self.prevHash = Blockchain.chain[-1].calcHash()
        self.nonce = self.pow()
        Blockchain.chain.append(self)

        return self

app = Flask(__name__)

@app.route('/')
def func():
    return render_template('first.html')

@app.route('/home', methods = ['POST'])
def func2():
    choice = request.form['candidate']
    v1 = vote(int(choice))

    with open('votefile.csv','a',newline="") as votefile:
        writer = csv.writer(votefile)
        for key,value in v1.voteobject.items():
            writer.writerow([key,value])

    if vote.count%4==0:
        blockx = Block().mineblock()
        with open('blockchain.txt','ab') as blockfile:
            pickle._dump(blockx,blockfile)
        print("block added")
    return redirect('/thanks')

@app.route('/thanks', methods = ['GET'])
def thank():
    return render_template('home.html')
EVoting = Blockchain()
EVoting.addGenesis()

if __name__ == '__main__':

    app.run(port = 5000)
    # data = EVoting.display()
    # print(data)

    with open('blockchain.txt','rb') as blockfile:
        for i in range(len(EVoting.chain)-1):
            data = pickle._load(blockfile)

            print("Block Height: ", data.height)
            print("Data in block: ", data.data)
            print("Merkle root: ", data.merkle)
            print("Difficulty: ", data.difficulty)
            print("Time stamp: ", data.timeStamp)
            print("Previous hash: ", data.prevHash)
            print("Nonce: ", data.nonce)


