import pandas as pd 
import numpy as np 



class Inflection(object):
	def __init__(self, index):
		self.index = index
		self._next = None
		self._prev = None




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


def CreateRuns():
	runs = []
	for key in stocks:
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
			#run = RunConstructor(inflections)
			#runs.append(run)
			j=0
			item = start
			while j<deltaJ and item!=None:
				j=j+1
				item = item._next
	return runs





runThreshold = 1
runLength = 3
deltaJ = 2
stocks={} 
stocks['DIS'] = Init('DIS') #, 'AAPL', 'FOXA', 'CBS', 'TMX']
#stocks['AAPL']= Init('AAPL')


runs={}
runs['DIS'] = CreateRuns()











item = stocks['DIS'][0]
data = stocks['DIS'][1]
c=0
while item !=None:
	i = item.index
	if c<10:
		print(i)
	c=c+1
	#print(data['Adj Close'].iloc[i])
	item = item._next






