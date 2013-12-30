__author__ = 'chengye'

import TransJob


def calculateBasicTansStat(from_ts, to_ts, trans):
    total_volume = 0
    max_price = 0
    min_price = 100000
    start_price = trans[0]['price']
    end_price = trans[-1]['price']

    for tran in trans:
        total_volume += trans['amount']
        max_price = max(max_price, tran['price'])
        min_price = min(min_price, tran['price'])

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


def createTransStat(from_ts, to_ts, func, collection):
    if not collection.find_one({"from": from_ts, "to": to_ts}):
        trans = TransJob.getTransByDate(from_ts, to_ts)
        stat = func(from_ts, to_ts, trans)
        collection.insert(stat)
    else:
        return collection.find_one({"from": from_ts, "to": to_ts})

def getTransStatLastN(n, collection):
    return collection.find().sort([("from", -1), ("to", -1)]).limit(n)