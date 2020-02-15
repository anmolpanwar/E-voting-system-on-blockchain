import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
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
secret = "abc".encode()
print("Message is:", secret)
keyobj = PKCS1_OAEP.new(key = bobPK)
bob = keyobj.encrypt(secret)
print(bob)
keyobj1 = PKCS1_OAEP.new(key = bobkey)
dec = keyobj1.decrypt(bob)
print(dec)
