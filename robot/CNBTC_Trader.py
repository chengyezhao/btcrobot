__author__ = 'yunling'

import chbtc_api_python
from Balance import Balance
import sys, os
import logging
import Order
from pymongo import MongoClient


logging.basicConfig(filename = os.path.join(os.getcwd(), 'CNBTC_Trader.log'), level = logging.INFO)


class Trader:

    def __init__(self):
        self.api = chbtc_api_python.chbtc_api(chbtc_api_python.ACCESS_KEY, chbtc_api_python.SECRET_KEY)

    def getAccountBalance(self):
        result = self.api.query_account()
        if result.has_key('code'):
            logging.error("getAccountBalance, API return error code " + str(result['code']))
            return None
        balance = result['result']['balance']
        frozen = result['result']['frozen']
        b = Balance(balance['CNY']['amount'], frozen['CNY']['amount'],
                        balance['BTC']['amount'], frozen['BTC']['amount'])
        logging.info("Get balance: " + str(b.toJson()))
        return b

    def sendOrder(self, order):
        if order.type == 'buy':
            result = self.api.buyOrder(order.amount, order.price)
            if result['code'] == 1000:
                order.id = result['id']
            else:
                logging.error("sendOrder, API return error code " + str(result['code']))
                order.id = -1
        else:
            if order.type == 'sell':
                result = self.api.sellOrder(order.amount, order.price)
                if result['code'] == 1000:
                        order.id = result['id']
                else:
                    logging.error("sendOrder, API return error code " + str(result['code']))
                    order.id = -1
        return order

    def cancelOrderById(self, order):
        result = self.api.cancelOrder(order.id)
        if result['code'] == 1000:
            order.status = Order.CANCELLED
        return order

    def getRemoteOrder(self, order):
        result = self.api.getOrder(order.id)
        if result.has_key('code'):
            return None
        order.traded_amount = result['trade_amount']
        order.status = result['status']
        return order

    def getLatestOrders(self, order_type):
        orders = []
        if order_type == 'buy':
            result = self.api.getBuyOrders()
        else:
            result = self.api.getSellOrders()
        for ord in result:
            orders.append(Order.fromCNBTCOrder(ord))
        return orders



if __name__ == '__main__':
    client = MongoClient("mongodb://115.28.4.59:27017")
    col = client.order.cnbtc
    col2 = client.balance.cnbtc
    t = Trader()
    b = t.getAccountBalance()
    b.save(col2)
    print b.toJson()
    orders = t.getLatestOrders('buy')
    for o in orders:
        print o.toJson()
        #o.save(col)
    remote_order = t.getRemoteOrder(orders[0])
    print remote_order.toJson()
    #new_order = t.sendOrder(Order.Order(type='buy', amount=0.001, price=30))
    #print new_order.toJson()
