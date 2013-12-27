__author__ = 'chengye'

from TransJob import insertTrans, getTransFromUrl
import TransJob
import time
from datetime import datetime
from pymongo import MongoClient
import schedule

client = MongoClient('mongodb://115.28.4.59:27017/')
db = client.trans

def MTGOXJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_MTGOX), db.mtgoxbtcusd, "mtgoxbtcusd")
    print "====MTGOXJob " + str(datetime.now()) + ", new transaction: " + str(n)

def BTCCHINAJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_MTGOX), db.btcchinabtccny, "btcchinabtccny")
    print "====BTCCHINAJob " + str(datetime.now()) + ", new transaction: " + str(n)


def BTECJob():
    n = insertTrans(getTransFromUrl(TransJob.URL_BTCE), db.btcebtcusd, "btcebtcusd")
    print "====BTECJob " + str(datetime.now()) + ", new transaction: " + str(n)


schedule.every(10).seconds.do(MTGOXJob)
time.sleep(1)
schedule.every(10).seconds.do(BTCCHINAJob)
time.sleep(1)
schedule.every(10).seconds.do(BTECJob)


while True:
    schedule.run_pending()
    time.sleep(1)