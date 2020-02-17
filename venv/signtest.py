from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii

sk = RSA.generate(1024, Crypto.Random.new().read)
skt = binascii.hexlify(sk.exportKey(format='DER')).decode('ascii')
print(skt)
