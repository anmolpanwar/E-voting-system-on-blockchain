import simplejson as json

def jsonify_votedata(votedatalist):
    jsondict = {'data':votedatalist[0],'key':votedatalist[1]}
    #--this returns a string for the dictionary but converts the bytes data
    #--into string...so we need to convert it back when recieved on the
    #--other end of the peer....
    return json.dumps(jsondict)
