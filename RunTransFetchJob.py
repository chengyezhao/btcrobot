__author__ = 'chengye'

from TransJob import insertTrans, getTransFromUrl
import TransJob
import time
from datetime import datetime
from pymongo import MongoClient
import sys
import schedule

print sys.argv[1]
client = MongoClient(sys.argv[1])
db = client.trans

def MTGOXJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_MTGOX), db.mtgoxbtcusd, "mtgoxbtcusd")
    print "====MTGOXJob " + str(datetime.now()) + ", new transaction: " + str(n)

def BTCCHINAJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_BTCCHINA), db.btcchinabtccny, "btcchinabtccny")
    print "====BTCCHINAJob " + str(datetime.now()) + ", new transaction: " + str(n)


def BTECJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_BTCE), db.btcebtcusd, "btcebtcusd")
    print "====BTECJob " + str(datetime.now()) + ", new transaction: " + str(n)

def OKCOINJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_OKCOIN), db.okcoinbtccny, "okcoinbtccny")
    print "====OKCOINJob " + str(datetime.now()) + ", new transaction: " + str(n)

def OKCOINLTCJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_OKCOIN_LTC), db.okcoinltccny, "okcoinltccny")
    print "====OKCOINLTCJob " + str(datetime.now()) + ", new transaction: " + str(n)


schedule.every(5).seconds.do(MTGOXJob)
time.sleep(1)
schedule.every(5).seconds.do(BTCCHINAJob)
time.sleep(1)
schedule.every(5).seconds.do(BTECJob)
time.sleep(1)
schedule.every(5).seconds.do(OKCOINJob)
time.sleep(1)
schedule.every(5).seconds.do(OKCOINLTCJob)



while True:
    schedule.run_pending()
    time.sleep(1)