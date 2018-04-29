import pandas as pd 
import numpy as np 
from models import Run, Inflection
import matplotlib.pyplot as plt
from split import split

#Git status
#Git Add
#Git commit
#git push origin master

#git fetch 
#git merge origin master

#git branch
#git checkout -b Josh

#git checkout master
#git branch -D Josh



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
			if item._next !=None:
				if item._prev !=None: 	
					item._prev._next = item._next._next
				if item._next._next!=None:
					item._next._next.prev = item._prev
				item._next = item._next._next
			elif item._prev !=None: 	
				item._prev._next = None
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





runThreshold = 1  #Dollars
runLength = 2   #INflection Points
deltaJ = 2
stocks={} 
stocks['DIS'] = Init('DIS') #, 'AAPL', 'FOXA', 'CBS', 'TMX']
#stocks['AAPL']= Init('AAPL')
runs={}
for key in stocks:
	runs[key] = CreateRuns(key)



#for run in runs['DIS']:
	#print("RUN:")
	#for inflection in run.inflections:
	#	print(stocks['DIS'][1]['Adj Close'].iloc[inflection.index])
	#print("\n")




for key in runs:
	DataMatrix = np.zeros((len(runs[key])-1,2))
	for i in range(len(runs[key])-1):
		runs[key][i].RunPrices = np.array(stocks[key][1]['Adj Close'][runs[key][i].inflections[0].index:runs[key][i].inflections[runLength-1].index+1])
		#print(stocks[key][1]['Adj Close'][runs[key][i].inflections[1].index],stocks[key][1]['Adj Close'][runs[key][i].inflections[0].index])
		DataMatrix[i,0] = stocks[key][1]['Adj Close'][runs[key][i].inflections[1].index]-stocks[key][1]['Adj Close'][runs[key][i].inflections[0].index]
		DataMatrix[i,1] = stocks[key][1]['Adj Close'][runs[key][i].inflections[runLength-1]._next.index]-stocks[key][1]['Adj Close'][runs[key][i].inflections[runLength-1].index]

SortedDataMatrix = DataMatrix[DataMatrix[:,0].argsort()]
#print(DataMatrix)
#for i in range(SortedDataMatrix.shape[0]):
#	print(SortedDataMatrix[i,:])

print(SortedDataMatrix.shape)

results = split(range(10),SortedDataMatrix[0:10,1],.001)


for v in results['variables']:
    if v.name[0] == 'x':
        print("%s = %s" %(v.name, v.varValue) )


#plt.scatter(SortedDataMatrix[0:end,0],SortedDataMatrix[0:end,1], color = 'red')
#plt.scatter(SortedDataMatrix[end:10,0],SortedDataMatrix[end:10,1], color = 'blue')

#plt.show()	




