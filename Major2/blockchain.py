#--libraries
from hashlib import *
import cryptography
from time import time
from flask import *
import csv
import pickle

#--project files
import enc as enc
import aes as aes

difficulty = 2

class vote:
    count = 0

    def __init__(self,hiddenvoterid,candidateID):
        self.hiddenvoterid = hiddenvoterid
        self.candidate = candidateID
        self.time = time()
        vote.count+=1
        self.votedata = [self.hiddenvoterid, self.candidate, self.time]

    #--vote gets a digital signature by voter's private key and gets signed by admin public key
    def encryptvote(self):
        self.votedata.append(enc.sign(voterkeys['sk'],bytes(sha256(str('---'.join(str(x) for x in self.votedata)).encode('utf-8')).hexdigest(),'utf-8')))
        return [aes.encrypt('***'.join(str(i) for i in self.votedata),voterkeys['aeskey']), enc.encrypt(Blockchain.adminpub,voterkeys['aeskey'])]


class Blockchain:

    chain = []

    #--administrator public/private key pair generated along with the blockchain initialization.
    #--the public key of admin will be used to encrypt the vote data for confidentiality
    adminpriv,adminpub = enc.rsakeys()

    def __init__(self):
        self.addGenesis()
        print('Blockchain initialized')

    @staticmethod
    #--genesis block creation has nothing to do with blockchain class...
    #--...but has to be created when blockchain is initialized
    def genesis():
        #--genesis block created
        gen = Block(0,"Let the real democracy rule!!", sha256(str("Let the real democracy rule!!").encode('utf-8')).hexdigest(), difficulty, time(),'',0,'Errrrrorrr')
        return gen

    @staticmethod
    def addGenesis():
        genesisblock = Blockchain.genesis()
        #--find the proof of work for genesis block
        genesisblock.nonce = genesisblock.pow()
        genesisblock.hash = genesisblock.calcHash()
        Blockchain.chain.append(genesisblock)

        #--information of genesis block written to the blockchain data file
        with open('temp/Blockchain.dat', 'ab') as genfile:
            pickle._dump(genesisblock, genfile)
        print("Genesis block added")

    @staticmethod
    def display():
        #--print the information of blocks of the blockchain in the console
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
    #--to clear up the votepool after a block has been mined...
    def update_votepool():
        votefile = open('temp/votefile.csv','w+')
        votefile.close()
        return "Done"


class Block:

    #--basic structure of block that will be created when the block is generated
    #--the data in the block will be updated later and block will be mined then.
    def __init__(self,height = 0,data = 'WARNING = SOME ERROR OCCURED',merkle = '0',difficulty = 0,time = 0,prevHash = '0',pow=0, hash = 'ERROR'):
        self.height = height                    #len(Blockchain.chain-1)
        self.data = data                        #loadvote()
        self.merkle = merkle                    #calculateMerkleRoot()
        self.difficulty = difficulty            #cryptography difficulty
        self.timeStamp = time                   #time()
        self.prevHash = prevHash                #previous block hash
        self.nonce = pow                        #proof of work function will find nonce
        self.hash = hash                        #hash of the current block

    #--The HEART OF BLOCKCHAIN - 'Proof-of-Work' function
    def pow(self,zero=difficulty):
        self.nonce=0
        while(self.calcHash()[:zero]!='0'*zero):
            self.nonce+=1
        return self.nonce

    #--calculate hash of a given block
    def calcHash(self):
        return sha256((str(str(self.data)+str(self.nonce)+str(self.timeStamp)+str(self.prevHash))).encode('utf-8')).hexdigest()


    @staticmethod
    def loadvote():
        votelist = []
        try:
            with open('temp/votefile.csv', mode = 'r') as votepool:
                csvreader = csv.reader(votepool)
                for row in csvreader:
                    votelist.append({'Vote Data':row[0],'Key':row[1]})
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
        self.height = len(Blockchain.chain)                 #len(Blockchain.chain-1)
        self.data = self.loadvote()                         #loadvote()
        self.merkle = self.merkleRoot()                     #calculateMerkleRoot()
        self.difficulty = difficulty                        # DIFFICULTY for the cryptographic puzzle
        self.timeStamp = time()                             #time()
        self.prevHash = Blockchain.chain[-1].calcHash()     #Calculate the hash of previous
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
invisiblevoter = '' # global variable used to hide voter's identity
voterkeys = {} #--voter's keys stored temporarily in this dictionary

@app.route('/signup', methods = ['POST'])
def votersignup():
    voterid = request.form['voterid']
    pin = request.form['pin']
    voterkeys['aeskey'] = aes.get_private_key(voterid)
    global invisiblevoter

#####-------ZERO KNOWLEDGE PROOF-------########
    invisiblevoter = str(sha256((str(voterid)+str(pin)).encode('utf-8')).hexdigest())

#--Voter re-signup check
    if voterid not in voterlist:
        voterlist.append(voterid)

#--If condition satisfied, voter can be allowed to vote and his data will be written on the database
        with open('temp/VoterID_Database.txt', 'a') as voterdata:
            voterdata.write(str(sha256(str(voterid).encode('utf-8')).hexdigest()))
            voterdata.write("\n")
        return render_template('vote.html')
#--If not, the voter will be redirected to a different page.
    else:
        return render_template('oops.html')


@app.route('/vote', methods = ['POST'])
def voter():
#--the voter is eligible if reached this page.
#--hence his own keys will be generated.
    voterkeys['sk'],voterkeys['pk'] = enc.rsakeys()         #--voter public/private key pair generated
    choice = request.form['candidate']
#--vote object created
    v1 = vote(invisiblevoter, int(choice))

    with open('temp/votefile.csv','a',newline="") as votefile:
        writer = csv.writer(votefile)
        writer.writerow(v1.encryptvote())
  
#---Current frequency to add and mine new blocks is after generation of every 4 votes
    if vote.count%4==0:
        blockx = Block().mineblock()
        with open('temp/blockchain.dat','ab') as blockfile:
            pickle._dump(blockx,blockfile)
        print("block added")
    return redirect('/thanks')

@app.route('/thanks', methods = ['GET'])
def thank():
    return render_template('thanks.html')


#--Blockchain initialized and Genesis block added
EVoting = Blockchain()
EVoting.addGenesis()

#--Created a file for voter database storage
f = open('temp/VoterID_Database.txt', 'w+')
f.close()


if __name__ == '__main__':

    app.run(port = 5000)
    Blockchain.display()
