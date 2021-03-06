
__author__ = 'yunling'

from datetime import datetime, timedelta
import Util
import sys

class Market:
    """
    class for market data access
    """

    def __init__(self, trans, depth, stat_min, stat_hour, trend_index):
        self.trans = trans
        self.depth = depth
        self.stat_min = stat_min
        self.stat_hour = stat_hour
        self.trend_index = trend_index
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
        useful_price = min_price_data[-(W+1):-1]
        useful_meas = meas[-(W+1):-1]
        return Util.marketTrendIndex(useful_price, useful_meas)

    def getMarketTrendIndexInLastN(self, W):
        r = self.__2array(self.trend_index.find({'date': {
            "$lte": self.__now()
        }}).sort([("date", -1)]).limit(W))
        r.reverse()
        return r


if __name__ == '__main__':
    from pymongo import MongoClient
    from datetime import datetime
    from Market import Market
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    client = MongoClient("mongodb://115.28.4.59:27017")
    market = Market(client.trans.cnbtc, client.depths.cnbtc, client.trans_stat.cnbtc_min, client.trans_stat.cnbtc_hr, client.trans_stat.cnbtc_index)
    now = datetime.now()
    index_list = market.getMarketTrendIndexInLastN(60 * 24)
    index_480 = [x['index_480'] for x in index_list]
    index_240 = [x['index_240'] for x in index_list]
    index_120 = [x['index_120'] for x in index_list]
    index_60 = [x['index_60'] for x in index_list]
    t = [x['date'] for x in index_list]
    plt.figure(1, figsize=(15, 15))

    price_list = market.getMALastNMin(60 * 24, 10)

    plt.subplot(511)
    plt.plot(t, index_60, '-')
    plt.title("Market Trend with N = 60 min")
    plt.grid()

    plt.subplot(512)
    plt.plot(t, index_120, '-')
    plt.title("Market Trend with N = 120 min")
    plt.grid()

    plt.subplot(513)
    plt.plot(t, index_240, '-')
    plt.title("Market Trend with N = 240 min")
    plt.grid()

    plt.subplot(514)
    plt.plot(t, index_480, '-')
    plt.title("Market Trend with N = 480 min")
    plt.grid()

    plt.subplot(515)
    plt.plot(t, price_list, '-')
    plt.title("Market Price MA")
    plt.grid()

    plt.savefig(sys.argv[1])



if __name__ == '__old_main__':
    from pymongo import MongoClient
    from datetime import datetime
    from Market import Market
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    client = MongoClient("mongodb://115.28.4.59:27017")
    market = Market(client.trans.huobi, client.depths.huobi, client.trans_stat.huobi_min, client.trans_stat.huobi_hr, client.trans_stat.huobi_index)
    now = datetime.now()
    plt.figure(1, figsize=(15, 15))
    for i in range(1, 5):
        plt.subplot(410 + i)
        market.setNow(now)
        N = pow(2, i - 1) * 60
        M = 2 * 12 * 6
        ia = []
        t = []
        for i in range(0, M):
            market.setNow(now - timedelta(seconds=i * 60 * 5))
            t.append(now - timedelta(seconds=i * 60 * 5))
            index = market.getMarketTrendIndexWithWindow(N)
            ia.append(index)
        ia.reverse()
        t.reverse()
        plt.plot(t, ia, '-')
        plt.title("Market Trend with N = " + str(N) + " min")
        plt.grid()
    plt.savefig(sys.argv[1])