__author__ = 'yunling'

import numpy as np
import logging
import os

logging.basicConfig(filename = os.path.join(os.getcwd(), 'SimpleRobot.log'), level = logging.INFO)

LONG_WINDOW_SIZE = 60 * 6   #12 hours
SHORT_WINDOW_SIZE = 5       #5 mins
MIN_TH = -10
MAX_TH = 10

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
        price_delta_240 = np.average(np.asarray(index_240))
        price_delta_480 = np.average(np.asarray(index_480))

        current_index_60 = index_60[-1]
        current_index_120 = index_120[-1]
        current_index_240 = index_240[-1]
        current_index_480 = index_480[-1]


        #short term trend diff
        diff_60 = np.diff(np.array(index_60_s))
        diff_120 = np.diff(np.array(index_120_s))
        diff_240 = np.diff(np.array(index_240_s))
        diff_480 = np.diff(np.array(index_480_s))

        diff_60_score = np.average(diff_60[1:])
        diff_120_score = np.average(diff_120[1:])
        diff_240_score = np.average(diff_240[1:])
        diff_480_score = np.average(diff_480[1:])

        logging.info("\ncurrent_index_120 - price_delta_240 = %s, \ncurrent_index_240 - price_delta_480 = %s, \ndiff_120_score = %s, \ndiff_240_score = %s"
                     ,current_index_120 - price_delta_240, current_index_240 - price_delta_480, diff_120_score, diff_240_score)

        if current_index_120 - price_delta_240 < MIN_TH:  ## check short term trend for buy
            if diff_120_score > -0.15:
                return 0.85                 #start buy
            else:
                return 0.7                  #pause buy
        elif current_index_120 - price_delta_240 > MAX_TH:  ##check short term trend for sell
            if diff_120_score < 0.15:
                return 0.25                 #start sell
            else:
                return 0.4                  #pause sell
        elif current_index_240 - price_delta_480 < MIN_TH:    #if the middle term trend is still down, sell
            if diff_240_score > -0.1:
                return 0.90                 #start buy
            else:
                return 0.7                  #pause buy
        elif current_index_240 - price_delta_480 > MAX_TH:     #if the middle term trend is still up, buy
            if diff_240_score < 0.1:
                return 0.20                 #start sell
            else:
                return 0.4                  #pause sell
        elif diff_480_score > 0:
            return 0.95                     #start buy
        elif diff_480_score < 0:
            return 0.15
        else:                               #start sell
            return 0.5

