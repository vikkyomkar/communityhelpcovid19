import sys
import datetime
import subprocess
import requests
import json
import influx


### Variables ####
influxPost = "curl -i -XPOST 'http://localhost:8086/write?db=covid' --data-binary "
db=sys.argv[1]
table = 'covid_india'

def statesGraphData(datajson,states_code_mapping):
	month = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May': '05', 'Jun': '06'}
	state_dict = {}
	try:
		for key in datajson['states_daily']:
			date = key.pop('date')
			status = key.pop('status')
			#temp[status] = key
			if date not in state_dict.keys():
				state_dict[date] = {}
			state_dict[date][status] = key

	#print (state_dict.keys())

	#print (states_code_mapping['states']['ct'])
		for state in states_code_mapping['states']:
			for date in state_dict:
				y = 2020
				d ,m, year = date.strip().split('-')
				announcedate = (datetime.datetime(int(y), int(month[m]), int(d), 0, 0).strftime('%s')) + "000000000"

				statename = '_'.join(states_code_mapping['states'][state].split(' '))
				if state_dict['16-Mar-20']['Confirmed']['mp'] == '':
					state_dict['16-Mar-20']['Confirmed']['mp'] = 0
				activeIndicator = int(state_dict[date]['Confirmed'][state]) - int(state_dict[date]['Recovered'][state]) - int(state_dict[date]['Deceased'][state])
				#print (date, state, state_dict[date]['Confirmed'][state],state_dict[date]['Recovered'][state],state_dict[date]['Deceased'][state], activeIndicator)
				postQuery = "{0},state={1} sgconfirmed={2},sgrecovered={3},sgdeaths={4},sgactiveindicator={5} {6}".format(table,statename,state_dict[date]['Confirmed'][state],state_dict[date]['Recovered'][state],state_dict[date]['Deceased'][state], activeIndicator ,announcedate)
				print(postQuery)
				#influx.Post(db,postQuery)
	except Exception as e:
		print(e)
		sys.exit(1)

def main():
	try:
		with open('states_code_mapping') as f1:
			states_code_mapping = json.load(f1)

		with open('states') as f:
			datajson = json.load(f)

			statesGraphData(datajson,states_code_mapping)
	except Exception as e:
		print(e)
		sys.exit(1)

if __name__ == "__main__":
	main()
