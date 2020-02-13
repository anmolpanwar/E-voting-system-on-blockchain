from time import time
class vote:

    count = 0

    def __init__(self,candidateID):
        self.candidate = candidateID
        self.time = time()
        vote.count+=1
    # def abs(self):
    #     pass

v1 = vote(2)
v2 = vote(8)
print (vote.__dict__)
