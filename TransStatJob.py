__author__ = 'chengye'

import TransJob


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


def getTransStatLastN(n, collection):
    return collection.find().sort([("from", -1), ("to", -1)]).limit(n)
