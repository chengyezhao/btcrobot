__author__ = 'chengye'

from TransJob import insertTrans, getTransFromUrl
import TransJob
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

def MTGOXJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_MTGOX), db.mtgoxbtcusd, "mtgoxbtcusd")
    logging.info("MTGOXJob " + ", new transaction: " + str(n))

def BTCCHINAJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_BTCCHINA), db.btcchinabtccny, "btcchinabtccny")
    logging.info( "BTCCHINAJob " +  ", new transaction: " + str(n))


def BTECJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_BTCE), db.btcebtcusd, "btcebtcusd")
    logging.info( "`BTECJob " +  ", new transaction: " + str(n))

def OKCOINJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_OKCOIN), db.okcoinbtccny, "okcoinbtccny")
    logging.info( "OKCOINJob " +  ", new transaction: " + str(n))

def OKCOINLTCJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_OKCOIN_LTC), db.okcoinltccny, "okcoinltccny")
    logging.info( "OKCOINLTCJob " +  ", new transaction: " + str(n))


schedule.every(5).seconds.do(MTGOXJob)
time.sleep(1)
schedule.every(5).seconds.do(BTCCHINAJob)
time.sleep(1)
schedule.every(5).seconds.do(BTECJob)
time.sleep(1)
schedule.every(5).seconds.do(OKCOINJob)
time.sleep(1)
schedule.every(5).seconds.do(OKCOINLTCJob)
time.sleep(1)


while True:
    schedule.run_pending()
    time.sleep(1)