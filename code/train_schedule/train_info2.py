import os
import sys
import influx

placeArray= []
db = 'traininfo'
table = 'places'

fh = open('train_data1','r')
#fh2 = open('output','w')

for line in fh:
	tplaceArray= []
	trainNos,trainName = line.strip().split('\t')
	no1,no2 = trainNos.split('/')
	stream = os.popen('curl https://erail.in/train-running-status/{0}?date=22-May-2020 |grep stndetailrun'.format(no1))
	output = stream.read()
	
	array1 = output.split(' >')[1:]
	for e in array1:
		if " - " in e:
			place = e.split('-')[0].strip()
			tplaceArray.append(place)
	placeArray = tplaceArray[::-1]
	
	places = ' -> '.join(placeArray)
	route = trainName + ' [ ' + places +  ' ]'
	#fh2.write("{0} - {1}\n".format(trainNo,route))

	for ele in placeArray:
		place = '\ '.join(ele.strip().split(' '))
		postQuery = "{0},trainNo={1},place={2} route=\"{3}\"".format(table,no2,place,route)
		print(postQuery)
		influx.Post(db,postQuery)

