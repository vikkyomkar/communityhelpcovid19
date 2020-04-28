#!/bin/sh

#
# Flush the table before running it
#


exitCode=0
db="covid_static"

rawfiles=("data1"  "data2" "data3")

for i in "${rawfiles[@]}"
do
	curl https://api.covid19india.org/raw_${i}.json > ${i}
	python /mnt/covid/code/rawdata/rawDataProcessor.py  ${i} ${db}
done
