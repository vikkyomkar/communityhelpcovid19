import sys
import datetime
import subprocess
import requests
import json
import influx

### Variables ####
##url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSz8Qs1gE_IYpzlkFkCXGcL_BqR8hZieWVi-rphN1gfrO3H4lDtVZs4kd0C3P8Y9lhsT1rhoB-Q_cP4/pub?output=csv&gid=486127050"
url = "https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv"
db = sys.argv[1]
#table = 'sampleTests'
table = 'covid_india'

population = {
	"Uttar_Pradesh" : 223897418,
	"Maharashtra" : 124945748,
	"Bihar" : 121741741,
	"West_Bengal" : 98785114,
	"Andhra_Pradesh" : 87641369,
	"Madhya_Pradesh" : 82961852,
	"Tamil_Nadu" : 80288487,
	"Rajasthan" : 77122315,
	"Karnataka" : 68159821,
	"Gujarat" : 68927491,
	"Odisha" : 46172447,
	"Kerala" : 34732356,
	"Jharkhand" : 34149478,
	"Assam" : 32652597,
	"Punjab" : 30471254,
	"Haryana" : 28237755,
	"Chhattisgarh" : 27134411,
	"Jammu_and_Kashmir" : 14591623,
	"Uttarakhand" : 11453488,
	"Himachal_Pradesh" : 7234695,
	"Tripura" : 3914581,
	"Meghalaya" : 3257373,
	"Nagaland" : 2063533,
	"Goa" : 1562488,
	"Arunachal_Pradesh" : 1511873,
	"Mizoram" : 1156288,
	"Delhi" : 16787941,
	"Chandigarh" : 1249223,
	"Ladakh" : 133487
}

for k,v in population.items():
	postQuery = "{0},detectedstate={1} population={2}".format(table,k,v)
	#print(postQuery)
	influx.Post(db,postQuery)

def dataProcess():
	FH = open('/mnt/covid/sampletestdata','r')
	for line in FH:
		try:
			#positiveTests = 0
			testArray = line.split(',')
			if testArray[1] != "" and testArray[2] != "" and testArray[1] != "State":

				state = '_'.join(testArray[1].split(' '))
				d,m,y = testArray[0].split('/')
				date = (datetime.datetime(int(y), int(m), int(d), 0, 0).strftime('%s')) + "000000000"
				if testArray[2] != "":
					totalTests = testArray[2] 
				#if testArray[3] != "":
				#	positiveTests = testArray[3]
		
				#postQuery = "{0},detectedstate={1} totalTests={2},positiveTests={3} {4}".format(table,state,totalTests,positiveTests,int(date))				
				postQuery = "{0},detectedstate={1} sampleTestsdone={2} {3}".format(table,state,totalTests,int(date))				
				#print(postQuery)
				influx.Post(db,postQuery)
		except Exception as e:
			print(e)
			sys.exit(1)

##### Fetch data Starts here########
try:
	dataProcess()
	#req = requests.get(url)
	#f req.status_code == 200:
	#	dataProcess(req.text)
except Exception as e:
	print(e)
	sys.exit(1)
