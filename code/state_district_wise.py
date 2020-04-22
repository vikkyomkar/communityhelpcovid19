import sys
import datetime
import subprocess
import requests
import json
import influx

### Variables ####
db=sys.argv[1]
table = 'covid_india'

def state_district_wise(datajson):
	state_dict = {'Jammu_and_Kashmir' : 'Jammu_Kashmir', 'Dadra_and_Nagar_Haveli' : 'Dadra_Nagar_Haveli', 'Andaman_and_Nicobar_Islands' : 'Andaman_Nicobar'}
	for key in datajson.keys():
		try:
			for key2 in datajson[key]['districtData']:
				statename = '_'.join(key.split(' '))   
				if statename in state_dict.keys():
                                        state = state_dict[statename]
                                else:
                                        state = statename

				district = '_'.join(key2.split(' '))
		
				active = datajson[key]['districtData'][key2]['active']
				confirmed = datajson[key]['districtData'][key2]['confirmed']
				deceased = datajson[key]['districtData'][key2]['deceased']
				recovered = datajson[key]['districtData'][key2]['recovered']
				deltaconfirmed = datajson[key]['districtData'][key2]['delta']['confirmed']
				deltadeaths = datajson[key]['districtData'][key2]['delta']['deceased']
				deltarecovered =  datajson[key]['districtData'][key2]['delta']['recovered']

				postQuery = "{0},state={1},district={2} dactive={3},dconfirmed={4},ddeaths={5},drecovered={6},ddeltaconfirmed={7},ddeltadeaths={8},ddeltarecovered={9}".format(table,state,district,active,confirmed,deceased,recovered,deltaconfirmed,deltadeaths,deltarecovered)
				
				influx.Post(db,postQuery)
		except Exception as e:		
			print(e)
			sys.exit(1)
def main():
	try:
		with open('/mnt/covid/code/state_district_wise') as f:
			datajson = json.load(f)
			state_district_wise(datajson)
	except Exception as e:
		print(e)
		sys.exit(1)

if __name__ == "__main__":
	main() 
