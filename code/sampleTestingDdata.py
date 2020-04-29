import sys
import datetime
import subprocess
import requests
import json
import influx

### Variables ####
db = sys.argv[1]
table = 'covid_india'

population = {
	"Uttar_Pradesh" : 223897418,
	"Maharashtra" : 124945748,
	"Bihar" : 121741741,
	"West_Bengal" : 98785114,
	"Andhra_Pradesh" : 54000000,
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
	"Jammu_Kashmir" : 14591623,
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

def dataProcess(datajson):
	state_dict = {'Jammu_and_Kashmir' : 'Jammu_Kashmir', 'Dadra_and_Nagar_Haveli' : 'Dadra_Nagar_Haveli', 'Andaman_and_Nicobar_Islands' : 'Andaman_Nicobar'}
	for key in datajson['states_tested_data']:
		try:
			if key['totaltested'] != "":
				statename = '_'.join(key['state'].split(' '))   		
				if statename in state_dict.keys():
					state = state_dict[statename]
				else:
					state = statename
				d,m,y = key['updatedon'].split('/')
				date = (datetime.datetime(int(y), int(m), int(d), 0, 0).strftime('%s')) + "000000000"
				postQuery = "{0},detectedstate={1} sampleTestsdone={2} {3}".format(table,state,key['totaltested'],int(date))
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
