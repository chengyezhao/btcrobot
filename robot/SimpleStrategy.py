__author__ = 'yunling'

import numpy as np
import logging, os

logging.basicConfig(filename = os.path.join(os.getcwd(), 'SimpleRobot.log'), level = logging.INFO)

LONG_WINDOW_SIZE = 60 * 12 #12 horus
SHORT_WINDOW_SIZE = 10 #30 mins
MIN_TH = -10
MAX_HT = 10

class SimpleStrategy:

    def __init__(self, market):
        self.market = market

    def getBuyConfident(self):
        trend_index_long = self.market.getMarketTrendIndexInLastN(LONG_WINDOW_SIZE)
        index_480 = [x['index_480'] for x in trend_index_long]
        index_240 = [x['index_240'] for x in trend_index_long]
        index_120 = [x['index_120'] for x in trend_index_long]
        index_60 = [x['index_60'] for x in trend_index_long]

        trend_index_short = self.market.getMarketTrendIndexInLastN(SHORT_WINDOW_SIZE)
        index_480_s = [x['index_480'] for x in trend_index_short]
        index_240_s = [x['index_240'] for x in trend_index_short]
        index_120_s = [x['index_120'] for x in trend_index_short]
        index_60_s = [x['index_60'] for x in trend_index_short]

        #long term price stable delta
        price_delta = np.average(np.asarray(index_240))
        current_index_60 = index_60[-1]
        current_index_120 = index_120[-1]

        #short term trend diff
        diff_60 = np.diff(np.array(index_60_s))
        diff_120 = np.diff(np.array(index_120_s))
        diff_240 = np.diff(np.array(index_240_s))

        diff_60_score = np.average(diff_60[1:])

        logging.info("Long term price_delta = %s, current_index_60 = %s, current_index_60 - price_delta = %s,  current_index_120 = %s, diff_60_score = %s"
                     ,price_delta , current_index_60,  current_index_60 - price_delta, current_index_120, diff_60_score)


        if current_index_60 - price_delta < MIN_TH:  ## check for buy actio
        # n
            if diff_60_score > -0.15:
                return 0.85
            else:
                return 0.7
        elif current_index_60 - price_delta > MAX_HT:  ##check for sell acton
            if diff_60_score < -0.15:
                return 0.25
            else:
                return 0.4
        elif current_index_120 < 0:    #check for sell action
            return 0.25
        elif current_index_120 > 0:     #check for buy action
            return 0.85
        else:
            return 0.5

