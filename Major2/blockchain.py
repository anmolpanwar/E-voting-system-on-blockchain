#--libraries
from hashlib import *
import cryptography
from time import time,sleep
from flask import *
import csv
import pickle
import simplejson as json
import threading as thr
import os

#--project files
import enc as enc
import aes as aes
import peer2 as pp

#--Global variables
DIFFICULTY = 2

BLOCK_TIME_LIMIT = 15 #--(seconds)

PROJECT_PATH = "~/Documents/PycharmProjects/python practice/Major2"

class vote:
    count = 0

    def __init__(self,hiddenvoterid,candidateID):
        #--voterid hashed with PIN (ZKP)
        self.hiddenvoterid = hiddenvoterid
        self.candidate = candidateID
        self.time = time()
        self.votedata = [self.hiddenvoterid, self.candidate, self.time]

    #--vote gets a digital signature by voter's private key and gets signed by admin public key
    def encryptvote(self):
        #--the data of the vote (in the votedata list) will be first hashed by SHA-256
        #--then, the data will be converted into bytes and signed by voter's private key
        #--and that hashed signature will be appended with votedata itself
        self.votedata.append(enc.sign(voterkeys['sk'], bytes(sha256(str('---'.join(str(x) for x in self.votedata)).encode('utf-8')).hexdigest(),'utf-8')))

        #--now that whole data (the new votedata list) will be encrypted by AES encryption
        #-- and the shared key of AES will be encrypted with admin's public key
        #-- this data will be broadcasted and saved into the unconfirmed votepool and will be added in the block
        return [aes.encrypt('***'.join(str(i) for i in self.votedata),voterkeys['aeskey']), enc.encrypt(Blockchain.adminpub,voterkeys['aeskey'])]

    #--keep track of no. of votes
    @classmethod
    def inc_votecount(cls):
        cls.count+=1

    @classmethod
    def get_votecount(cls):
        #--return the current number of votes
        return cls.count


class Blockchain:
    #--holds the info of chain of blocks as objects
    chain = []

    #--administrator public/private key pair generated along with the blockchain initialization.
    #--the public key of admin will be used to encrypt the vote data for confidentiality
    adminpriv,adminpub = enc.rsakeys()
    with open('temp/Adminkeys.txt', 'wb') as adminkeyfile:
        pickle._dump(adminpriv,adminkeyfile)
        pickle._dump(adminpub,adminkeyfile)

    def __init__(self):
        self.addGenesis()
        print('Blockchain initialized')

    @staticmethod
    #--genesis block creation has nothing to do with blockchain class...
    #--...but has to be created when blockchain is initialized
    def genesis():

        #--genesis block created
        gen = Block(0,"Let the real democracy rule!!",0, sha256(str("Let the real democracy rule!!").encode('utf-8')).hexdigest(), DIFFICULTY, time(),'',0,'Errrrrorrr')
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
        try:
            with open('temp/blockchain.dat','rb') as blockfile:
                for i in range(len(EVoting.chain)):
                    data = pickle._load(blockfile)

                    #--print all data of a block
                    print("Block Height: ", data.height)
                    print("Data in block: ", data.data)
                    print("Number of votes: ",data.number_of_votes)
                    print("Merkle root: ", data.merkle)
                    print("Difficulty: ", data.DIFFICULTY)
                    print("Time stamp: ", data.timeStamp)
                    print("Previous hash: ", data.prevHash)
                    print("Block Hash: ", data.hash)
                    print("Nonce: ", data.nonce, '\n\t\t|\n\t\t|')

        except FileNotFoundError:
            print("\n.\n.\n.\n<<<File not found!!>>>")


    @staticmethod
    #--to clear up the votepool after a block has been mined...
    def update_votepool():
        try:
            votefile = open('temp/votefile.csv','w+')
            votefile.close()

        except Exception as e:
            print("Some error occured: ", e)
        return "Done"

    def is_votepool_empty(self):
    #--path to votefile
        my_path = PROJECT_PATH.join('/temp/votefile.csv')
    #--will return true if file exists and has no data
        if os.path.isfile(os.path.expanduser(my_path)) and os.stat(os.path.expanduser(my_path)).st_size==0:
            return True
    #--False otherwise
        return False


