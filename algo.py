import random
import yfinance as yf
from backtest import CMT
import backtrader as bt
import matplotlib.pyplot as plt

MA_TYPE = ["simple", "exponential"]
LOWER_MA_LENGTH = 3
UPPER_MA_LENGTH = 250
SIGNAL_PERIOD_MAX = 300
SIGNAL_PERIOD_MIN = 1
PRICE_FIELDS = ["open", "high", "low", "close"]

POPULATION_SIZE = 100
#STRAT_TYPE = ["MACD", "MAC"]

class Strategy:
    def __init__(self, fast_ma=None, slow_ma=None, signal_ma=None, ma_type=None, price_field=None):
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.signal_ma = signal_ma
        self.ma_type = ma_type
        self.price_field = price_field
# 

def generate_initial_strats():
    starting_strats = []

    for i in range(0, POPULATION_SIZE):
        #strat = []
        strat = Strategy()
        rand_ma_type = random.randint(0, len(MA_TYPE) - 1)
        #strat.append(MA_TYPE[rand_ma_type])
        strat.ma_type = MA_TYPE[rand_ma_type]

        fast_moving_average = 1
        slow_moving_average = 0
        while slow_moving_average < fast_moving_average:                            #
            fast_moving_average = random.randint(LOWER_MA_LENGTH, UPPER_MA_LENGTH)
            slow_moving_average = random.randint(LOWER_MA_LENGTH, UPPER_MA_LENGTH)
        #strat.append(fast_moving_average)
        #strat.append(slow_moving_average)
        strat.slow_ma = slow_moving_average
        strat.fast_ma = fast_moving_average

        signal_period = random.randint(SIGNAL_PERIOD_MIN, SIGNAL_PERIOD_MAX)
        #strat.append(signal_period)
        strat.signal_ma = signal_period

        price_field = random.randint(0, len(PRICE_FIELDS)-1)
        #strat.append(PRICE_FIELDS[price_field])
        strat.price_field = PRICE_FIELDS[price_field]
        starting_strats.append(strat)

    return starting_strats



def download_data(tickers):
    for ticker in tickers:
        output_file = f'data/{ticker}.csv'
        #yf.download(ticker).to_csv(output_file)
        data = yf.download(ticker, period="max", progress=False)
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        data.to_csv(output_file)



#def run_backtest():


def strategy_fitness(strat, tickers):
    total_gain = 0
    perc_gains = []
    for stock in tickers:
        cerebro = bt.Cerebro()
        cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
        # Add the CMT strategy to the cerebro
        cerebro.addstrategy(CMT, fast_period=strat.fast_ma, slow_period=strat.slow_ma, signal_period=strat.signal_ma, moving_average_type=strat.ma_type, price_type=strat.price_field)

        # Add the stock data to the cerebro
        data = bt.feeds.GenericCSVData(
            dataname=f'data/{stock}.csv',
            dtformat=('%Y-%m-%d'),
            datetime=0,
            high=2,
            low=3,
            open=1,
            close=4,
            volume=5,
            openinterest=-1
        )
        cerebro.adddata(data)

        cerebro.broker.setcash(10000.0)

        strategies = cerebro.run()
        # plotting -----------

        # Plot the stock price and strategy equity
        '''
        cerebro.plot(
            figscale=1.5,
            style='line',
            title='Equity Curves',
            ylabel='Equity',
            ylabel_lower='Equity',
            plotdist=0.7,
            figratio=(10, 5),
            equity=True,
            subplots=True,
        )
        '''
        

        # --------------------
        final_value = cerebro.broker.getvalue()

        gain = (final_value - 10000.0) / 10000.0 * 100.0
        perc_gains.append(gain)
        total_gain += gain

    # Calculate the average gain across all stocks
    avg_gain = total_gain / len(tickers)

    return avg_gain, perc_gains



#crossover

#mutation


#picking parents to breed -- selection 





test_strat = Strategy(fast_ma=12, slow_ma=26, signal_ma=9, ma_type='exponential', price_field='close')


trade = generate_initial_strats()

tickers = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'NFLX', 'GOOG', 'META']
avg,all = strategy_fitness(test_strat, tickers)
print(avg)
print(all)

#print(trade)

#download_data(tickers)



