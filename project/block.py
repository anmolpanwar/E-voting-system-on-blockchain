class Block:

    def __init__(self,height,data,merkleRoot,difficulty,timeStamp,prevHash):
        self.height = height                   #len(Blockchain.chain-1)
        self.data = data                       #packdatainblock()
        self.merkleRoot = merkleRoot           #calculateMerkleRoot()
        self.difficulty = difficulty
        self.timeStamp = timeStamp             #time()
        self.prevHash = prevHash               #Blockchain.chain[len(Blockchain.chain)-1].hash
        self.nonce = self.pow()                #proof of work function will find nonce.
