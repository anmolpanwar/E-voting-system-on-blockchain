from hashlib import *

def verify_blockchain(blockchain):
    for i in range(1,len(blockchain)):
        if blockchain[i].prevHash == blockchain[i-1].calcHash():
            continue
        else:
            error_msg ="""+-----------------------------------------+
            |                                         |
            | Somebody messed up at Block number - {} |
            |                                         |
            +-----------------------------------------+""".format(i)

            return error_msg, False

    return True
