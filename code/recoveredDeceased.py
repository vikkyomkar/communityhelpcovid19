import sys
import datetime
import subprocess
import requests
import json
import influx

### Variables ####
#url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSz8Qs1gE_IYpzlkFkCXGcL_BqR8hZieWVi-rphN1gfrO3H4lDtVZs4kd0C3P8Y9lhsT1rhoB-Q_cP4/pub?output=csv&gid=200733542"
url = "https://api.covid19india.org/csv/latest/death_and_recovered.csv"
db = sys.argv[1]
table = 'covid_india'

### removed 'Nagaland' : 'NL'
dummyData = {'Meghalaya' : 'ML','Assam' : 'AS','Jharkhand' : 'JH' ,'Andaman_and_Nicobar_Islands' : 'AN','Arunachal_Pradesh': 'AR','Chandigarh' : 'CH','Chhattisgarh': 'CT','Goa' : 'GA','Ladakh' : 'LA','Manipur' : 'MN','Uttarakhand' : 'UT','Tripura' : 'TR' ,'Puducherry' : 'PY','Mizoram' : 'MZ'}

for case in ['Recovered','Deceased']:
	for k,v in dummyData.items():
		postQuery = "{0},detectedstate={1},statecode={2} {3}=0".format(table,k,v,case)
		influx.Post(db,postQuery)

for case in ['NewConfirmed','newRecovered','newDeceased']:
	postQuery = "{0},detectedstate=Maharashtra,statecode=Mumbai {1}=0".format(table,case)
	influx.Post(db,postQuery)

def dataProcess():
	startHr = 1
	flag = 0
	FH = open('/mnt/covid/deathRecoverdata','r')
	for line1 in FH:
		try:
			line = line1.replace('#','')
			city = 'Details_Awaited'
			district = 'Details_Awaited'
			state = 'Details_Awaited'
			statecode = 'Details_Awaited'
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
					#### Condition due to wrong data in sheet 159 line in recovery sheet
					state = '_'.join(pArray[7].split(' ')) 
					if state == "Hyderabad":
						state = 'Andhra_Pradesh'
						district = 'Hyderabad'
				if pArray[8] != "":
					statecode = '_'.join(pArray[8].split(' '))
				postQuery = "{0},city={1},detecteddistrict={2},detectedstate={3},statecode={4} {5}=1".format(table,city,district,state,statecode,pArray[4])
				if int(d) == int(datetime.datetime.now().day) and int(m) == int(datetime.datetime.now().month):
					postQuery = postQuery + ",new{0}=1".format(pArray[4])
				postQuery = postQuery + " {0}".format(int(date)+flag)

				influx.Post(db,postQuery)
		except Exception as e:
			print(e)
			sys.exit(1)

##### Fetch data Starts here########
try:
	#req = requests.get(url)
	#if req.status_code == 200:
	dataProcess()
except Exception as e:
	print(e)
	sys.exit(1)
