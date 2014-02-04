__author__ = 'chengye'

from TransJob import insertTrans, getTransFromUrl
from DepthJob import insertDepth, getDepthFromUrl
import TransJob
import DepthJob
import time
from pymongo import MongoClient
import sys
import schedule
import logging
import os

logging.basicConfig(filename = os.path.join(os.getcwd(), 'RunTransFetchJob.log'), level = logging.INFO)

logging.info("Connect to mongodb at " + sys.argv[1])
client = MongoClient(sys.argv[1])
db = client.trans
db2 = client.depths

def MTGOXJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_MTGOX), db.mtgoxbtcusd, "mtgoxbtcusd")
    logging.info("MTGOXJob " + ", new transaction: " + str(n))

def BTCCHINAJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_BTCCHINA), db.btcchinabtccny, "btcchinabtccny")
    logging.info("BTCCHINAJob " + ", new transaction: " + str(n))


def BTECJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_BTCE), db.btcebtcusd, "btcebtcusd")
    logging.info("BTECJob " + ", new transaction: " + str(n))

def OKCOINJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_OKCOIN), db.okcoinbtccny, "okcoinbtccny")
    logging.info("OKCOINJob " + ", new transaction: " + str(n))

def OKCOINLTCJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_OKCOIN_LTC), db.okcoinltccny, "okcoinltccny")
    logging.info("OKCOINLTCJob " + ", new transaction: " + str(n))

def FXBTCJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_FXBTC), db.fxbtccny, "fxbtccny")
    logging.info("FXBTCJob " + ", new transaction: " + str(n))

def CNBTCJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_CNBTC), db.cnbtc, "cnbtc")
    logging.info("CNBTC " + ", new transaction: " + str(n))

def CNBTC_DEPTH_JOB():
    f = insertDepth(getDepthFromUrl(DepthJob.URL_CNBTC), db2.cnbtc)
    if f:
        logging.info("CNBTC " + ", new depth get")


schedule.every(5).seconds.do(MTGOXJob)
time.sleep(1)
schedule.every(5).seconds.do(BTCCHINAJob)
time.sleep(1)
schedule.every(5).seconds.do(BTECJob)
time.sleep(1)
schedule.every(5).seconds.do(CNBTCJob)
time.sleep(1)
schedule.every(1).seconds.do(CNBTC_DEPTH_JOB)


while True:
    schedule.run_pending()
    time.sleep(1)