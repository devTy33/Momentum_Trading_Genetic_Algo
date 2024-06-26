import random
import yfinance as yf
from backtest import CMT
import backtrader as bt
import matplotlib.pyplot as plt

MA_TYPE = ["simple", "exponential"]
LOWER_MA_LENGTH = 3
UPPER_MA_FAST_LENGTH = 200
UPPER_MA_LENGTH = 250
SIGNAL_PERIOD_MAX = 300
SIGNAL_PERIOD_MIN = 1
PRICE_FIELDS = ["open", "high", "low", "close"]

average_selected_fitness = []

POPULATION_SIZE = 100
#STRAT_TYPE = ["MACD", "MAC"]
hall_of_fame = [(0,[0,0]), (0,[0,0]), (0,[0,0]), (0,[0,0]), (0,[0,0]), (0,[0,0]), (0,[0,0]), (0,[0,0])]

def graph_results():
    epochs = list(range(25))
    plt.plot(epochs, average_selected_fitness)
    plt.xlabel('Epochs')
    plt.ylabel('Average Selected Fitness')
    plt.title('Plot of Average Selected Fitness over Epochs')
    plt.show()


def add_best(trade_strat, avg_gain, num_trades):
    global hall_of_fame 
    hall_of_fame = sorted(hall_of_fame, key=lambda x: x[1][0])
    for i, winner in enumerate(hall_of_fame):
        if winner[1][0] < avg_gain:
            hall_of_fame[i] = (trade_strat, [avg_gain, num_trades])
            break



class Strategy:
    def __init__(self, fast_ma=None, slow_ma=None, signal_ma=None, ma_type=None, price_field=None):
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.signal_ma = signal_ma
        self.ma_type = ma_type
        self.price_field = price_field
# 

def generate_random_strats(size):
    starting_strats = []

    for i in range(0, size):
        
        strat = Strategy()
        rand_ma_type = random.randint(0, len(MA_TYPE) - 1)
        strat.ma_type = MA_TYPE[rand_ma_type]

        fast_moving_average = 1
        slow_moving_average = 0
        while slow_moving_average < fast_moving_average:                            #
            fast_moving_average = random.randint(LOWER_MA_LENGTH, UPPER_MA_FAST_LENGTH)
            slow_moving_average = random.randint(LOWER_MA_LENGTH, UPPER_MA_LENGTH)
        
        strat.slow_ma = slow_moving_average
        strat.fast_ma = fast_moving_average

        signal_period = random.randint(SIGNAL_PERIOD_MIN, SIGNAL_PERIOD_MAX)
        strat.signal_ma = signal_period

        price_field = random.randint(0, len(PRICE_FIELDS)-1)
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
    total_trades = 0  
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
        num_trades = strategies[0].num_trades
        total_trades = num_trades
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
    add_best(strat, avg_gain, total_trades)
    return avg_gain, total_trades

# 30 percent chance of mutation when preforming uniform crossover
def mutation_prob():
    random_number = random.randint(1,10)
    if random_number <= 2:
        return True
    else:
        return False

# uniform crossover 
def crossover(strat1, strat2):
    uniform = random.randint(1,2)
    if mutation_prob():
        slow_moving_avg = random.randint(LOWER_MA_LENGTH, UPPER_MA_LENGTH)
    else:
        slow_moving_avg = strat1.slow_ma if uniform == 1 else strat2.slow_ma

    # make sure 
    uniform = random.randint(1,2)
    if mutation_prob():
        fast_moving_avg = 500
        while fast_moving_avg > slow_moving_avg:
            fast_moving_avg = random.randint(LOWER_MA_LENGTH, UPPER_MA_FAST_LENGTH)
    else:
        fast_moving_avg = strat1.fast_ma if uniform == 1 else strat2.fast_ma
        if fast_moving_avg > slow_moving_avg and fast_moving_avg == strat1.fast_ma: fast_moving_avg = strat2.fast_ma
        if fast_moving_avg > slow_moving_avg and fast_moving_avg == strat2.fast_ma: fast_moving_avg = strat1.fast_ma

    
    uniform = random.randint(1,2)
    if mutation_prob():
        signal_moving_avg = random.randint(SIGNAL_PERIOD_MIN, SIGNAL_PERIOD_MAX)
    else:
        signal_moving_avg = strat1.signal_ma if uniform == 1 else strat2.signal_ma


    uniform = random.randint(1,2)
    if mutation_prob():
        rand_ma_type = random.randint(0, len(MA_TYPE) - 1)
        moving_avg_type = MA_TYPE[rand_ma_type]
    else:
        moving_avg_type = strat1.ma_type if uniform == 1 else strat2.ma_type
    
    uniform = random.randint(1,2)
    if mutation_prob():
        price_f = random.randint(0, len(PRICE_FIELDS)-1)
        price_type = PRICE_FIELDS[price_f]
    else:    
        price_type = strat1.price_field if uniform == 1 else strat2.price_field
    
    child = Strategy(fast_ma=fast_moving_avg, slow_ma=slow_moving_avg, signal_ma=signal_moving_avg, ma_type=moving_avg_type, price_field=price_type)

    return child



