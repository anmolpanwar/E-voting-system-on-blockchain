import json

def savedb(func, *args, **kwargs):
    db_obj = args[0]
    path = db_obj.path
    fd = open(db_obj.path, "w")
    fd.write(json.dumps(db_obj.db, sort_keys=True, indent=4))
    fd.close()

def loaddb(func, *args, **kwargs):
    fd = open(args[0].path, "r").read()
    args[0].db = json.loads(fd)