class Block:

    #--basic structure of block that will be created when the block is generated
    #--the data in the block will be updated later and block will be mined then.
    def __init__(self,height = 0,data = 'WARNING = SOME ERROR OCCURED',votes = 0,merkle = '0',DIFFICULTY = 0,time = 0,prevHash = '0',pow=0, hash = 'ERROR'):
        self.height = height                    #len(Blockchain.chain-1)
        self.data = data                        #loadvote()
        self.number_of_votes = votes            #votecount per block
        self.merkle = merkle                    #calculateMerkleRoot()
        self.DIFFICULTY = DIFFICULTY            #cryptography difficulty
        self.timeStamp = time                   #time()
        self.prevHash = prevHash                #previous block hash
        self.nonce = pow                        #proof of work function will find nonce
        self.hash = hash                        #hash of the current block

    #--The HEART OF BLOCKCHAIN - 'Proof-of-Work' function
    def pow(self,zero=DIFFICULTY):
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
        votecount = 0
        try:
            with open('temp/votefile.csv', mode = 'r') as votepool:
                csvreader = csv.reader(votepool)
                for row in csvreader:
                    votelist.append({'Vote Data':row[0],'Key':row[1]})
                    votecount+=1
            return votelist,votecount

        except(IOError,IndexError):
            pass

        finally:
            print("data loaded in block")
            print("Updating unconfirmed vote pool...")
            print (Blockchain.update_votepool())


    #--create a merkle tree of vote transactions and return the merkle root of the tree
    def merkleRoot(self):
        return 'congrats'

    #--fill the block with data and append the block in the blockchain
    def mineblock(self):
        self.height = len(Blockchain.chain)                 #len(Blockchain.chain-1)
        self.data,self.number_of_votes = self.loadvote()    #loadvote() and return number of votes in current block
        self.merkle = self.merkleRoot()                     #MerkleRoot()
        self.DIFFICULTY = DIFFICULTY                        #DIFFICULTY for the cryptographic puzzle
        self.timeStamp = time()                             #time()
        self.prevHash = Blockchain.chain[-1].calcHash()     #Calculate the hash of previous
        self.nonce = self.pow()                             #Calculate nonce
        self.hash = self.calcHash()                         #compute hash of current block
        Blockchain.chain.append(self)

        return self     #--return block object

#########################################################################

#------------------------------FLASK APP--------------------------------#

app = Flask(__name__)


@app.route('/')
#--the login page, home page
def home():
    return render_template('home.html')

voterlist = [] #--to keep duplicates out
invisiblevoter = '' #--global variable used to hide voter's identity
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
    voterkeys['sk'],voterkeys['pk'] = enc.rsakeys()         #--voter public/private key pair generated here
    choice = request.form['candidate']

#--vote object created
    v1 = vote(invisiblevoter, int(choice))
    vote.inc_votecount()

#--votedata digitally signed and encrypted and sent to the temporary pool
    with open('temp/votefile.csv','a',newline="") as votefile:
        writer = csv.writer(votefile)
        encvotedata = v1.encryptvote()
        writer.writerow(encvotedata)

#--and broadcasted to other peers on the network
    pp.send_to_peer('192.168.0.135',9999,encvotedata)

#---Current frequency to add and mine new blocks is after generation of every 4 votes
    # if vote.count%4==0:
    #     blockx = Block().mineblock()
    #     with open('temp/blockchain.dat','ab') as blockfile:
    #         pickle._dump(blockx,blockfile)
    #     print("block added")
    return redirect('/thanks')


@app.route('/thanks', methods = ['GET'])
def thank():
    #--thank you page
    return render_template('thanks.html')


#--Blockchain initialized and Genesis block added
EVoting = Blockchain()

#--Created a file for voter database storage
f = open('temp/VoterID_Database.txt', 'w+')
f.close()

#--inline methode that runs parallel to the program
def inlinetimer():
    while True:
        sleep(BLOCK_TIME_LIMIT)        #--global variable
        #--sleep for 15 seconds --> mine a block --> repeat
        blockx = Block().mineblock()
        with open('temp/blockchain.dat','ab') as blockfile:
            pickle._dump(blockx,blockfile)
        print("block added")

#--seperate thread running in the background
def mineblocktimer():
    timerthread = thr.Thread(target=inlinetimer)
    timerthread.start()

mineblocktimer()


if __name__ == '__main__':
    #--run flask application
    app.run(port = 5000)
    #--after flask application stops
    #--load the remaining data in the temporary vote pool
    #--into a block and mine it
    if not EVoting.is_votepool_empty():
        lastblock = Block().mineblock()
        with open('temp/blockchain.dat','ab') as blockfile:
            pickle._dump(lastblock,blockfile)
        print("block added")

    Blockchain.display()
    print("\n\n\n", end = '')
    print("Total number of votes:",vote.get_votecount())
