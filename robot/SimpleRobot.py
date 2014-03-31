
__author__ = 'yunling'
import time
import logging
import Order
import sys, os
from Balance import Balance


logging.basicConfig(filename = os.path.join(os.getcwd(), 'SimpleRobot.log'), level = logging.INFO)


SLEEP_TIME = 30  #seconds
SLICE_CNY_AMOUNT = 200
SLICE_BTC_AMOUNT = 0.05
ORDER_WAIT_TIME = 60 #seconds

class SimpleRobot:

    def __init__(self, market, trader, strategy):
        self.market = market
        self.trader = trader
        self.strategy = strategy

    def run(self):

        balance = Balance(0,0,0,0)

        while True:

            try:

                new_balance = self.trader.getAccountBalance()
                if balance != new_balance:
                    self.trader.saveBalance(new_balance)
                    balance = new_balance

                buyConfident = self.strategy.getBuyConfident()
                logging.info("BuyConfident = " + str(buyConfident))

                if buyConfident > 0.8:
                    buyAmount = SLICE_CNY_AMOUNT
                    if balance.cny > SLICE_CNY_AMOUNT:
                        self.clearSellOrder()
                        self.buy(buyAmount)
                elif buyConfident < 0.3:
                    sellAmount = SLICE_BTC_AMOUNT
                    if balance.btc > SLICE_BTC_AMOUNT:
                        self.clearBuyOrder()
                        self.sell(sellAmount)
                else:
                    self.clearSellOrder()
                    self.clearBuyOrder()
            except:
                pass

            time.sleep(SLEEP_TIME)

    def clearSellOrder(self):
        pass

    def clearBuyOrder(self):
        pass

    def buy(self, total_amount):

        topDepth = self.market.getTopDepth()
        orderPrice = topDepth['asks'][0]
        new_order = self.trader.sendOrder(Order.Order(type="buy", amount=total_amount / orderPrice, price=orderPrice))
        self.trader.saveOrder(new_order)
        logging.info("New order : " + str(new_order.toJson()))

        if new_order.id == -1:
            logging.info("Buy Order failed")
            return

        i = 0
        while i < ORDER_WAIT_TIME:
            remote_order = self.trader.getRemoteOrder(new_order)
            self.trader.saveOrder(remote_order)
            if remote_order is not None:
                remote_order.save(self.orderCollection)
                if remote_order.status == Order.PARR_COMPLETED or remote_order.status == Order.COMPLETED:
                    logging.info("Buy Order success")
                    return
            time.sleep(1)
            i += 1


        logging.info("Buy Order timeout")
        self.trader.cancelOrderById(new_order.id)

    def sell(self, total_amount):

        topDepth = self.market.getTopDepth()
        orderPrice = topDepth['bids'][0]
        new_order = self.trader.sendOrder(Order.Order(type="sell", amount=total_amount, price=orderPrice))
        self.trader.saveOrder(new_order)
        logging.info("New order : " + str(new_order.toJson()))

        if new_order.id == -1:
            logging.info("Sell Order failed")
            return

        i = 0
        while i < ORDER_WAIT_TIME:
            remote_order = self.trader.getRemoteOrder(new_order)
            if remote_order is not None:
                self.trader.saveOrder(remote_order)
                if remote_order.status == Order.PARR_COMPLETED or remote_order.status == Order.COMPLETED:
                    logging.info("Sell Order success")
                    return
            time.sleep(1)
            i += 1


        logging.info("Sell Order timeout")
        self.trader.cancelOrderById(new_order.id)

if __name__ == '__main__':
    from SimpleRobot import SimpleRobot
    from pymongo import MongoClient
    from CNBTC_Trader import Trader
    from SimpleStrategy import SimpleStrategy
    from Market import Market
    client = MongoClient("mongodb://115.28.4.59:27017")
    market = Market(client.trans.cnbtc, client.depths.cnbtc, client.trans_stat.cnbtc_min,
                    client.trans_stat.cnbtc_hr, client.trans_stat.cnbtc_index)
    trader = Trader(client.order.cnbtc, client.balance.cnbtc)
    strategy = SimpleStrategy(market)
    robot = SimpleRobot(market, trader, strategy)
    robot.run()

