__author__ = 'chengye'

import pycurl
import cStringIO
import random
import json
import hashlib
from datetime import datetime, timedelta

URL_MTGOX = r"http://info.btc123.com/lib/jsonProxyEx.php?type=MtGoxTradesv2NODB&suffix="
URL_BTCCHINA = r"http://info.btc123.com/lib/jsonProxyEx.php?type=btctradeTrades&suffix="
URL_BTCE = r"http://i.btc123.com/lib/jsonProxyEx.php?type=btceBTCUSDtrades&suffix="
URL_OKCOIN = r"http://www.okcoin.com/api/trades.do?&suffix="
URL_OKCOIN_LTC = r"http://www.okcoin.com/api/trades.do?symbol=ltc_cny&suffix="
URL_FXBTC = r"http://data.fxbtc.com/api?op=query_last_trades&symbol=btc_cny&count=100&suffix="
URL_CNBTC = r"http://api.chbtc.com/data/trades?suffix="


def getTransFromUrl(url):
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
        return transJson
    except pycurl.error, error:
        return []


def insertTrans(trans, collection, symbol):
    n = 0
    if symbol == "fxbtccny" and trans['result'] == True:
        for tran in trans['datas']:
            new_trans = {
                '_id': tran['ticket'],
                'date': datetime.fromtimestamp(int(tran['date'])),
                'price': float(tran['rate']),
                'amount': float(tran['vol'])
            }
            #check whether transaction already it exits
            if not collection.find_one({"_id": new_trans['_id']}):
                collection.insert(new_trans)
                n += 1
    else:
        for tran in trans:
            new_trans = {
                '_id': hashlib.md5(symbol + str(tran['date']) + str(tran['amount']) + str(tran['price'])).hexdigest(),
                'date': datetime.fromtimestamp(int(tran['date'])),
                'price': float(tran['price']),
                'amount': float(tran['amount'])
            }
            #check whether transaction already it exits
            if not collection.find_one({"_id": new_trans['_id']}):
                collection.insert(new_trans)
                n += 1

    return n


def getTransByDate(from_ts, to_ts, collection):
    return collection.find({'date': {
        "$gte": from_ts,
        "$lt": to_ts
    }})


def getTransThisMin(collection):
    to_ts = datetime.now()
    from_ts = datetime(to_ts.year, to_ts.month, to_ts.day,
                       to_ts.hour, to_ts.minute, 0, 0)
    return getTransByDate(from_ts, to_ts, collection)


def getTransInLastNMin(collection, n=1):
    rt = datetime.now()
    to_ts = datetime(rt.year, rt.month, rt.day,
                     rt.hour, rt.minute, 0, 0)
    from_ts = to_ts - timedelta(seconds=n * 60)
    return getTransByDate(from_ts, to_ts, collection)


def getTransThisHour(collection):
    to_ts = datetime.now()
    from_ts = datetime(to_ts.year, to_ts.month, to_ts.day,
                       to_ts.hour, 0, 0, 0)
    return getTransByDate(from_ts, to_ts, collection)


def getTransInLastNHour(collection, n=1):
    rt = datetime.now()
    to_ts = datetime(rt.year, rt.month, rt.day,
                     rt.hour, 0, 0, 0)
    from_ts = to_ts - timedelta(seconds=n * 3600)
    return getTransByDate(from_ts, to_ts, collection)


def getTransInLastN(n, collection):
    return collection.find().sort([("date", -1)]).limit(n)
