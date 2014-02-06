__author__ = 'yunling'


import pycurl
import cStringIO
import random
import json
import hashlib
from datetime import datetime, timedelta

URL_CNBTC = r"http://api.chbtc.com/data/depth?suffix="


def getDepthFromUrl(url):
    url += str(random.random())
    buf = cStringIO.StringIO()
    try:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.TIMEOUT, 5)
        c.setopt(c.CONNECTTIMEOUT, 8)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        decode = json.JSONDecoder()
        transJson = decode.decode(buf.getvalue())
        buf.close()
        if 'bids' in transJson and 'asks' in transJson:
            return transJson
        return False
    except pycurl.error, error:
        return False



def insertDepth(depths, collection):
    if not depths:
        return False
    new_depth = {
        '_id' : hashlib.md5(str(depths)).hexdigest(),
        'date': datetime.now(),
        'asks': depths['asks'],
        'bids': depths['bids'],
        'life': 0
    }
    if not collection.find_one({"_id": new_depth['_id']}):
        collection.insert(new_depth)
        return True
    else:
        collection.update({"_id": new_depth['_id']}, {"$inc": {"life": 1}})
        return False