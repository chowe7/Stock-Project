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



'''
for i in range(0, len(date_close)):



#print(mydata)
print(date_close)
print(date_open)

date_close.to_csv('closing.csv')
#when the file is run it rewrites the csv and eliminates the header

data = pd.read_csv('closing.csv', delimiter = ',')

d = []

for i in range(0, len(data)):
    d.append(i)
'''
'''
#np.polyfit fits the data to a polynomial, with this case in particular being a polynomial to the power of 1
#which leads to a linear fit. This returns the coefficent(s) and y intercept
#np.poly1d turns this into a function called fit_fn
fit = np.polyfit(d, data['Close'], 1)
fit_fn = np.poly1d(fit)    


#Here we calculate the sum of the residuals, which is the sum of the abslute value of the
#difference between the value for point on the linear fit and 
#the actual value from the data at the same position of x. 
#We then average it and use these averages to create confidence band above and below our linear fit
resid_sum = 0
resid_avg = 0

for i in range(0, len(data.index)):
    resid_sum += abs(fit_fn(d[i]) - data['Close'][i])

resid_avg = resid_sum / len(data.index)

#Here we alter the data points to take into account the residuals
resid_up = []
resid_down = []

for i in range(0, len(data.index)):
    resid_up.append(fit_fn(d[i]) + resid_avg)

for i in range(0, len(data.index)):
    resid_down.append(fit_fn(d[i]) - resid_avg)


#This is fitting the new residual data points, one set for + residual_avg and one set for - residual_avg,
#to a new linear fit function
fit_up = np.polyfit(d, resid_up, 1)
fit_down = np.polyfit(d, resid_down, 1)

fit_fn_up = np.poly1d(fit_up)
fit_fn_down = np.poly1d(fit_down)

sec_arr = []
sec_down = []
sec_up = [] 

fin_arr = []
fin_arr_down = []
fin_arr_up = []

resid_sum = 0
resid_avg = 0
print(len(d)/20)

for i in range(0, len(d) - int(((len(d))/20))):
    sec_arr = []
    sec_down = []
    sec_up = [] 

    resid_up = []
    resid_down = []

    resid_sum = 0
    resid_avg = 0

    for j in range(i, i + int(len(d)/20)):

        sec_arr.append(data['Close'][i])

    fit = np.polyfit(d[0:5], sec_arr, 1)
    fit_fn = np.poly1d(fit)

    for k in range(0, len(sec_arr)):
        resid_sum += abs(fit_fn(k) - sec_arr[k])
        
    resid_avg = resid_sum / len(sec_arr)

    for k in range(0, len(sec_arr)):
        resid_up.append(fit_fn(k) + resid_avg)

    for k in range(0, len(sec_arr)):
        resid_down.append(fit_fn(k) - resid_avg)

    fit_up = np.polyfit(d[0:5], resid_up, 1)
    fit_down = np.polyfit(d[0:5], resid_down, 1)

    fit_fn_up = np.poly1d(fit_up)
    fit_fn_down = np.poly1d(fit_down)


        
    fin_arr.append(fit_fn(d[5]))
    fin_arr_up.append(fit_fn_up(d[5]))
    fin_arr_down.append(fit_fn_down(d[5])) 


print('len of fin_arr')
print(len(fin_arr))
print(len(d[0:95]))

plt.plot(d[0:95], fin_arr, d[0:95], fin_arr_up, d[0:95], fin_arr_down)

Plotting the line of best fit along with the confidence bands 
plt.plot(d, data['Close'], 'ko', d, fit_fn(d), 'k', 
d, fit_fn_down(d), 'g', d, fit_fn_up(d), 'g')



plt.show()
'''