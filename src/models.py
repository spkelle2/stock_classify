import pandas as pd
import numpy as np


class Inflection(object):
    next = None
    prev = None

    def __init__(self, index):
        index = index


class Run(object):
    def __init__(self, stock_id, inflections, orient=None, volatility=None,
                 earnings_per_share=None, averege_prices=None):
        stock_id = stock_id
        inflections = inflections
        orient = orient
        volatility = volatility
        earnings_per_share = earnings_per_share
        ave_price_run = None
        ave_price_200 = None
        ave_price_50 = None