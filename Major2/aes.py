import base64
from hashlib import *
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
import enc, time

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

##############-----pw will not be input by user, rather be generated by hashing the voterID itself. Makes it unique.
pw = 'anmol'

def get_private_key(pw):
    password = str(sha256((pw).encode('utf-8')).hexdigest())
    salt = b"this is a salt and the m0re c0mplex th!s wi11 be, the m0re d!44icult w1!! b3 the K37"
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key


def encrypt(raw, private_key):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, private_key):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

if __name__=='__main__':

    voterpriv, voterpub = enc.rsakeys()
    adminpriv, adminpub = enc.rsakeys()

    l = ['eee9ca050b625c9a8206beb29e5687d915f70aaa061993d9ea5bdf2041c66a26', 1, time.time()]
    #--all 3 elements of votedata appended together as a string and hashed
    #--hash converted to bytes
    #--then signed by voter's private key
    #--then appended back to the list
    l.append(enc.sign(voterpriv,bytes(sha256(str('---'.join(str(x) for x in l)).encode('utf-8')).hexdigest(),'utf-8')))
    #--now the list elements are again appended together as string and encrypted
    #--using the shared key
    #--this encrypted data is to be added to vote pool and sent to other as well.
    #--and the key must be encrypted by RSA algotithm using the public key of admin(reciever)

    vote = {'data': encrypt('***'.join(str(i) for i in l),get_private_key(pw)), 'key': enc.encrypt(adminpub,get_private_key(pw))}
    print(vote)
    #--decrypt key
    deckey = enc.decrypt(adminpriv,vote['key'])

    decrypted = decrypt(vote['data'],get_private_key(pw)).decode('utf-8')
    print(decrypted)
    ourdata = decrypted.split('***')
    ourdata[1] = int(ourdata[1])
    ourdata[2] = float(ourdata[2])
    ourdata[3] = bytes(((ourdata[3].replace('b\'','')).replace('\'','')),'utf-8')

    # First let us encrypt secret message
    # encrypted = encrypt("This is a secret message", pw)
    # print(encrypted)
    #
    #
    # # Let us decrypt using our original password
    # decrypted = decrypt(encrypted, pw)
    # print(bytes.decode(decrypted))
