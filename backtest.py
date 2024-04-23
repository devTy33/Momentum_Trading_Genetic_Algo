import backtrader as bt

class CMT(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        fast_period=12,
        slow_period=26,
        signal_period=9,
        moving_average_type='ema',
        price_type='close'   
    )

    def __init__(self):
        price_data = getattr(self.data, self.params.price_type)
        if self.params.moving_average_type == 'ema':
            self.fast_ma = bt.indicators.EMA(price_data, period=self.p.fast_period)
            self.slow_ma = bt.indicators.EMA(price_data, period=self.p.slow_period)
            self.signal_line = bt.indicators.EMA(self.macd_line, period=self.p.signal_period)
        else:  # Use SMA if not EMA
            self.fast_ma = bt.indicators.SMA(price_data, period=self.p.fast_period)
            self.slow_ma = bt.indicators.SMA(price_data, period=self.p.slow_period)
            self.signal_line = bt.indicators.SMA(self.macd_line, period=self.p.signal_period)
        
        self.macd_line = self.fast_ma - self.slow_ma
        self.macd_crossover = bt.indicators.CrossOver(self.macd_line, self.signal_line)

    def next(self):

        if self.macd_crossover > 0:
            self.buy()  # enter long position
        elif self.macd_crossover < 0:
            self.close()  # close long position