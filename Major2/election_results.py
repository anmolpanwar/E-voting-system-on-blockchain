import pickle
import hashlib
import enc
import aes
from blockchain import Block


def gather_votes():
    votelist = []
    with open('temp/Blockchain.dat', 'rb') as blockfile:

        gen = pickle._load(blockfile)
        while True:
            try:
                block = pickle._load(blockfile)
                votelist.extend(block.data)
            except EOFError:
                break
    return votelist

# def unlock_key(locked_key,adminsk):
#     votedata_key = bytes(locked_key,'utf-8')
#     return enc.decrypt(adminsk, votedata_key)
#
#
# def decrypt_vote(locked_key, adminsk, data):
#     aeskey = unlock_key(locked_key,adminsk)
#     data = bytes(data, 'utf-8')
#     unlocked = aes.decrypt(data,aeskey)
#     votedata = unlocked.split('***')
#     votedata[1]=int(votedata[1])
#     votedata[2]=int(votedata[2])
#     votedata[3]=bytes(votedata[3][2:-1],'utf-8')
#     return votedata
#
# def get_result(adminsk):
#     votelist = gather_votes()
#     candidates = []
#     for vote in votelist:
#         data = decrypt_vote(vote['Key'],adminsk,vote['Vote Data'])
#         candidates.append(data[1])
#     return candidates

def get_result(adminsk):
    votelist = []
    with open('temp/Blockchain.dat', 'rb') as blockfile:
        gen = pickle._load(blockfile)
        while True:
            try:
                block = pickle._load(blockfile)
                votelist.extend(block.data)
            except EOFError:
                break
    candy = []
    for vote in votelist:
        votedata_key = bytes(vote['Key'],'utf-8')
        aeskey = enc.decrypt(adminsk, votedata_key)
        unlocked = aes.decrypt(bytes(vote['Vote Data'],'utf-8'),aeskey)
        unlocked = str(unlocked)[2:-1]
        votedata = unlocked.split('***')
        votedata[1]=int(votedata[1])
        candy.append(votedata[1])

    return candy
