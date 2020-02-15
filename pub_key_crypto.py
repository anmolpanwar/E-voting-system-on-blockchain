import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from hashlib import sha256

def genkey(keylen=1024):
    random_value = Random.new().read
    keypair = RSA.generate(keylen,random_value)
    return keypair

bobkey = genkey()
alicekey = genkey()

alicePK = alicekey.publickey()
bobPK = bobkey.publickey()

print(bobPK)
print(alicePK)
secret = "abc"
print("Message is:", secret)
