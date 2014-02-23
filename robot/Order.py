__author__ = 'yunling'


from datetime import datetime

WAITING = 0
CANCELLED = 1
COMPLETED = 2
PARR_COMPLETED = 3
TO_CANCEL = 5


class Order:

    def __init__(self, type, amount, price, id=None, status=WAITING, date=0, traded_amount=0):
        if date == 0:
            self.date = datetime.now()
        else:
            self.date = date
        self.id = id
        self.type = type
        self.amount = amount
        self.price = price
        self.status = status
        self.traded_amount = traded_amount

    def save(self, collection):
        return collection.save({
            '_id' : self.id,
            'date': self.date,
            'type': self.type,
            'amount': self.amount,
            'price': self.price,
            'status': self.status,
            'traded_amount': self.traded_amount
        })

    def toJson(self):
        return {
            'id' : self.id,
            'date': self.date,
            'type': self.type,
            'amount': self.amount,
            'price': self.price,
            'status': self.status,
            'traded_amount': self.traded_amount
        }

def fromCNBTCOrder( object):
    type = 'buy'
    if object['type'] == 0:
        type = 'sell'
    return Order(type, object['total_amount'], object['price'],
                object['id'], object['status'], datetime.fromtimestamp(int(object['trade_date'])/1000),
                object['trade_amount'])