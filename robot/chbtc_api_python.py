import json, urllib2, hashlib, struct, sha, time, sys


ACCESS_KEY = '94fd85b7-a381-4e3a-ab57-a66daf7cb0a5'
SECRET_KEY = '05fe699a-d2cb-4e0d-ac59-9034de1275f8'

class chbtc_api:

    def __init__(self, mykey, mysecret):
        self.mykey = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb = struct.pack("%ds" % len(aKey), aKey)
        value = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value = struct.pack("%ds" % len(aValue), aValue)
        #print value
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params=''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time() * 1000)
            params += '&sign=%s&reqTime=%d' % (sign, reqTime)
            url = 'https://trade.chbtc.com/api/' + path + '?' + params
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception, ex:
            print >> sys.stderr, 'chbtc request ex: ', ex
            return None

    def query_account(self):
        params = "method=getAccountInfo&accesskey=" + self.mykey
        path = 'getAccountInfo'
        return self.__api_call(path, params)

    def buyOrder(self, amount, price, symbol='btc'):
        params = "method=order&accesskey=" + self.mykey + "&price=" + str(price)\
                 + "&amount=" + str(amount) + "&tradeType=1&currency=" + symbol
        path = 'order'
        return self.__api_call(path, params)

    def sellOrder(self, amount, price, symbol='btc'):
        params = "method=order&accesskey=" + self.mykey + "&price=" + str(price) \
                 + "&amount=" + amount + "&tradeType=0&currency=" + symbol
        path = 'order'
        return self.__api_call(path, params)

    def cancelOrder(self, order_id, symbol='btc'):
        params = "method=cancelOrder&accesskey=" + self.mykey + "&id=" + str(order_id) + "&currency=" + symbol
        path = 'cancelOrder'
        return self.__api_call(path, params)

    def getOrder(self, order_id, symbol='btc'):
        params = "method=getOrder&accesskey=" + self.mykey + "&id=" + str(order_id) + "&currency=" + symbol
        path = 'getOrder'
        return self.__api_call(path, params)

    def getBuyOrders(self, symbol='btc', page=1):
        params = "method=getOrders&accesskey=" + self.mykey + "&tradeType=1&currency=" + symbol + "&pageIndex=" + str(page)
        path = 'getOrders'
        return self.__api_call(path, params)

    def getSellOrders(self, symbol='btc', page=1):
        params = "method=getOrders&accesskey=" + self.mykey + "&tradeType=0&currency=" + symbol + "&pageIndex=" + str(page)
        path = 'getOrders'
        return self.__api_call(path, params)

if __name__ == '__main__':
    api = chbtc_api(ACCESS_KEY, SECRET_KEY)
    print api.query_account()
    #buy_result = api.buyOrder(0.001, 30)
    #print buy_result
    print api.getOrder(2014021232149695)
    print api.getBuyOrders()
    print api.getSellOrders()
    print api.cancelOrder(201402232149695)