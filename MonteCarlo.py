import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from matplotlib import style

style.use('ggplot')

NUM_SIMULATIONS =1000
NUM_STEPS = 252
PERIOD_WINDOW = 500 # this is the period window used at each step to compute the mean and std

prices = pd.read_csv('AAPL.csv')['Close'][-PERIOD_WINDOW:]

simulations = {} # to store all the simulations

for i in range(NUM_SIMULATIONS): 
    returns = prices.pct_change()
    prices_deque = deque(prices, maxlen = PERIOD_WINDOW) # we will drag the window later to compute period specific mean and std
    last_price = prices.iloc[-1]
    all_simul_prices = [last_price]  # we make sure all predictions start at the same price (last real price)
    
    for _ in range(NUM_STEPS):
        sigma =  returns.std()
        mu = returns.mean()
        new_price = last_price * (1 + np.random.normal(mu,sigma))  
        last_price = new_price
        prices_deque.append(new_price)
        returns = pd.Series(prices_deque, name= 'new_prices_deque').pct_change() #redefine the returns variable
        all_simul_prices.append(new_price) # where we store all simulated prices
    simulations.update({f'simul_{i}': all_simul_prices}) 

df_simulations = pd.DataFrame(simulations) 

plt.figure(figsize=(10,6))
plt.plot(df_simulations)
plt.axhline(y = prices.iloc[-1], color ='black', linestyle ='-')  #to have a clear view of the starting point 
plt.xlabel('Days')
plt.ylabel('Prices')
plt.title('Monte Carlo Simulation',fontweight='bold')
plt.show()
