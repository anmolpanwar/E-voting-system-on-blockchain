# import jsonlib
import simplejson as json
l = [b'eafadfdws',b'werg']
my = {'data':b'eafadfdws', 'key':l[1]}
s = json.dumps(my)
print(s)
print(type(s))
myback = json.loads(s)
print(myback)
# myback['data'] = bytes(myback['data'],'utf-8')
# print(myback)
