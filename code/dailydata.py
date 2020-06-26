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
#latestDay = ""

def totalTests(datajson):
	yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%d/%m")
	for key in datajson['tested']:
		try:
			if key['totalsamplestested'] != "": #if yesterday in key['updatetimestamp']:
				postQuery = "{0} totalsamplestested={1}".format(table,key['totalsamplestested'])
				#print(postQuery)
				influx.Post(db,postQuery)
		except Exception as e:
			print(e)
			sys.exit(1)		

def dailyCases(datajson):
	month = {'January' : '01', 'February' : '02', 'March' : '03', 'April' : '04', 'May': '05', 'June': '06'}
	for key in datajson['cases_time_series']:
		try:
			y = 2020	
			d ,m = key['date'].strip().split(' ')
			#latestDay = "{0}/{1}/{2}".format(d,month[m],y)
			announcedate = (datetime.datetime(int(y), int(month[m]), int(d), 0, 0).strftime('%s')) + "000000000"
			totalactive = int(key['totalconfirmed']) - int(key['totalrecovered']) - int(key['totaldeceased'])
			postQuery = "{0} dailyconfirmed={1},dailyrecovered={2},dailydeceased={3},totalconfirmed={4},totalactive={5},totalrecovered={6},totaldeceased={7} {8}".format(table,key['dailyconfirmed'],key['dailyrecovered'],key['dailydeceased'],key['totalconfirmed'],totalactive,key['totalrecovered'],key['totaldeceased'],announcedate)
			#print(postQuery)
			influx.Post(db,postQuery)
		except Exception as e:
			print(e)
			sys.exit(1)

def statewise(datajson):
	state_dict = {'Jammu_and_Kashmir' : 'Jammu_Kashmir', 'Dadra_and_Nagar_Haveli' : 'Dadra_Nagar_Haveli', 'Andaman_and_Nicobar_Islands' : 'Andaman_Nicobar'}
	for key in datajson['statewise']:
		try:
			if key['state'] != 'Total':
				state = '\ '.join(key['state'].strip().split(' '))

				if int(key['deltadeaths']) < 0:
					key['deltadeaths'] = 0
					print(key['deltadeaths'])

				if int(key['deltaconfirmed']) != 0 or int(key['deltarecovered']) != 0 or int(key['deltadeaths']) != 0:
					if int(key['deltaconfirmed']) > 0:
						postQuery = "{0},state={1} homedeltaconfirmed={2},homedeltadeaths={3},homedeltarecovered={4}".format(table,state,key['deltaconfirmed'],key['deltadeaths'],key['deltarecovered'])
						influx.Post(db,postQuery)
						#print(postQuery)
				if key['state'] == 'Delhi':
					postQuery = "{0},state={1},district=Delhi district=\"{2}\",ddeltaconfirmed={3},ddeltadeaths={4},ddeltarecovered={5},sactive={6},sconfirmed={7},sdeaths={8},srecovered={9},sdeltaconfirmed={10},sdeltadeaths={11},sdeltarecovered={12},dactive={13},drecovered={14},ddeaths={15}".format(table,state,'Delhi',key['deltaconfirmed'],key['deltadeaths'],key['deltarecovered'],key['active'],key['confirmed'],key['deaths'],key['recovered'],key['deltaconfirmed'],key['deltadeaths'],key['deltarecovered'],key['active'],key['recovered'],key['deaths'])
					#print(postQuery)
					influx.Post(db,postQuery)
				else:
					postQuery = "{0},state={1} sactive={2},sconfirmed={3},sdeaths={4},srecovered={5},sdeltaconfirmed={6},sdeltadeaths={7},sdeltarecovered={8}".format(table,state,key['active'],key['confirmed'],key['deaths'],key['recovered'],key['deltaconfirmed'],key['deltadeaths'],key['deltarecovered'])
					influx.Post(db,postQuery)

				### put data for state graph
				y = 2020
				d = int(datetime.datetime.now().day)
				m = int(datetime.datetime.now().month)
				announcedate = (datetime.datetime(int(y), int(m), int(d), 0, 0).strftime('%s')) + "000000000"
				activeindicator = int(key['deltaconfirmed']) - int(key['deltadeaths']) - int(key['deltarecovered'])
				postQuery = "{0},state={1} sgconfirmed={2},sgrecovered={3},sgdeaths={4},sgactiveindicator={5} {6}".format(table,state,key['deltaconfirmed'],key['deltarecovered'],key['deltadeaths'],activeindicator,announcedate)
				influx.Post(db,postQuery)
			else:
				y = 2020
				d , m, rest = key['lastupdatedtime'].strip().split('/')
				announcedate = (datetime.datetime(int(y), int(m), int(d), 0, 0).strftime('%s')) + "000000000"

                                postQuery = "{0} dailyconfirmed={1},dailyrecovered={2},dailydeceased={3},totalconfirmed={4},totalactive={5},totalrecovered={6},totaldeceased={7} {8}".format(table,key['deltaconfirmed'],key['deltarecovered'],key['deltadeaths'],key['confirmed'],key['active'],key['recovered'],key['deaths'],announcedate)
                                influx.Post(db,postQuery)
				#print(postQuery)
		except Exception as e:		
			print(e)
			sys.exit(1)
def main():
	try:
		with open('/mnt/covid/code/dailydata') as f:
			datajson = json.load(f)
			totalTests(datajson)
			statewise(datajson)
			dailyCases(datajson)
	except Exception as e:
		print(e)
		sys.exit(1)

if __name__ == "__main__":
	main() 
