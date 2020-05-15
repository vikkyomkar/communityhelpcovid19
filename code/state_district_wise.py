import sys
import datetime
import subprocess
import requests
import json
import influx

### Variables ####
db=sys.argv[1]
table = 'covid_india'

def state_district_wise(datajson,zonejson):

	color = {'Green' : 1, 'Orange' : 3, 'Red' : 5}
	zoneDict = {}
	for key in zonejson['zones']:
		if key['zone'] != '':
			zoneDict[key['district']] = key['zone']
	for key in datajson.keys():
		try:
			for key2 in datajson[key]['districtData']:
				if key2 in zoneDict.keys():
					zonecode = color[zoneDict[key2]]
				else:
					zonecode = 7

				state = '\ '.join(key.strip().split(' '))
				district = '_'.join(key2.split(' '))
		
				active = abs(datajson[key]['districtData'][key2]['active'])
				confirmed = abs(datajson[key]['districtData'][key2]['confirmed'])
				deceased = abs(datajson[key]['districtData'][key2]['deceased'])
				recovered = abs(datajson[key]['districtData'][key2]['recovered'])
				deltaconfirmed = abs(datajson[key]['districtData'][key2]['delta']['confirmed'])
				deltadeaths = abs(datajson[key]['districtData'][key2]['delta']['deceased'])
				deltarecovered =  abs(datajson[key]['districtData'][key2]['delta']['recovered'])
				postQuery = '{0},state={1},district={2} district=\"{3}\",dactive={4},dconfirmed={5},ddeaths={6},drecovered={7},ddeltaconfirmed={8},ddeltadeaths={9},ddeltarecovered={10},zone={11}'.format(table,state,district,key2,active,confirmed,deceased,recovered,deltaconfirmed,deltadeaths,deltarecovered,zonecode)
				#print(postQuery)	
				influx.Post(db,postQuery)
		except Exception as e:		
			print(e)
			sys.exit(1)
def main():
	try:
		with open('/mnt/covid/code/districtZone') as f1:
			zonejson = json.load(f1)

		with open('/mnt/covid/code/state_district_wise') as f2:
			datajson = json.load(f2)

		state_district_wise(datajson,zonejson)
	except Exception as e:
		print(e)
		sys.exit(1)

if __name__ == "__main__":
	main() 
