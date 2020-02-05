#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import json
from collections import OrderedDict
from decorators import wrap
from utils import savedb, loaddb
# ---- Logic Start ----------------------#

class Hashlite:
    def __init__(self, path, reset=False):
        self.path = path
        if os.path.exists(path):
           f = open(path, "r").read() 
           self.db = json.loads(f)
        elif reset or not os.path.exists(path):
            self.db = {}
            with open(self.path, 'w') as dbfile:
                dbfile.write(json.dumps(self.db))

    @wrap(loaddb, savedb)
    def set(self, key=None, value=None, subkey=None, force=False):
        try:
            if subkey!=None and self.db.get(key, False) !=False:
                if type(self.db.get(key, None)) is list:
                    self.db[key][subkey] = value
                    return True
                if type(self.db.get(key, None)) is dict:
                    r = self.db[key].setdefault(subkey, value )
                    if r == value:
                        return True
                    elif force == True:
                        self.db[key] = value
                        return True
        except Exception as e:
            return False
        if not subkey:
            r = self.db.setdefault(key, value)
            if r == value:
                return True
            elif force == True:
                self.db[key] = value
                return True
        return False 
      
    @wrap(loaddb, savedb)
    def get(self, key=None, subkey=None):
        """
        subkey can be positional key or alphabetical
        """
        if subkey:
            if type(self.db.get(key, None)) is list:
                if subkey < len(self.db.get(key)):
                    return self.db.get(key)[subkey] 
                else: 
                    return None
            if type(self.db.get(key, None)) is dict:
                return self.db.get(key).get(subkey, None)
        if not key and not subkey:
            return self.db
        return self.db.get(key, None)
        
        
    @wrap(loaddb, savedb)
    def listcreate(self, key=None, subkey=None, force=False):
        if subkey and self.db.get(key, None) != None:
            if force:
                # when you want that key to reset 
                self.db[key][subkey] = []
            else:
                # when db[key] is a list we dont perform
                if type(self.db[key]) is list:
                    print("Operation cant be performed")
                # when its a dict use setdefault and confirm it happened or not
                if type(self.db[key]) is dict:
                    r = self.db[key].setdefault(subkey, [])
                    if r == []:
                        return True
                    else:
                        return False
                
        else:
            if force:
                self.db[key] = []
            else:
                r = self.db.setdefault(key, [])
                if r == []:
                    return True
                else:
                    return False

    @wrap(loaddb, savedb)
    def dictcreate(self, key=None, subkey=None, force=False):
        if subkey and self.db.get(key, None) != None:
            if force:
                # when you want that key to reset
                self.db[key][subkey] = {}
            else:
                # when db[key] is a list we dont perform
                if type(self.db[key]) is list:
                    print("Operation cant be performed")
                # when its a dict use setdefault and confirm it happened or not
                if type(self.db[key]) is dict:
                    r = self.db[key].setdefault(subkey, {})
                    if r == {}:
                        return True
                    else:
                        return False
        else:
            if force:
                self.db[key] = {}
            else:
                r = self.db.setdefault(key, {})
                if r == {}:
                    return True
                else:
                    return False

    @wrap(loaddb, savedb)
    def listpop(self, key=None, subkey=None):
        if subkey != None and self.db.get(key, False): 
            if type(self.db[key]) is list:
                # operation not permitted
                return False
            if type(self.db[key]) is dict and subkey in self.db[key].keys():
                try:
                    return self.db[key][subkey].pop()
                except IndexError as e:
                    # coz of empty list cant be popped
                    return False
            else:
                # need to return proper messages
                return False
        else:
            try:
                if type(self.db.get(key, None)) is list:
                    return self.db[key].pop()
                else:
                    # coz operation not permitted
                    return False
            except IndexError as e:
                return False 
        return False

    @wrap(loaddb, savedb)
    def listpush(self, key=None, value=None, subkey=None):
        if subkey != None and type(self.db.get(key, False)) is dict:
            if subkey in self.db[key] and \
               type(self.db[key].get(subkey, False)) is list:
                self.db[key][subkey].append(value)
            else:
                # need to return proper messages
                return False
        else:
            if type(self.db.get(key, None)) is list:
                return self.db[key].append(value)
            else:
                # coz operation not permitted
                return False
        return False

    @wrap(loaddb, savedb)
    def delete(self, key=None, subkey=None):
        if subkey != None and self.db.get(key, None):
            if type(self.db[key]) is dict:
                return self.db[key].pop(key, False)
            elif type(self.db[key]) is list: 
                return self.db[key].pop(key, False)
            else:
                return False
        else:
            return self.db.pop(key, False)
  
    @wrap(loaddb, savedb)
    def listreset(self, key=None, subkey=None):
        return self.lcreate(key, subkey, force=True)

    @wrap(loaddb, savedb)
    def getfirst(self, key=None, subkey=None):
        out = self.db
        for dkey in sorted(out.keys(), reverse=True):
            if re.match(key, dkey):
                if subkey!= None and subkey in out[dkey]:
                    return out[dkey][subkey]
                else:
                    return out[dkey]
        return False

    @wrap(loaddb, savedb)
    def emptydb(self):
        self.db = {}
        return True

def runcli():
  print("Welcome to hashlite db shell")
