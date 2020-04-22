import influx
db="sitedata"
table='stats'

FH = open('/mnt/covid/routineJobs/sitestats/traffic.txt','r')
traffic = 0
for line in FH:
	try:
		if "website-stats" not in line:
			if "hotspot-areas" in line or "states-data" in line or "covid19-national-stats" in line:
				traffic += 1
			elif "/api/dashboards" in line or "/api/annotations" in line or "path=/ " in line:
				traffic += 1

			#if "/api/dashboards" in line or "path=/ " in line or "path=/d/" in line or "/api/annotations" in line:
			#	traffic += 1

	except Exception as e:
		print(e)
FH.close()
### Save data
print("Total site traffic --- {0}".format(traffic))
postQuery = "{0} sitetraffic={1}".format(table,traffic)
influx.Post(db,postQuery)
