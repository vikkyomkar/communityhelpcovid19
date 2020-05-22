import os
import sys
import influx

placeArray= []
db = 'traininfo'
table = 'places'

trainNo=sys.argv[1]
trainName=sys.argv[2]
fh = open('tmp','r')
#fh2 = open('output','w')


for line in fh:
	placeArray.append(line.strip())

places = ' -> '.join(placeArray)
route = trainName + ' [ ' + places +  ' ]'
for ele in placeArray:
	place = '\ '.join(ele.strip().split(' '))
	postQuery = "{0},trainNo={1},place={2} route=\"{3}\"".format(table,trainNo,place,route)
	print(postQuery)
	influx.Post(db,postQuery)

