import sys
import json
import datetime
import subprocess
import influx

### Variables ####
db = sys.argv[1] 
table = "covid_india"

with open('/mnt/covid/code/rawdata') as f:
	data = json.load(f)

MedicalStaff = ['doctor','compounder','nurse','health worker','private hospital','hospital staff']
FamilyTransmission = ['family','husband','wife','daughter','father','mother','siblings','son','spouse','close contact']
LocalTransmission = [ 'relative','neighbour','no travel history','friend','teacher','car','contact transmission','local transmission','domestic worker','no history of travel','locally transmitted','tenant','contact','work','passenger','cab driver']
TravelledAbroad = ['wuhan','austria','italy','Dubai','iran','thailand','malaysia','oman','foreign','us','london','japan','greece','saudi','qatar','france','philippines','spain','russia','netherlands','middle east','uae','united kingdom','indonesia','turkey','germany','dublin','ireland','mexico','finland','portugal','scotland','singapore','sweden','denmark','abroad','baharain','australia']

causeDict = {'MedicalStaff' : 0, 'FamilyTransmission':0, 'LocalTransmission':0,'TravelledAbroad':0,'TravelToDelhi':0,'DomesticTravel':0}

for patient in data['raw_data']:
	try:
		flag = 0
		if patient['notes'] != "":
			data=patient['notes'].lower()
			for ele in MedicalStaff:
				if ele in data:
					if flag != 1:
						causeDict['MedicalStaff'] += 1
						flag = 1

			if flag != 1:	
				for ele in FamilyTransmission:
					if ele in data:
						if flag != 1:
							causeDict['FamilyTransmission'] += 1
							flag = 1
			if flag != 1:
				for ele in LocalTransmission:
					if ele in data:
						if flag != 1:
							causeDict['LocalTransmission'] += 1
							flag = 1
			"""
			if flag != 1:
				for ele in LocalTransmission:
                                	if ele in data:
                                        	if flag != 1:
							causeDict['LocalTransmission'] += 1
							flag = 1
			"""
			flag = 0
			for ele in TravelledAbroad:
				if 'travel' in data and ele in data:
					if flag != 1:
						causeDict['TravelledAbroad'] += 1
						flag = 1
						
			if 'travel' in data and 'delhi' in data:
				if flag != 1:
					causeDict['TravelToDelhi'] += 1
					flag = 1
			
			if 'travel' in data or 'visit' in data:
				if flag != 1:
					causeDict['DomesticTravel'] += 1
	except Exception as e:
		print(e)

for k,v in causeDict.items():
	postQuery="{0},infectionType={1} totalinfections={2}".format(table,k,v)
	influx.Post(db,postQuery)
