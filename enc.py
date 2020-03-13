import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64


#Creating Private Key of 1024 bits and Public Key
def rsakeys():
     length=1024
     privatekey = RSA.generate(length, Random.new().read)
     publickey = privatekey.publickey()
     return privatekey, publickey


#function for encryption which takes public key, plain text as arguments. This function returns a base64 encoded string of ciphertext.
def encrypt(rsa_publickey,plain_text):
     cipher_text=rsa_publickey.encrypt(plain_text,32)[0]
     b64cipher=base64.b64encode(cipher_text)
     return b64cipher


#For decryption, we create a function that takes ciphertext and private key as arguments.
def decrypt(rsa_privatekey,b64cipher):
     decoded_ciphertext = base64.b64decode(b64cipher)
     plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
     return plaintext


#Function sign takes two arguments, private key and data. This function returns base64 string of digital signature.
def sign(privatekey,data):
    return base64.b64encode(str((privatekey.sign(data,''))[0]).encode())


#Function verify takes two arguments, public key and digital signature in base64 and returns a boolean True if signature matches the data, False if not matches data.
def verify(publickey,data,sign):
     return publickey.verify(data,(int(base64.b64decode(sign)),))


if __name__=='__main__':
     rpriv,rpub = rsakeys()
     spriv,spub = rsakeys()

     rl = []
     signed = sign(spriv,bytes(rl))
     encrypted = encrypt(rpub,signed)
     signed1 = decrypt(rpriv,encrypted)
     print(verify(spub,bytes(rl),signed1))
