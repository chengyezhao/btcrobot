__author__ = 'chengye'

import TransJob
import Util as Util
from datetime import datetime
from pymongo import MongoClient

def calculateBasicTransStat(from_ts, to_ts, trans):
    total_volume = 0
    max_price = 0
    min_price = 100000
    end_price = 0
    start_price = 0

    i = 0

    for tran in trans:
        if i == 0:
            start_price = tran['price']
        total_volume += tran['amount']
        max_price = max(max_price, tran['price'])
        min_price = min(min_price, tran['price'])
        end_price = tran['price']
        i += 1

    obj = {
        'from': from_ts,
        'to': to_ts,
        'volume': total_volume,
        'max':  max_price,
        'min':  min_price,
        'start':  start_price,
        'end':  end_price
    }
    return obj




def createTransStat(from_ts, to_ts, func, from_collection, to_collection):
    trans = TransJob.getTransByDate(from_ts, to_ts, from_collection)
    stat = func(from_ts, to_ts, trans)
    e = to_collection.find_one({"from": from_ts, "to": to_ts})
    if not e:
        to_collection.insert(stat)
    else:
        stat["_id"] = e["_id"]
        return to_collection.save(stat)


def __2array(cursor):
    result = []
    for i in cursor:
        result.append(i)
    return result

def getTransStatLastN(n, collection):
    return collection.find().sort([("from", -1), ("to", -1)]).limit(n)

def getLastNMinStat(N, collection):
    r = __2array(collection.find({'from': {"$lte": datetime.now()}}).sort([("from", -1)]).limit(N))
    r.reverse()
    return r


def getMarketTrendIndexWithWindow(collection, W):
    raw_min_data = getLastNMinStat(W * 2, collection)
    min_price_data = Util.nozeros([x['end'] for x in raw_min_data])
    meas = Util.moving_average(min_price_data, W)
    useful_price = min_price_data[-(W+1):-1]
    useful_meas = meas[-(W+1):-1]
    return Util.marketTrendIndex(useful_price, useful_meas)


def insertMarketIndex(from_collection, to_collection):
    index_60 = getMarketTrendIndexWithWindow(from_collection, 60)
    index_120 = getMarketTrendIndexWithWindow(from_collection, 120)
    index_240 = getMarketTrendIndexWithWindow(from_collection, 240)
    index_480 = getMarketTrendIndexWithWindow(from_collection, 480)
    obj = {
        'date': datetime.now(),
        'index_60': index_60,
        'index_120': index_120,
        'index_240':  index_240,
        'index_480': index_480
    }
    to_collection.insert(obj)


if __name__ == '__main__':
    client = MongoClient("mongodb://115.28.4.59:27017")
    db1 = client.trans
    db2 = client.trans_stat
    insertMarketIndex(db2.btcchinabtccny_min, db2.btcchinabtccny_index)
