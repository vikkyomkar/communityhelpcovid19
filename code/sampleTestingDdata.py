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
	"Telangana" : 37220000,
        "Uttar Pradesh" : 223897418,
        "Maharashtra" : 124945748,
        "Bihar" : 121741741,
        "West Bengal" : 98785114,
        "Andhra Pradesh" : 54000000,
        "Madhya Pradesh" : 82961852,
        "Tamil Nadu" : 80288487,
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
        "Jammu and Kashmir" : 14591623,
        "Uttarakhand" : 11453488,
        "Himachal Pradesh" : 7234695,
        "Tripura" : 3914581,
        "Meghalaya" : 3257373,
        "Nagaland" : 2063533,
        "Goa" : 1562488,
        "Arunachal Pradesh" : 1511873,
        "Mizoram" : 1156288,
        "Delhi" : 16787941,
        "Chandigarh" : 1249223,
        "Ladakh" : 133487
}

for k,v in population.items():
	state = '\ '.join(k.split(' '))
	postQuery = "{0},state={1} population={2}".format(table,state,v)
	#print(postQuery)
	influx.Post(db,postQuery)

def dataProcess(datajson):
	#state_dict = {'JammuandKashmir' : 'JammuKashmir', 'DadraandNagarHaveli' : 'DadraNagarHaveli', 'AndamanandNicobarIslands' : 'AndamanNicobar'}
	state_dict = {'Jammu_and_Kashmir' : 'Jammu_Kashmir', 'Dadra_and_Nagar_Haveli' : 'Dadra_Nagar_Haveli', 'Andaman_and_Nicobar_Islands' : 'Andaman_Nicobar'}
	for key in datajson['states_tested_data']:
		try:
			if key['totaltested'] != "":
				#statename = '_'.join(key['state'].split(' '))   		
				#statename = ''.join(key['state'].split(' '))   		
				#if statename in state_dict.keys():
				#	state = state_dict[statename]
				#else:
				#	state = statename
				state = '\ '.join(key['state'].strip().split(' '))
			
				d,m,y = key['updatedon'].split('/')
				date = (datetime.datetime(int(y), int(m), int(d), 0, 0).strftime('%s')) + "000000000"
				postQuery = "{0},state={1} sampleTestsdone={2} {3}".format(table,state,key['totaltested'],int(date))
				influx.Post(db,postQuery)	
		except Exception as e:
			print(e)
			sys.exit(1)

##### Fetch data Starts here########
try:
	with open('/mnt/covid/code/sampletestdata') as f:
		datajson = json.load(f)
		dataProcess(datajson)

except Exception as e:
	print(e)
	sys.exit(1)