#produces new population and adds parents to new population: 50 children, 20 parents, 30 new randomly produced
def breed(breeding_population):
    # breed 5 times 
    fit = [inner_list[0] for _, inner_list in breeding_population]
    average_selected_fitness.append(sum(fit) / len(fit))
    random.shuffle(breeding_population)
    children = []
    for i in range(0,10):
        #random.shuffle(breeding_population)
        for j in range(0,len(breeding_population)-1, 2):
            parent1 = breeding_population[j] # should be j was i
            parent2 = breeding_population[j+1] # should be j was i
            children.append(crossover(parent1[0], parent2[0]))
        breeding_population = breeding_population[1:] + breeding_population[:1] #shift the index every time to not get identical children / mates

    #random_strats = generate_random_strats(20)
    # return children + random_strats
    return children



#picking parents to breed -- selection 
# tournament of size 5, so there will be 20 winners 
# 20 winners = 10 offspring = 30
# randomly generate 30 new strats
def tournament_selection(population):
    breeding_population = []

    random.shuffle(population)
    tournaments = []
    for i in range(0, len(population), 5):
        tournaments.append(population[i:i+5])

    for tournament in tournaments:
        #most_fit = max(tournament, key=lambda x: x[1])
        most_fit = max(tournament, key=lambda x: x[1][0])
        breeding_population.append(most_fit)

    untested_population = breed(breeding_population)

    return breeding_population, untested_population





def initial_fitness(first_pop, tickers):
    population = []
    for ind in first_pop:
        print("first pop")
        fitness, num_trades = strategy_fitness(ind, tickers)
        population.append((ind, [fitness, num_trades]))
    return population


base_strat = Strategy(fast_ma=12, slow_ma=26, signal_ma=9, ma_type='exponential', price_field='close')
#tickers = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'NFLX', 'GOOG', 'META']
tickers = ['TSLA']

first_pop = generate_random_strats(100)
population = initial_fitness(first_pop, tickers)
#avg,all = strategy_fitness(test_strat, tickers)

#download_data(tickers)

def print_while_run(pop):
    for strat in pop:
        print(strat[1][0], end=" ")  # Use space as the end character to print values on the same line
        # Optionally, you can add a newline character after a certain number of values
        if (i + 1) % 10 == 0:  # Print a newline after every 10 values
            print()  # Print a newline

epochs = 25

for i in range(0,epochs):
    print(i)
    breeding_population, untested_population = tournament_selection(population)
    population.clear()
    for person in untested_population:
        fitness_val, num_trades = strategy_fitness(person, tickers)
        population.append((person, [fitness_val, num_trades]))

    population = population
    print_while_run(population)

############# Print hall of fame and 10 best from last epoch

population = sorted(population, key=lambda x: x[1], reverse=True)

for i in range(0,10):
    print("return: ", population[i][1][0])
    print("number of trades: ", population[i][1][1])
    print("Fast MA:", population[i][0].fast_ma)
    print("Slow MA:", population[i][0].slow_ma)
    print("Signal MA:", population[i][0].signal_ma)
    print("MA Type:", population[i][0].ma_type)
    print("Price Field:", population[i][0].price_field)
    print()


print("---------- All Time Winners -----------")
for winner in hall_of_fame:
    print("return: ", winner[1][0])
    print("Number of trades: ", winner[1][1])
    print("Fast MA:", winner[0].fast_ma)
    print("Slow MA:", winner[0].slow_ma)
    print("Signal MA:", winner[0].signal_ma)
    print("MA Type:", winner[0].ma_type)
    print("Price Field:", winner[0].price_field)
    print()


print("--------- Base line strategy -----------")
print(strategy_fitness(base_strat, tickers))

graph_results()