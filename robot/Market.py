__author__ = 'yunling'

from datetime import datetime, timedelta


class Market:
    """
    class for market data access
    """

    def __init__(self, trans, depth, stat_min, stat_hour):
        self.trans = trans
        self.depth = depth
        self.stat_min = stat_min
        self.stat_hour = stat_hour

    def __2array(self, cursor):
        result = []
        for i in cursor:
            result.append(i)
        return result


    ##  methods to get Transaction level information
    def getTransByDate(self, from_ts, to_ts):
        return self.__2array(self.trans.find({'date': {
            "$gte": from_ts,
            "$lt": to_ts
        }}))

    def getTransInThisMin(self):
        to_ts = datetime.now()
        from_ts = datetime(to_ts.year, to_ts.month, to_ts.day,
                           to_ts.hour, to_ts.minute, 0, 0)
        return self.getTransByDate(from_ts, to_ts)

    def getTransInLastNMin(self, n=1):
        rt = datetime.now()
        to_ts = datetime(rt.year, rt.month, rt.day,
                         rt.hour, rt.minute, 0, 0)
        from_ts = to_ts - timedelta(seconds=n * 60)
        return self.getTransByDate(from_ts, to_ts)

    def getTransInThisHour(self):
        to_ts = datetime.now()
        from_ts = datetime(to_ts.year, to_ts.month, to_ts.day,
                           to_ts.hour, 0, 0, 0)
        return self.getTransByDate(from_ts, to_ts)

    def getTransInLastNHour(self, n=1):
        rt = datetime.now()
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
        return self.__2array(self.depth.find({},{"date":1, "asks": {"$slice": -N}, "bids":{"$slice": N}}).sort([("date", -1)]).limit(1))[0]

    def getTopDepth(self):
        result = self.getTopNDepth(1)
        result['asks'] = result['asks'][0]
        result['bids'] = result['bids'][0]
        return result

    ## method to get market statistics
    def getLastNMinStat(self, N):
        r =  self.__2array(self.stat_min.find().sort([("from", -1)]).limit(N))
        r.reverse()
        return r

    def getLastNHourStat(self, N):
        r = self.__2array(self.stat_hour.find().sort([("from",-1)]).limit(N))
        r.reverse()
        return r

    def getMinStatByDate(self, from_ts, to_ts):
        pass

    def getHourStatByDate(self, from_ts, to_ts):
        pass