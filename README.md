# E-voting-system-on-blockchain
An E-voting system based on blockchain, build from scratch.
![Image description](https://raw.githubusercontent.com/anmolpanwar/E-voting-system-on-blockchain/master/path/to/img.png)


# What is a blockchain?
 A blockchain is a distributed decentralized digital ledger that holds information and can be used to maintain transparency in a system and the integrity of the data in that system.

 A 'Blockchain', as it sounds, is a chain of blocks (a small file that holds some data and can not be altered or tampered with) cryptographically linked together and replicated among a large network of people with no-one having control.
 
 The blocks are linked together cryptographically such that any block in that chain contains the "Hash" of previous block (with an exception of first block of blockchain). A hash is a fixed length code that is output from the data itself and any change in that data will completely change the resulting hash.
 So, if someone tries to change some data from some particular block, lets say a person tries to change a record in the data in the 3rd block of blockchain, which consists of 100 blocks at present, then any slight change in the data will result changing the hash of that block. This hash is stored with the data of the next block (4th block), so the change in data of 3rd block changes the hash of 3rd block which in turn changes the hash of the 4th block and so on. The whole blockchain is invalidated and thus it is almost impossible to change the data on the blockchain. Thus, it is a decentralised distributed immutable digital ledger.
 
 # Signing transactions
 In this program we create transactions by manually giving the addresses of both the sender and receiver along with the amount and this information along with the current timestamp gets stored in a pool of pending transactions. Then the transactions from that pool (a list of transactions in this program) are picked up and hashed using the hashing algorithm SHA-256 and then by RIPEMD-160 and a merkle root structure is created.
 
 # Implementing Proof-of-Work (PoW)
 Proof of work is a brilliant way to ensure the integrity of the data. The algorithm dictates that - a node must go through a large amount of computational work in order to add the block to the blockchain because once added the data in the block can never be modified. Hence, to prevent an attacked from injecting a fraudulent database state (modifying the data and making everyone believe and follow that database state) because in order to do so, the attacker must go through a large amount of computational work to change one block, and then the one that follows it and then the next one and so on. This is practically impossible to surpass the work done by honest nodes collectively (versus the attacker himself) unless the attacker possesses more than 50% of the computational resources.
 
 This is achieved by scanning for a value (a number) that when appended at the end of the data and hashed with SHA-256 gives the output with a certain number of zeroes at the beginning of the hash. So we have no option other than just "guessing and checking" the hash again and again after recursively changing the number and checking the hash untill we hit the target hash.
 
 This is known as Proof of Work. It proves that a node underwent a good amount of work and spent a considerable amount of time to find that number to achieve the target hash.


 For a practical scenario - the length of the output hash of a SHA256 algorithm is 256 bits. The bitcoin protocol dictates that the hash for each block must begin with AT LEAST 30 zeroes. This means we have to check AT MOST 2^30 possible outcomes and an AVERAGE of 2^29 outcomes to output the desired hash.
 This probability is close to 1 in a Billion and for an average computer, this would take approximately 15 minutes to compute and close to 10 minutes for an ASIC (Application Specific Integrated Circuits) device; a device specially designed to compute hashes and nothing else.
 If the average time of adding a new block gets lesser, the difficulty is increased by the bitcoin protocol itself.

Refer to my article - https://medium.com/@anmolpanwar8/heres-why-blockchain-is-not-yet-ready-to-gain-traction-ac92c323d84d
