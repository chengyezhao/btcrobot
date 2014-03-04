__author__ = 'yunling'

class SimpleStrategy:

    def __int__(self, market, mea_window, min_price_delta):
        self.market = market
        self.mea_window = mea_window
        self.min_price_delta = min_price_delta

    def getBuyConfident(self):
        pass

    def getSellConfident(self):
        return 1 - self.getBuyConfident()

