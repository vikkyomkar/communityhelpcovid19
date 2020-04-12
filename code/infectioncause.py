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

medicalStaff = ['doctor','compounder','nurse','health worker','private hospital','hospital staff']
familyTransmission = ['family','husband','wife','daughter','father','mother','siblings','son','spouse','close contact']
localTransmission = [ 'relative','neighbour','no travel history','friend','teacher','car','contact transmission','local transmission','domestic worker','no history of travel','locally transmitted','tenant','contact','work','passenger','cab driver']
travelAbroad = ['wuhan','austria','italy','Dubai','iran','thailand','malaysia','oman','foreign','us','london','japan','greece','saudi','qatar','france','philippines','spain','russia','netherlands','middle east','uae','united kingdom','indonesia','turkey','germany','dublin','ireland','mexico','finland','portugal','scotland','singapore','sweden','denmark','abroad','baharain','australia']

causeDict = {'medicalStaff' : 0, 'familyTransmission':0, 'localTransmission':0,'travelAbroad':0,'delhitravel':0,'domestictravel':0}

for patient in data['raw_data']:
	try:
		flag = 0
		if patient['notes'] != "":
			data=patient['notes'].lower()
			for ele in medicalStaff:
				if ele in data:
					if flag != 1:
						causeDict['medicalStaff'] += 1
						flag = 1

			if flag != 1:	
				for ele in familyTransmission:
					if ele in data:
						if flag != 1:
							causeDict['familyTransmission'] += 1
							flag = 1
			if flag != 1:
				for ele in localTransmission:
					if ele in data:
						if flag != 1:
							causeDict['localTransmission'] += 1
							flag = 1
			"""
			if flag != 1:
				for ele in localTransmission:
                                	if ele in data:
                                        	if flag != 1:
							causeDict['localTransmission'] += 1
							flag = 1
			"""
			flag = 0
			for ele in travelAbroad:
				if 'travel' in data and ele in data:
					if flag != 1:
						causeDict['travelAbroad'] += 1
						flag = 1
						
			if 'travel' in data and 'delhi' in data:
				if flag != 1:
					causeDict['delhitravel'] += 1
					flag = 1
			
			if 'travel' in data or 'visit' in data:
				if flag != 1:
					causeDict['domestictravel'] += 1
	except Exception as e:
		print(e)

for k,v in causeDict.items():
	postQuery="{0},infectionType={1} totalinfections={2}".format(table,k,v)
	influx.Post(db,postQuery)	





