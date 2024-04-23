import random
import yfinance as yf
from backtest import CMT

MA_TYPE = ["simple", "exponential"]
LOWER_MA_LENGTH = 3
UPPER_MA_LENGTH = 250
SIGNAL_PERIOD_MAX = 300
SIGNAL_PERIOD_MIN = 1
PRICE_FIELDS = ["Open", "High", "Low", "Close"]

POPULATION_SIZE = 100
#STRAT_TYPE = ["MACD", "MAC"]



def generate_initial_strats():
    starting_strats = []

    for i in range(0, POPULATION_SIZE):
        strat = []
        rand_ma_type = random.randint(0, len(MA_TYPE) - 1)
        strat.append(MA_TYPE[rand_ma_type])

        fast_moving_average = 1
        slow_moving_average = 0
        while slow_moving_average < fast_moving_average:                            #
            fast_moving_average = random.randint(LOWER_MA_LENGTH, UPPER_MA_LENGTH)
            slow_moving_average = random.randint(LOWER_MA_LENGTH, UPPER_MA_LENGTH)
        strat.append(fast_moving_average)
        strat.append(slow_moving_average)
        
        signal_period = random.randint(SIGNAL_PERIOD_MIN, SIGNAL_PERIOD_MAX)
        strat.append(signal_period)

        price_field = random.randint(0, len(PRICE_FIELDS)-1)
        strat.append(PRICE_FIELDS[price_field])
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







trade = generate_initial_strats()

tickers = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'NFLX', 'GOOG', 'META']

download_data(tickers)



