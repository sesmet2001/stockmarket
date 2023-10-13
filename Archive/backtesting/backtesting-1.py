# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 17:27:39 2021

@author: sefsmet
"""

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import backtesting

from backtesting.test import SMA, GOOG


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 50)

    def next(self):
        if crossover(self.data.Close,self.ma2):
            self.buy()
        elif crossover(self.ma2,self.data.Close):
            self.sell()

backtesting.set_bokeh_output(notebook=False)
bt = Backtest(AMD, SmaCross, commission=.002,
              exclusive_orders=True)
stats = bt.run()
print(stats)
#bt.display()