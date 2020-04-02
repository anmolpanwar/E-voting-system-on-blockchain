from hashlib import *
from time import sleep

def sync_blocks(blockchain):
    for i in range(1,len(blockchain)):
        if blockchain[i].prevHash == blockchain[i-1].calcHash():
            continue
        else:
            return i, False

    return 0, True


def verify_block(block):

    check_1 = sha256((str(str(block.data)+str(block.nonce)+str(block.timeStamp)+str(block.prevHash))).encode('utf-8')).hexdigest()
    sleep(5)
    check_2 = sha256((str(str(block.data)+str(block.nonce)+str(block.timeStamp)+str(block.prevHash))).encode('utf-8')).hexdigest()

    return check_1==check_2
