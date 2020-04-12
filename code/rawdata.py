import sys
import json
import datetime
import subprocess
import influx

### Variables ####
db = sys.argv[1] 
table = "covid_india"

with open('/mnt/covid/rawdata') as f:
	data = json.load(f)

totalConfirm = 0
todayConfirm = 0
startHr = 1
ages = {'0-10' : 0, '11-20' : 0 , '21-30' : 0, '31-40': 0, '41-50': 0, '51-60': 0, '61-70':0, '71-80': 0, '81-90': 0,'91-100' : 0 }

for patient in data['raw_data']:
	try:
		flag = 0
		postQuery = "{0}".format(table)
		#ages = {'0-10' : 0, '11-20' : 0 , '21-30' : 0, '31-40': 0, '41-50': 0, '51-60': 0, '61-70':0, '71-80': 0, '81-90': 0,'91-100' : 0 }
		patientDict = {'agebracket' 	: 'Details_Awaited', 
				'gender' 	: 'Details_Awaited',
				'detectedcity'	: 'Details_Awaited',
				'detecteddistrict': 'Details_Awaited',
				'detectedstate' : 'Details_Awaited',
				'statecode'	: 'Details_Awaited',
				'nationality': 'Details_Awaited',
				'typeoftransmission' : 'TBD'
				}
		if patient['agebracket'] != "":
			age = int(patient['agebracket'].split('-')[0])	
			if age >= 0 and age <= 10:
				ages['0-10'] += 1
			elif age > 10 and age <= 20:
				ages['11-20'] += 1
			elif age > 20 and age <= 30:
				ages['21-30'] += 1 
			elif age > 30 and age <= 40:
				ages['31-40'] += 1 
			elif age > 40 and age <= 50:
				ages['41-50'] += 1 
			elif age > 50 and age <= 60:
				ages['51-60'] += 1 
			elif age > 60 and age <= 70:
				ages['61-70'] += 1 
			elif age > 70 and age <= 80:
				ages['71-80'] += 1 
			elif age > 80 and age <= 90:
				ages['81-90'] += 1
			elif age > 90 and age <= 100:
				ages['91-100'] += 1

		#if  patient['detectedstate'] not in ['Kerala/Puducherry?','Details Awaited']:
		for k,v in  patientDict.items():
			if  patient[k] != "":
				flag +=1
				patientDict[k] = '_'.join(patient[k].split(' '))
		if flag != 0:
			if patientDict['detectedstate'] in ['Kerala/Puducherry','Details_Awaited']:
				continue 
				#print(patientDict['detectedstate'])

			totalConfirm += 1
			startHr += 1
			if startHr > 23:
				startHr = 1

			d,m,y = patient['dateannounced'].split('/')
			announcedate = (datetime.datetime(int(y), int(m), int(d), startHr, 0).strftime('%s')) + "000000000"

			for k,v in  patientDict.items():
				postQuery = "{0},{1}={2}".format(postQuery,k,v)

			if int(d) == int(datetime.datetime.now().day) and int(m) == int(datetime.datetime.now().month):
				postData = "{0} Confirmed=1,NewConfirmed=1 {1}".format(postQuery,int(announcedate) + totalConfirm)
			else:
				postData = "{0} Confirmed=1 {1}".format(postQuery,int(announcedate) + totalConfirm)
			
			influx.Post(db,postData)
	except Exception as e:
		print(e)

for k,v in ages.items():
	postQuery="{0},age_bracket={1} count={2}".format(table,k,v)
	influx.Post(db,postQuery)	





