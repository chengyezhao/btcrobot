__author__ = 'yunling'
import time
import logging
import Order

logging.basicConfig(filename = os.path.join(os.getcwd(), 'SimpleRobot.log'), level = logging.INFO)


SLEEP_TIME = 10
SLICE_CNY_AMOUNT = 500
SLICE_BTC_AMOUNT = 0.1


class SimpleRobot:

    def __init__(self, market, trader, strategy):
        self.market = market
        self.trader = trader
        self.strategy = strategy

    def run(self):

        while True:

            #得到并保存当前的账户详细
            balance = self.trader.getAccountBalance()
            self.trader.saveBalance(balance)

            #确定是否买入
            buyConfident = self.strategy.getBuyConfident(self.market)
            logging.info("BuyConfident = " + str(buyConfident))
            if buyConfident > 0.5:
                self.clearSellOrder()
                self.buy(SLICE_CNY_AMOUNT)

            #确定是否卖出
            sellConfident = self.strategy.getSellConfident(self.market)
            logging.info("SellConfident = " + str(sellConfident))
            if sellConfident > 0.5:
                self.clearBuyOrder()
                self.sell(SLICE_BTC_AMOUNT)

            time.sleep(SLEEP_TIME)

    def buy(self, total_amount):

        slice_amount = SLICE_CNY_AMOUNT
        if total_amount < slice_amount:
            slice_amount = total_amount

        while total_amount > 0:

            #构建一笔交易
            topDepth = self.market.getTopDepth()
            orderPrice = topDepth['asks']
            new_order = self.trader.sendOrder(Order.Order(type="buy", amount=slice_amount/orderPrice, price=orderPrice))
            self.trader.saveOrder(new_order)
            logging.info("New order : " + new_order.toJson())

            #交易是否成功发送
            if new_order.id == -1:
                continue

            #等待交易成功
            while True:
                remote_order = self.trader.getRemoteOrder(new_order)
                self.trader.saveOrder(remote_order)
                if remote_order is not None:
                    remote_order.save(self.orderCollection)
                    if remote_order.status == Order.PARR_COMPLETED or remote_order.status == Order.COMPLETED:
                        break
                time.sleep(1)

            total_amount = total_amount - slice_amount

    def sell(self, total_amount):
        slice_amount = SLICE_BTC_AMOUNT
        if total_amount < slice_amount:
            slice_amount = total_amount

        while total_amount > 0:

            #构建一笔交易
            topDepth = self.market.getTopDepth()
            orderPrice = topDepth['bids']
            new_order = self.trader.sendOrder(Order.Order(type="sell", amount=slice_amount, price=orderPrice))
            self.trader.saveOrder(new_order)
            logging.info("New order : " + new_order.toJson())

            #交易是否成功发送
            if new_order.id == -1:
                continue

            #等待交易成功
            while True:
                remote_order = self.trader.getRemoteOrder(new_order)
                if remote_order is not None:
                    self.trader.saveOrder(remote_order)
                    if remote_order.status == Order.PARR_COMPLETED or remote_order.status == Order.COMPLETED:
                        break
                time.sleep(1)

            total_amount = total_amount - slice_amount