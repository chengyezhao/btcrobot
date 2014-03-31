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

    def __eq__(self, other):
        return self.cny == other.cny and self.btc == other.btc and self.cny_frozen == other.cny_frozen and self.btc_frozen == other.btc_frozen