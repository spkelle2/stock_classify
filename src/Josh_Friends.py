import pandas as pd 
import numpy as np 
from models import Run, Inflection





def Init(stock) :
	rawData = pd.read_csv(stock + '.csv')
	rawData2 = pd.read_csv(stock + '-2.csv')
	length = rawData['Date'].count()
	rawData.reset_index(drop = True)
	rawData2.reset_index(drop = True)
	rawData['Delta'] = rawData2['Adj Close']-rawData['Adj Close'] 
	print("Read ", stock)
	return (loop_construct(rawData), rawData)



def loop_construct(data):
	last_ = None
	next_ = None
	curr = None
	first = False
	for i in range(data.shape[0]):
		if i > 0:
			last = curr
			if data['Delta'].iloc[i]*data['Delta'].iloc[i-1]<0:# and  (abs(data['Delta'].iloc[i])>runThreshold or data['Delta'].iloc[i-1]*data['Delta'].iloc[i+1]<0):
				curr = Inflection(i)
				curr._prev = last
				if last != None:
					last._next = curr
				if first == False:
					start = curr
					first = True
	return start


def CreateRuns(key):
	runs = []
	item = stocks[key][0]
	data = stocks[key][1]
	while item != None:
		if abs(data['Delta'].iloc[item.index])<runThreshold and data['Delta'].iloc[ item.index -1  ]*data['Delta'].iloc[item.index+1]>0:
			item._prev._next = item._next._next
			item._next._next.prev = item._prev
			item._next = item._next._next
		item = item._next
	item = stocks[key][0]
	while item != None:
		inflections = []
		inflections.append(item)
		n=0
		start = item
		while n<runLength-1 and item!=None:
			n=n+1
			inflections.append(item._next)
			item = item._next
			finish = item
		if finish !=None:
			_run = Run(key, inflections)
			runs.append(_run)
		j=0
		item = start
		while j<deltaJ and item!=None:
			j=j+1
			item = item._next
	return runs





runThreshold = 1
runLength = 3
deltaJ = 1
stocks={} 
stocks['DIS'] = Init('DIS') #, 'AAPL', 'FOXA', 'CBS', 'TMX']
#stocks['AAPL']= Init('AAPL')
runs={}
for key in stocks:
	runs[key] = CreateRuns(key)



for run in runs['DIS']:
	print("RUN:")
	for inflection in run.inflections:
		print(stocks['DIS'][1]['Adj Close'].iloc[inflection.index])
	print("\n")



c=0
for key in runs:
	for run in runs[key]:
		run.RunPrices = np.array(stocks[key][1]['Adj Close'][run.inflections[0].index:run.inflections[runLength-1].index+1])
		#ToDo: Potential error in indexing
		if c == 0 or c==1:
			print(run.RunPrices)
		c=c+1










