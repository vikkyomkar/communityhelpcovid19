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

	delhi_dactive = 0
	delhi_dconfirmed = 0
	delhi_ddeaths = 0
	delhi_drecovered = 0
	delhi_ddeltaconfirmed = 0
	delhi_ddeltadeaths = 0
	delhi_ddeltarecovered = 0

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


				if state ==  'Delhi':
					delhi_dactive += active
					delhi_dconfirmed += confirmed
					delhi_ddeaths += deceased
					delhi_drecovered += recovered
					delhi_ddeltaconfirmed += deltaconfirmed
					delhi_ddeltadeaths += deltadeaths 
					delhi_ddeltarecovered += deltarecovered
				else:
					postQuery = '{0},state={1},district={2} district=\"{3}\",dactive={4},dconfirmed={5},ddeaths={6},drecovered={7},ddeltaconfirmed={8},ddeltadeaths={9},ddeltarecovered={10},zone={11}'.format(table,state,district,key2,active,confirmed,deceased,recovered,deltaconfirmed,deltadeaths,deltarecovered,zonecode)
					#print(postQuery)	
					influx.Post(db,postQuery)
		except Exception as e:		
			print(e)
			sys.exit(1)
	postQuery = '{0},state={1},district={2} district=\"{3}\",dactive={4},dconfirmed={5},ddeaths={6},drecovered={7},ddeltaconfirmed={8},ddeltadeaths={9},ddeltarecovered={10}'.format(table,'Delhi','Delhi','Delhi',delhi_dactive,delhi_dconfirmed,delhi_ddeaths,delhi_drecovered,delhi_ddeltaconfirmed,delhi_ddeltadeaths,delhi_ddeltarecovered)
	#print(postQuery)
	influx.Post(db,postQuery)

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
