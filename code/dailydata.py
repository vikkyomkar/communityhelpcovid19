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
	month = {'January' : '01', 'February' : '02', 'March' : '03', 'April' : '04'}
	for key in datajson['cases_time_series']:
		try:
			y = 2020	
			d ,m = key['date'].strip().split(' ')
			announcedate = (datetime.datetime(int(y), int(month[m]), int(d), 0, 0).strftime('%s')) + "000000000"
			dailyactive = int(key['dailyconfirmed']) - int(key['dailyrecovered']) - int(key['dailydeceased'])
			postQuery = "{0} dailyactive={1},dailyrecovered={2},dailydeceased={3} {4}".format(table,dailyactive,key['dailyrecovered'],key['dailydeceased'],announcedate)
			#print(postQuery)
			influx.Post(db,postQuery)
		except Exception as e:
			print(e)
			sys.exit(1)

def main():
	try:
		with open('/mnt/covid/dailydata') as f:
			datajson = json.load(f)
			totalTests(datajson)
			dailyCases(datajson)
	except Exception as e:
		print(e)
		sys.exit(1)

if __name__ == "__main__":
	main() 
