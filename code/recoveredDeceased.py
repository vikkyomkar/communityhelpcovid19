import sys
import datetime
import subprocess
import requests
import json
import influx

### Variables ####
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pub?output=csv&gid=200733542"
db = sys.argv[1]
table = 'covid_india'

dummyData = ['Assam','Jharkhand','Andaman_and_Nicobar_Islands','Arunachal_Pradesh','Chandigarh','Chhattisgarh','Dadra_and_Nagar_Haveli','Goa','Ladakh','Manipur','Uttarakhand','Tripura','Puducherry','Mizoram']
for case in ['Recovered','Deceased']:
	for state in dummyData:
		postQuery = "{0},detectedstate={1} {2}=0".format(table,state,case)
		influx.Post(db,postQuery)

#for case in ['newConfirmed', 'newRecovered','newDeceased']:
#	postQuery = "{0},detectedstate=Arunachal_Pradesh {1}=0".format(table,case)
#	influx.Post(db,postQuery)

def dataProcess(textdata):
	startHr = 1
	flag = 0
	for line1 in textdata.split('\n'):
		try:
			line = line1.replace('#','')
			city = 'UnKnown'
			district = 'UnKnown'
			state = 'UnKnown'
			#pDict = {'city' : 5, 'b_district' : 6, 'a_state' : 7}
			pArray = line.split(',')
			if pArray[4] != "" and pArray[1] != "Date" and pArray[7] not in ['Kerala/Puducherry?']:
				flag +=1
				startHr += 1
				if startHr > 23:
					startHr = 1
				d,m,y = pArray[1].split('/')
				date = (datetime.datetime(int(y), int(m), int(d), startHr, 0).strftime('%s')) + "000000000"
				if pArray[5] != "":
					city = '_'.join(pArray[5].split(' '))
				if pArray[6] != "":  
					district = '_'.join(pArray[6].split(' ')) 
				if pArray[7] != "":
					state = '_'.join(pArray[7].split(' ')) 
				
				#postQuery = "{0},city={1},bdistrict={2},state={3} {4}=1".format(table,city,district,state,pArray[4])
				postQuery = "{0},city={1},bdistrict={2},detectedstate={3} {4}=1".format(table,city,district,state,pArray[4])
				if int(d) == int(datetime.datetime.now().day) and int(m) == int(datetime.datetime.now().month):
					postQuery = postQuery + ",new{0}=1".format(pArray[4])
				postQuery = postQuery + " {0}".format(int(date)+flag)

				influx.Post(db,postQuery)
		except Exception as e:
			print(e)
			sys.exit(1)

##### Fetch data Starts here########
try:
	req = requests.get(url)
	if req.status_code == 200:
		dataProcess(req.text)
except Exception as e:
	print(e)
	sys.exit(1)

