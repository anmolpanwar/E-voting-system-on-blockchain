# E-voting-system-on-blockchain
An E-voting system based on blockchain, build from scratch.
![Image description](https://github.com/anmolpanwar/E-voting-system-on-blockchain/blob/master/Major2/cover.png)


# What is a blockchain?
 A blockchain is a distributed decentralized digital ledger that holds information and can be used to maintain transparency in a system and the integrity of the data in that system.

 A 'Blockchain', as it sounds, is a chain of blocks (a small file that holds some data and can not be altered or tampered with) cryptographically linked together and replicated among a large network of people with no-one having control.
 
 The blocks are linked together cryptographically such that any block in that chain contains the "Hash" of previous block (with an exception of first block of blockchain). A hash is a fixed length code that is output from the data itself and any change in that data will completely change the resulting hash.
 So, if someone tries to change some data from some particular block, lets say a person tries to change a record in the data in the 3rd block of blockchain, which consists of 100 blocks at present, then any slight change in the data will result changing the hash of that block. This hash is stored with the data of the next block (4th block), so the change in data of 3rd block changes the hash of 3rd block which in turn changes the hash of the 4th block and so on. The whole blockchain is invalidated and thus it is almost impossible to change the data on the blockchain. Thus, it is a decentralised distributed immutable digital ledger.
 
 # Signing and encrypting transactions
 In this program, as the voter signs up successfully and chooses the candidate, the vote data - Hidden voterID (SHA256 hash of (voterID appended with PIN)), candidateID and the current timestamp gets digitally signed by the voter's private key (generated at successful sign up) and then encrypted with AES algorithm and the key of the algorithm is encrypted with the Administrator's public key. This whole set of data - Vote data, encrypted AES key and the voter's public key is packed as a single unit of data and stored in a pool of pending transactions and broadcasted on the network to other peers. <br>
Similarly the data gets accumulated in the temporary pool by other peers as well. Then the transactions from that pool (a list of transactions in this program) are picked up by the nodes and packed into a block and the nodes begin to compete each other to find the correct Proof-of-Work for the block.
 
 # Implementing Proof-of-Work (PoW)
 Proof of work is a brilliant way to ensure the integrity of the data. The algorithm dictates that - a node must go through a large amount of computational work in order to add the block to the blockchain because once added the data in the block can never be modified. Hence, to prevent an attacked from injecting a fraudulent database state (modifying the data and making everyone believe and follow that database state) because in order to do so, the attacker must go through a large amount of computational work to change one block, and then the one that follows it and then the next one and so on. This is practically impossible to surpass the work done by honest nodes collectively (versus the attacker himself) unless the attacker possesses more than 50% of the computational resources.
 
 This is achieved by scanning for a value (a number) that when appended at the end of the data and hashed with SHA-256 gives the output with a certain number of zeroes at the beginning of the hash. So we have no option other than just "guessing and checking" the hash again and again after recursively changing the number and checking the hash untill we hit the target hash.
 
 This is known as Proof of Work. It proves that a node underwent a good amount of work and spent a considerable amount of time to find that number to achieve the target hash.


 For a practical scenario - the length of the output hash of a SHA256 algorithm is 256 bits. The bitcoin protocol (by default) dictates that the hash for each block must begin with AT LEAST 30 zeroes (however, that number of zeros is regularly scaled up or down so that mining a new block takes about 10 minutes on an average). This means we have to check AT MOST 2^30 possible outcomes and an AVERAGE of 2^29 outcomes to output the desired hash.
 This probability is close to 1 in a Billion and for an average computer, this would take several minutes to compute but the devices that are especially designed to compute hashes and nothing else can increase the efficiency greatly and thus all the miners collectively maintain an average time of 10 minutes. Those devices are known as ASIC (Application Specific Integrated Circuits) device. They consume a large amount of power and thus PoW is a very power hungry consensus algorithm.

> Blockchain really is a miraculous technology but still there are reasons that steer it away from widespread adoption. To know more, refer to my article @ medium
> #### Here - https://medium.com/@anmolpanwar8/heres-why-blockchain-is-not-yet-ready-to-gain-traction-ac92c323d84d  
<br>

## Instructions  
### \[Note: The project files are in the folder - Major2. Rest all the files are experiment and a part of 'rough work', not related to project.]
<br>

**Directory structure for the project**  
| - - **\<Project folder name\>/**  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `blockchain.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `enc.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `aes.py`<br>
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `broadcast.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `jsonify.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `verification.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `takeyourkeyhome.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `listener.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `election_results.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - `bar_chart.py`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - **templates/**  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `vote.html`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `oops.html`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `home.html`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `thanks.html`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - **static/**  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `shhhhhh.JPG`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `cong.png`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `image.png`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `nota.png`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - **styles/**  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `style.css`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `10.jpeg`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `vote.css`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `cong.png`  
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | - - `image.png`  
| &nbsp;&nbsp;&nbsp;&nbsp; | - - **temp/**  
<br>
<br>
**Steps to run the application program:**  
* Install the necesaary libraries  
* Change the IP address (and port number, optional) to your computer's IP in `listener.py`<br>
* Run `listener.py`<br>
* Run `blockchain.py`  
* The files in **temp/** will be created automatically  
* Open `localhost:<port number>`
* Sign up as voter
* Choose a candidate
* Repeat
* Watch the blockchain developing behind the scenes
<br>
<br>
<br>

## hidden_msg = [84, 104, 97, 110, 107, 32, 89, 111, 117]
## decrypt = [chr(i) for i in hidden_msg]
## print(' '.join(decrypt))
