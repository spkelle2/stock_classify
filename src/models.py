import pandas as pd
import numpy as np



class Inflection(object):
    def __init__(self, index):
        self.index = index
        self._next = None
        self._prev = None




class Run(object):
    def __init__(self, stock_id, inflections, orient=None, volatility=None,
                 earnings_per_share=None, averege_prices=None):
        self.stock_id = stock_id
        self.inflections = inflections
        self.orient = orient
        self.volatility = volatility
        self.earnings_per_share = earnings_per_share
        self.RunPrices = None
        self.ave_price_200 = None
        self.ave_price_50 = None