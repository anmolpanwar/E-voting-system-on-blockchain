import simplejson as json

def jsonify_votedata(votedatalist):
    jsondict = {'data':votedatalist[0],'key':votedatalist[1]}
    return json.dumps(jsondict)
