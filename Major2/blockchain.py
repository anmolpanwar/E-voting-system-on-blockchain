from hashlib import *
# from cryptography.hazmat.primitives.asymmetric import *
import cryptography
from time import time
from flask import *
import csv
import pickle
import enc

difficulty = 2

class vote:

    count = 0

    def __init__(self,hiddenvoterid,candidateID):
        self.hiddenvoterid = hiddenvoterid
        self.candidate = candidateID
        self.time = time()
        vote.count+=1
        self.votedata = [self.hiddenvoterid, self.candidate, self.time]

    def signvote(self):
        pass

class Blockchain:

    chain = []

    def __init__(cls):
        print('Blockchain initialized')
        pass

    def genesis(self):
        gen = Block(0,"Let the real democracy rule!!", sha256(str("Let the real democracy rule!!").encode('utf-8')).hexdigest(), difficulty, time(),'',0,'Errrrrorrr')
        return gen

    def addGenesis(self):
        genesisblock = self.genesis()
        genesisblock.nonce = genesisblock.pow()
        genesisblock.hash = genesisblock.calcHash()
        Blockchain.chain.append(genesisblock)
        with open('temp/Blockchain.dat', 'ab') as genfile:
            pickle._dump(genesisblock, genfile)
        print("Genesis block added")

    @staticmethod
    def display():
        with open('temp/blockchain.dat','rb') as blockfile:
            for i in range(len(EVoting.chain)):
                data = pickle._load(blockfile)

                print("Block Height: ", data.height)
                print("Data in block: ", data.data)
                print("Merkle root: ", data.merkle)
                print("Difficulty: ", data.difficulty)
                print("Time stamp: ", data.timeStamp)
                print("Previous hash: ", data.prevHash)
                print("Block Hash: ", data.hash)
                print("Nonce: ", data.nonce, '\n\t\t|\n\t\t|')

    @staticmethod
    def update_votepool():
        votefile = open('temp/votefile.csv','w+')
        votefile.close()
        return "Done"


class Block:

    def __init__(self,height = 0,data = 'WARNING = SOME ERROR OCCURED',merkle = '0',difficulty = 0,time = 0,prevHash = '0',pow=0, hash = 'ERROR'):
        self.height = height                    #len(Blockchain.chain-1)
        self.data = data                        #loadvote()
        self.merkle = merkle                    #calculateMerkleRoot()
        self.difficulty = difficulty            #cryptography difficulty
        self.timeStamp = time                   #time()
        self.prevHash = prevHash                #previous block hash
        self.nonce = pow                        #proof of work function will find nonce
        self.hash = hash

    def pow(self,zero=difficulty):
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
            with open('temp/votefile.csv', mode = 'r') as votepool:
                csvreader = csv.reader(votepool)
                for row in csvreader:
                    votelist.append({'VoterID':row[0],'CandidateID':row[1], 'Time':row[2]})
            return votelist

        except(IOError,IndexError):
            pass

        finally:
            print("data loaded in block")
            print("Updating unconfirmed vote pool...")
            print (Blockchain.update_votepool())



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
        self.hash = self.calcHash()
        Blockchain.chain.append(self)

        return self

#########################################################################

#------------------------------FLASK APP--------------------------------#

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

voterlist = []
invisiblevoter = ''

@app.route('/signup', methods = ['POST'])
def votersignup():
    voterid = request.form['voterid']
    pin = request.form['pin']
    global invisiblevoter
    invisiblevoter = str(sha256((str(voterid)+str(pin)).encode('utf-8')).hexdigest())
    if voterid not in voterlist:
        voterlist.append(voterid)
        with open('temp/VoterID_Database.txt', 'a') as voterdata:
            voterdata.write(str(sha256(str(voterid).encode('utf-8')).hexdigest()))
            voterdata.write("\n")
        return render_template('vote.html')
    else:
        return render_template('oops.html')


@app.route('/vote', methods = ['POST'])
def voter():
    choice = request.form['candidate']
    v1 = vote(invisiblevoter, int(choice))
    with open('temp/votefile.csv','a',newline="") as votefile:
        writer = csv.writer(votefile)
        writer.writerow(v1.votedata)

    if vote.count%4==0:
        blockx = Block().mineblock()
        with open('temp/blockchain.dat','ab') as blockfile:
            pickle._dump(blockx,blockfile)
        print("block added")
    return redirect('/thanks')

@app.route('/thanks', methods = ['GET'])
def thank():
    return render_template('thanks.html')


EVoting = Blockchain()
EVoting.addGenesis()
f = open('temp/VoterID_Database.txt', 'w+')
f.close()


if __name__ == '__main__':

    app.run(port = 5000)
    Blockchain.display()
