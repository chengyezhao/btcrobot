__author__ = 'yunling'

from datetime import datetime


class Balance:

    def __init__(self, cny, cny_frozen, btc, btc_frozen):
        self.date = datetime.now()
        self.cny = cny
        self.cny_frozen = cny_frozen
        self.btc = btc
        self.btc_frozen = btc_frozen


    def update(self, cny, cny_frozen, btc, btc_frozen):
        self.date = datetime.now()
        self.cny = cny
        self.cny_frozen = cny_frozen
        self.btc = btc
        self.btc_frozen = btc_frozen

    def toJson(self):
        return {
            'date': self.date,
            'btc': self.btc,
            'btc_frozen': self.btc_frozen,
            'cny': self.cny,
            'cny_frozen': self.cny_frozen
        }