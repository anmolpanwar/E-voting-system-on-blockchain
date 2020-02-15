from os import chmod
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
with open("/tmp/private.key", 'wb') as content_file:
    chmod("/tmp/private.key", 384)
    content_file.write(key.exportKey('PEM'))
pubkey = key.publickey()
with open("/tmp/public.key", 'wb') as content_file:
    content_file.write(pubkey.exportKey('OpenSSH'))
