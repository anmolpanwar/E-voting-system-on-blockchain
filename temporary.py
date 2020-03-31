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

ls = [b'Cz6GPw+07hqqNnJ3YPHvU/0RlT4lhyXxEA3RUgOE8h1xqQFkUREkHC9NXvAvQ1RI2rbFu5t26jhfJuasgJ/APubIn8RyvmrAUfz0OUWjDaMsObk9/lF+ibNU8DPhEYv3beUnf233EBLTzYc2enYG1eX8UjBM4zghFbo73YD2rVawwAeT4W8n+miviCnrcDwgdnv/xBpISLK24PttEs+WKh5X/Rb4gjfSTrw+mG+Q97HYRxGupbK2a5XFMIl+Tm+m/jluBb1Ectf55Xe1VsNhofJdVlcUgZ5INC56MYyjsDlhYIN4W5jF1ImJMVkp5clJkwsC3ksGMEWsmB70v49q+gXZys8csCBph91Esrj4coZy29SUNeNy9siw2721QfaWLaXEJuVMO+MI2EYSm7xndZinPTR//SvtQkhTLZOwmb0igtleClgR7yjjrZztyU9dX6yp9b39nN1l6YO5ZUHr1eq5y0LEHHzkwMqsoq9zi1t+x1eyk8v84tAkaLFtJqLHoq/sBVLk4r4FXgS02vqdwFnvtyvW48HzHfwK50mqZSC2wAEuqDCUSFYRpTlClN4Y/bPeD4P8bWpuLorKtKMCpOjADO3IcQ1acrdGcdM+hqK4wl0vatHQSsf21MWkXvOnXtlNLpEs22wHu7z9r0+1f10OqZiLjqNKKNiFsYODq5BojrzSFsfy4bQ1a8euo+xg', b'rTYwNswB8+EJrq83hAF+rAaSkN6PLNCf6NaVsA4ag4HEl0vnc04H7mmR5Ari+7sCDajLsQI99ececbGD4f9flcr39C+KT6NMqvvu+bdIgQZnaIlgmb2cDswrrCra+jiSAbFfKeNIDAVInfyDn+WO72sS2PRmpTmGykx74Kz/HC4=']
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
