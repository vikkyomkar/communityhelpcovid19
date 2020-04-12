import sys
import datetime
import influx

db=sys.argv[1]
table='basicstats'

today = datetime.date.today()
covidStart = datetime.date(2020,1,29) # taken one day before time to get correct data
lockdownStart = datetime.date(2020,3,24) # taken one day before time to get correct data

### Post covidStart days
postQuery = "{0} covidDays={1}".format(table,(today - covidStart).days)
influx.Post(db,postQuery)

### Post lockdownStart Days
postQuery = "{0} lockdownDays={1}".format(table,(today - lockdownStart).days)
influx.Post(db,postQuery)


