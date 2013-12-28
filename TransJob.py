__author__ = 'chengye'


import pycurl
import cStringIO
import random
import json
import hashlib
from pymongo import MongoClient
from datetime import datetime

URL_MTGOX = r"http://info.btc123.com/lib/jsonProxyEx.php?type=MtGoxTradesv2NODB&suffix="
URL_BTCCHINA = r"http://info.btc123.com/lib/jsonProxyEx.php?type=btctradeTrades&suffix="
URL_BTCE = r"http://i.btc123.com/lib/jsonProxyEx.php?type=btceBTCUSDtrades&suffix="
URL_OKCOIN = r"http://www.okcoin.com/api/trades.do"
URL_OKCOIN_LTC = r"http://www.okcoin.com/api/trades.do?symbol=ltc_cny"

def getTransFromUrl(url):
    #get json docuemnt from url
    url = url + str(random.random())
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    #print buf.getvalue()
    decode = json.JSONDecoder()
    transJson = decode.decode(buf.getvalue())
    buf.close()
    return transJson

def insertTrans(trans, collection, symbol):
    n = 0
    for tran in trans:
        new_trans = {}
        new_trans['_id'] = hashlib.md5(symbol + str(tran['date']) + str(tran['amount']) + str(tran['price'])).hexdigest()
        new_trans['date'] = int(tran['date'])
        new_trans['price'] = float(tran['price'])
        new_trans['amount'] = float(tran['amount'])
        #check whether transaction already it exits
        if(not collection.find_one({"_id": new_trans['_id']})):
            collection.insert(new_trans)
            n = n + 1

    return n
