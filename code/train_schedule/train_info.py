import os
import sys
import influx

placeArray= []
db = 'traininfo'
table = 'routes'

fh = open('train_data','r')
fh2 = open('output','w')

for line in fh:
	placeArray= []
	trainNo,trainName = line.strip().split(',')
	stream = os.popen('curl https://erail.in/train-running-status/{0}?date=22-May-2020 |grep stndetailrun'.format(trainNo))
	output = stream.read()
	
	array1 = output.split(' >')[1:]
	for e in array1:
		if " - " in e:
			place = e.split('-')[0].strip()
			placeArray.append(place)

	places = ' -> '.join(placeArray)
	route = trainName + ' [ ' + places +  ' ]'

	placestag = '|'.join(placeArray)
	routetag = '\ '.join(placestag.strip().split(' '))

	fh2.write("{0} - {1}".format(trainNo,route))

	for ele in placeArray:
		place = '\ '.join(ele.strip().split(' '))
		postQuery = "{0},trainNo={1},place={2},routetag={3} route=\"{4}\"".format(table,trainNo,place,routetag,route)
		influx.Post(db,postQuery)
