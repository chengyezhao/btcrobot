__author__ = 'yunling'

import datetime
import numpy as np
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

from Market import Market
import Util
from pymongo import MongoClient


##get data
N = 60*20
M = 24*10
client = MongoClient("mongodb://115.28.4.59:27017")
market = Market(client.trans.mtgoxbtcusd, client.depths.mtgoxbtcusd, client.trans_stat.cnbtc_min, client.trans_stat.cnbtc_hr)
raw_min_data = market.getLastNMinStat(N)
raw_hr_data = market.getLastNHourStat(M)
min_price_data = Util.nozeros([x['end'] for x in raw_min_data])
min_vol_data = [x['volume'] for x in raw_min_data]
hr_price_data = Util.nozeros([ x['end'] for x in raw_hr_data])
hr_vol_data = [x['volume'] for x in raw_hr_data]

min_ma20_data = Util.moving_average(min_price_data, 20)
min_ma60_data = Util.moving_average(min_price_data, 60)
min_ma120_data = Util.moving_average(min_price_data, 120)

hr_ma20_data = Util.moving_average(hr_price_data, 20)
hr_ma60_data = Util.moving_average(hr_price_data, 60)

#min price figure
plt.figure(1)
plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

#price
plt.sca(ax1)
plt.plot(min_price_data, color="blue", lw=1)
plt.plot(min_ma20_data, color="green", lw=2, label="EMA(20)")
plt.plot(min_ma60_data, color="black", lw=2, label="EMA(60)")
plt.plot(min_ma120_data, color="red", lw=2, label="EMA(120)")

plt.xlabel("date")
plt.ylabel("price")
plt.title("Min data")
plt.legend(loc='lower center', shadow=True, fancybox=True)
plt.axis([0, N, min(min_price_data), max(min_price_data)])

#volume
plt.sca(ax2)
plt.fill(min_vol_data, color="red")
plt.xlabel("date")
plt.ylabel("volume")
plt.axis([0, N, 0, max(min_vol_data)])

#hour data
plt.figure(2)
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

#price
plt.sca(ax1)
plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
plt.plot(hr_price_data, color="blue", lw=1)
plt.plot(hr_ma20_data, color="green", lw=2, label="EMA(20)")
plt.plot(hr_ma60_data, color="black", lw=2, label="EMA(60)")

plt.xlabel("date")
plt.ylabel("price")
plt.title("Hour data")
plt.legend(loc='lower center', shadow=True, fancybox=True)
plt.axis([0, M, min(hr_price_data), max(hr_price_data)])

#volume
plt.sca(ax2)
plt.fill(hr_vol_data, color="red")
plt.xlabel("date")
plt.ylabel("volume")
plt.axis([0, M, 0, max(hr_vol_data)])

plt.show()





