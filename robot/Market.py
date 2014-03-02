__author__ = 'yunling'

from datetime import datetime, timedelta
import Util


class Market:
    """
    class for market data access
    """

    def __init__(self, trans, depth, stat_min, stat_hour):
        self.trans = trans
        self.depth = depth
        self.stat_min = stat_min
        self.stat_hour = stat_hour
        self.now = False

    def __2array(self, cursor):
        result = []
        for i in cursor:
            result.append(i)
        return result

    def __now(self):
        if not self.now:
            return datetime.now()
        else:
            return self.now

    def setNow(self, t):
        self.now = t

    ##  methods to get Transaction level information
    def getTransByDate(self, from_ts, to_ts):
        return self.__2array(self.trans.find({'date': {
            "$gte": from_ts,
            "$lt": to_ts
        }}))

    def getTransInThisMin(self):
        to_ts = self.__now()
        from_ts = datetime(to_ts.year, to_ts.month, to_ts.day,
                           to_ts.hour, to_ts.minute, 0, 0)
        return self.getTransByDate(from_ts, to_ts)

    def getTransInLastNMin(self, n=1):
        rt = self.__now()
        to_ts = datetime(rt.year, rt.month, rt.day,
                         rt.hour, rt.minute, 0, 0)
        from_ts = to_ts - timedelta(seconds=n * 60)
        return self.getTransByDate(from_ts, to_ts)

    def getTransInThisHour(self):
        to_ts = self.__now()
        from_ts = datetime(to_ts.year, to_ts.month, to_ts.day,
                           to_ts.hour, 0, 0, 0)
        return self.getTransByDate(from_ts, to_ts)

    def getTransInLastNHour(self, n=1):
        rt = self.__now()
        to_ts = datetime(rt.year, rt.month, rt.day,
                         rt.hour, 0, 0, 0)
        from_ts = to_ts - timedelta(seconds=n * 3600)
        return self.getTransByDate(from_ts, to_ts)

    def getLastNTrans(self, n):
        r = self.__2array(self.trans.find().sort([("date", -1)]).limit(n))
        r.reverse()
        return r

    ##  methods to get latest market depth information
    def getFullDepth(self):
        return self.__2array(self.depth.find().sort([("date", -1)]).limit(1))[0]

    def getTopNDepth(self, N):
        return self.__2array(self.depth.find({}, {"date":1, "asks": {"$slice": -N}, "bids":{"$slice": N}}).sort([("date", -1)]).limit(1))[0]

    def getTopDepth(self):
        result = self.getTopNDepth(1)
        result['asks'] = result['asks'][0]
        result['bids'] = result['bids'][0]
        return result

    ## method to get market statistics
    def getLastNMinStat(self, N):
        r = self.__2array(self.stat_min.find({'from': {
            "$lte": self.__now()
        }}).sort([("from", -1)]).limit(N))
        r.reverse()
        return r

    def getLastNHourStat(self, N):
        r = self.__2array(self.stat_hour.find({'from': {
            "$lte": self.__now()
        }}).sort([("from", -1)]).limit(N))
        r.reverse()
        return r

    def getMALastNMin(self, N, W):
        raw = self.getLastNMinStat(N)
        close_price = Util.nozeros([x['end'] for x in raw])
        return Util.moving_average(close_price, W)

    def getMALastNHour(self, N, W):
        raw = self.getLastNHourStat(N)
        close_price = Util.nozeros([x['end'] for x in raw])
        return Util.moving_average(close_price, W)

    def getMarketTrendIndexWithWindow(self, W):
        raw_min_data = self.getLastNMinStat(W * 2)
        min_price_data = Util.nozeros([x['end'] for x in raw_min_data])
        meas = Util.moving_average(min_price_data, W)
        useful_price = min_price_data[-(N+1):-1]
        useful_meas = meas[-(N+1):-1]
        return Util.marketTrendIndex(useful_price, useful_meas)


if __name__ == '__main__':
    from pymongo import MongoClient
    import matplotlib.pyplot as plt
    client = MongoClient("mongodb://115.28.4.59:27017")
    market = Market(client.trans.cnbtc, client.depths.cnbtc, client.trans_stat.cnbtc_min, client.trans_stat.cnbtc_hr)
    now = datetime.now()
    market.setNow(now)
    N = 5 * 60
    M = 1 * 24 * 12
    ia = []
    t = []
    for i in range(0, M):
        market.setNow(now - timedelta(seconds=i * 60 * 5))
        t.append(now - timedelta(seconds=i * 60 * 5))
        index = market.getMarketTrendIndexWithWindow(N)
        ia.append(index)
    ia.reverse()
    t.reverse()
    plt.plot(t, ia, '-o')
    plt.grid()
    plt.show()