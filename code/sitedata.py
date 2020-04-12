import sys
import os
import datetime
import influx

db="sitedata"
table='stats'

stream = os.popen('grep "action=View" /var/log/grafana/grafana.log |wc -l')
output = stream.read().strip()
### Save data
postQuery = "{0} sitetraffic={1}".format(table,output)
influx.Post(db,postQuery)

