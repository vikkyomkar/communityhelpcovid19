#!/bin/bash

python /mnt/covid/hotspots/preparedata.py 
while read line
do
	curl -i -XPOST "http://localhost:8086/write?db=covid_static" --data-binary "${line}"

done < influxdata

