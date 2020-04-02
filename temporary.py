import enc as enc
import Major2.jsonify as js
import time
import pickle as pk
import simplejson as js
keys = {}
keys['private'],keys['public'] = enc.rsakeys()
#
# class vote:
#
#     def __init__(self,hiddenvoterid,candidateID,pubkey):
#         #--voterid hashed with PIN (ZKP)
#         self.hiddenvoterid = hiddenvoterid
#         self.candidate = candidateID
#         self.pubkey = pubkey
#         self.time = time.time()
#         self.votedata = [self.hiddenvoterid, self.candidate, self.time]
#
# v1 = vote('7112a70d9ef40de8a89ed2845cae954901aa6a67200e29bcc9344a0bbdb8f35a',1,keys['public'])
#print(keys['public'])
keyobj = pk._dumps(keys['public'])
print(keyobj)

ls = [b'C6yOrzSFsfy4bQ172sS2PRmpTmGa8euo+xg', b'rTDAVInfyDn+WO72sS2PRmpTmGykx74Kz/HC4=']
ls.append(str(keyobj)[2:-1])
jsondict = {'pubkey':ls[2],'data':ls[0],'key':ls[1]}

#

jd = js.dumps(jsondict)
ds = js.loads(jd)
vpubkey = bytes(ds['pubkey'],'utf-8')
vpubkeyORIGINAL = vpubkey.decode('unicode-escape').encode('ISO-8859-1')
print(vpubkeyORIGINAL)
VOTER_PUBLIC_KEY = pk._loads(vpubkeyORIGINAL)
print(VOTER_PUBLIC_KEY)
print(VOTER_PUBLIC_KEY==keys['public'])

# jsondict['pubkey'] = str(keyobj)
# #print(jsondict)
#
# news = jsondict['pubkey']
# newnew = news[2:-1]
# b = bytes(newnew,'utf-8')
# print()
# newbie = b.decode('unicode-escape').encode('ISO-8859-1')
# print(newbie)
#
# ch = pk._loads(newbie)
#
# print(ch==keys['public'])
