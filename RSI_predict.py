import numpy as np
from datetime import datetime, date, time
import matplotlib.pyplot as plt
import pandas as pd
import quandl
import csv

mydata = quandl.get('WIKI/F', start_date="2001-12-31", end_date="2002-5-23", returns='pandas', header=True)
#print(mydata)
mydata.to_csv('closing.csv')

date_close = mydata.filter(['Close'])
date_open = mydata.filter(['Open'])
#dummy values
date_RSI = mydata.filter(['Open'])



for i in range(0, 10):
    date_RSI['Open'][i] = 0


for i in range(0, len(date_close) - 10):

    sliceup = 0
    slicedown = 0
    for j in range(0, 10):
        change = date_close['Close'][i + j] - date_open['Open'][i + j]
        if change < 0:
            pchange = change / date_open['Open'][j]
            slicedown = slicedown + abs(pchange)
        else:
            pchange = change / date_open['Open'][i + j]
            sliceup = pchange + sliceup
    avgdown = slicedown / 10
    avgup = sliceup / 10
    rs = avgup / avgdown
    rsi = 100 - (100 / (1 + rs))
    date_RSI['Open'][i + 10] = rsi

date_RSI.to_csv('RSI.csv')

pl = 0
count = 0
#make an increment counter so itll only sell after a buy and vice versa 
for i in range(10, len(date_close)):

    if (date_RSI['Open'][i] <= 30) & (count == 0):
        print('buy')
        position = mydata['Open'][i]
        count = 1
    
    if (date_RSI['Open'][i] >= 70) & (count == 1):
        print('sell')
        pl = pl + (mydata['Open'][i] - position)
        position = 0
        count = 0


print(pl) 
