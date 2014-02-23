__author__ = 'yunling'

import datetime
import numpy as np
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from Market import Market
import Util
from pymongo import MongoClient


##get data
N = 60*200
M = 24*20
client = MongoClient("mongodb://115.28.4.59:27017")
market = Market(client.trans.cnbtc, client.depths.cnbtc, client.trans_stat.cnbtc_min, client.trans_stat.cnbtc_hr)
market.setNow(datetime.datetime(2014, 2, 1, 0, 0, 0, 0))
raw_min_data = market.getLastNMinStat(N)
raw_hr_data = market.getLastNHourStat(M)
min_date = [x['from'] for x in raw_min_data]
min_price_data = Util.nozeros([x['end'] for x in raw_min_data])
min_vol_data = [x['volume'] for x in raw_min_data]
hr_date = [x['from'] for x in raw_hr_data]
hr_price_data = Util.nozeros([ x['end'] for x in raw_hr_data])
hr_vol_data = [x['volume'] for x in raw_hr_data]

min_ma20_data = Util.moving_average(min_price_data, 20)
min_ma60_data = Util.moving_average(min_price_data, 60)
min_ma120_data = Util.moving_average(min_price_data, 120)

hr_ma20_data = Util.moving_average(hr_price_data, 20)
hr_ma60_data = Util.moving_average(hr_price_data, 60)

#min price figure
plt.figure(1, figsize=(12,6))
plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

#price
plt.sca(ax1)
plt.plot(min_date, min_price_data, color="blue", lw=1)
plt.plot(min_date, min_ma20_data, color="green", lw=2, label="EMA(20)")
plt.plot(min_date, min_ma60_data, color="black", lw=2, label="EMA(60)")
plt.plot(min_date, min_ma120_data, color="red", lw=2, label="EMA(120)")

plt.ylabel("BTC/RMB")
plt.title("BTC price & volume/min")
plt.legend(loc='lower center', shadow=True, fancybox=True)
plt.ylim(min(min_price_data), max(min_price_data))

#volume
plt.sca(ax2)
plt.fill(min_date, min_vol_data, color="red")
plt.ylabel("Volume")
plt.ylim(0, max(min_vol_data))

#hour data
plt.figure(2, figsize=(12,6))
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

#price
plt.sca(ax1)
plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
plt.plot(hr_date, hr_price_data, color="blue", lw=1)
plt.plot(hr_date, hr_ma20_data, color="green", lw=2, label="EMA(20)")
plt.plot(hr_date, hr_ma60_data, color="black", lw=2, label="EMA(60)")

plt.ylabel("BTC/RMB")
plt.title("BTC price & volume/Hour")
plt.legend(loc='lower center', shadow=True, fancybox=True)
plt.ylim(min(hr_price_data), max(hr_price_data))

#volume
plt.sca(ax2)
plt.fill(hr_date, hr_vol_data, color="red")
plt.ylabel("Volume")
plt.ylim(0, max(hr_vol_data))

plt.show()





