__author__ = 'chengye'

import TransStatJob
from datetime import datetime, timedelta
from pymongo import MongoClient
import sys
import logging
import os

logging.basicConfig(filename=os.path.join(os.getcwd(), 'RunTransStatHourJob.log'), level=logging.INFO)

logging.info("Connect to mongodb at " + sys.argv[1])
client = MongoClient(sys.argv[1])
db1 = client.trans
db2 = client.trans_stat

N = sys.argv[2]

#run by min, try to get trans in last 5 minutes, and calculated stat if not
rt = datetime.now()
collections = [
    (db1.mtgoxbtcusd, db2.mtgoxbtcusd_hr),
    (db1.btcchinabtccny, db2.btcchinabtccny_hr),
    (db1.btcebtcusd, db2.btcebtcusd_hr),
    #(db1.okcoinbtccny, db2.okcoinbtccny_hr),
    #(db1.okcoinltccny, db2.okcoinltccny_hr),
    #(db1.fxbtccny, db2.fxbtccny_hr),
    (db1.cnbtc, db2.cnbtc_hr)
]

for n in range(0, int(N)):
    to_ts = datetime(rt.year, rt.month, rt.day, rt.hour, 0, 0, 0) - timedelta(seconds=n * 3600)
    from_ts = to_ts - timedelta(seconds=3600)
    logging.info("Hour stat calculate from " + str(from_ts) + " to " + str(to_ts))
    for col in collections:
        TransStatJob.createTransStat(from_ts, to_ts, TransStatJob.calculateBasicTransStat, col[0], col[1])