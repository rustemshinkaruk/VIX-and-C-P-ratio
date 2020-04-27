import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

data=pd.read_csv('daily volume.csv')
data['call']= data.iloc[:,1].str.replace(',', '')
data['put']= data.iloc[:,2].str.replace(',', '')

data.date=data.date.map(lambda x: datetime.datetime.strptime(x,'%m/%d/%Y'))
data['call']=(data['call'].astype(str)).astype(float)
data['put']=(data['put'].astype(str)).astype(float)

data=data.sort_values(by='date')
data['c/p ratio']=data['call']/data['put']
data['total']=data['call']+data['put']
data['dif']=1-data['c/p ratio']
data.set_index('date',inplace=True)



vix=pd.read_csv('^VXO.csv')
vix.Date=vix.Date.map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))
vix.set_index('Date',inplace=True)


sp500=pd.read_csv('^GSPC.csv')
sp500.Date=sp500.Date.map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))
sp500.set_index('Date',inplace=True)
sp500['ret']=(sp500.Close-sp500.Close.shift(1))/sp500.Close.shift(1)
sp500['realized']=sp500.ret.rolling(7).std()*100*np.sqrt(252)

sp500.realized.plot()
vix.Close.plot()





ax = plt.subplot(111)
(data['c/p ratio']).plot(ax=ax,rot=0)
ax.set_ylabel('Call-to-Put ratio')
ax2=ax.twinx()
vix.Close.plot(ax=ax2,color='orange')
ax2.set_ylabel('VIX')
ax.set_title("VIX vs Call-to-Put ratio")
ax.legend(('C/P ratio',),loc=2)
ax2.legend(('VIX',),loc=1)
ax.set_xlabel("")

# Define the date format
#date_form = DateFormatter("%m-%d")
#date_form = DateFormatter("%b")
date_form = DateFormatter("%b-%y")
ax.xaxis.set_major_formatter(date_form)
## Ensure a major tick for each week using (interval=1) 
#ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
locator = mdates.MonthLocator(interval=1)
ax.xaxis.set_major_locator(locator)


ax.annotate("1",xy=('2020-01-24 00:00:00',0.986647),xytext=('2020-01-02 00:00:00',1.1),
            arrowprops=dict(facecolor='black',width=1),
            fontsize=14)
ax.annotate("2",xy=('2020-02-21 00:00:00',1.07046),xytext=('2020-02-03 00:00:00',0.9),
            arrowprops=dict(facecolor='black',width=1),
            fontsize=14)


fig = plt.gcf()
fig.set_size_inches(11.5, 7.5)
fig.savefig('test2png.png', dpi=100)














