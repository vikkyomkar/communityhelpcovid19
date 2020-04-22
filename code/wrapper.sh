#!/bin/sh

#* * * * * python /mnt/covid/sitedata.py
#*/30 04-17 * * * sh  /mnt/covid/wrapper.sh >> /var/log/covid.log
#27 18 * * * sh  /mnt/covid/wrapper.sh >> /var/log/covid.log


exitCode=0
db="covid"
db+=`date +'%m%d%H%M'`

rawdataUrl="https://api.covid19india.org/raw_data.json"
dailydata="https://api.covid19india.org/data.json"
sampledata="https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv"
deathRecoverdata="https://api.covid19india.org/csv/latest/death_and_recovered.csv"
districtdata="https://api.covid19india.org/state_district_wise.json"
####### Create DB #########
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE ${db}"
out=`echo $?`
exitCode=`expr ${exitCode} + ${out}`

####### Get basic stats #########
python /mnt/covid/code/basicstats.py ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
	echo "Basic stats data collection failed"
fi
exitCode=`expr ${exitCode} + ${out}`

###### Death and recover #########
curl ${deathRecoverdata} > /mnt/covid/code/deathRecoverdata
if [[ `echo $?` != 0 ]];then
        echo "failed"
fi
python /mnt/covid/code/recoveredDeceased.py ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
        echo "Recover and Deceased data collection failed"
fi

exitCode=`expr ${exitCode} + ${out}`


##### Get raw data #########
curl ${rawdataUrl} > /mnt/covid/code/rawdata
if [[ `echo $?` != 0 ]];then
        echo "failed"
fi
python /mnt/covid/code/rawdata.py  ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
        echo "Main data collection failed"
fi
exitCode=`expr ${exitCode} + ${out}`
python /mnt/covid/code/infectioncause.py ${db}

###### Get daily data #########
curl ${dailydata} > /mnt/covid/code/dailydata
if [[ `echo $?` != 0 ]];then
        echo "failed"
fi
python /mnt/covid/code/dailydata.py ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
        echo "daily trend data collection failed"
fi
exitCode=`expr ${exitCode} + ${out}`
###### Get District data #########
curl ${districtdata} > /mnt/covid/code/state_district_wise
if [[ `echo $?` != 0 ]];then
        echo "failed"
fi
python /mnt/covid/code/state_district_wise.py ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
        echo "District data collection failed"
fi
exitCode=`expr ${exitCode} + ${out}`
##### Get daily sample test data #############
curl ${sampledata} > /mnt/covid/code/sampletestdata
if [[ `echo $?` != 0 ]];then
        echo "failed"
fi
python /mnt/covid/code/sampleTestingDdata.py  ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
        echo "daily sample tests data collection failed"
fi
exitCode=`expr ${exitCode} + ${out}`
##### Check and update DB #######
if [[ ${exitCode} == 0 ]];then
	echo "All Jobs executed successfully"
	curl -X PUT -u admin:admin -H 'Content-Type: application/json;charset=UTF-8' \
	 --data-binary "{\"name\":\"InfluxDB\",\"type\":\"influxdb\",\"url\":\"http://localhost:8086\",\"access\":\"proxy\",\"database\":\"${db}\",\"user\":\"\",\"password\":\"\"}" \
	  http://localhost/api/datasources/1
else
	echo "Send failure email"

fi
