#!/bin/sh

#* * * * * python /mnt/covid/sitedata.py
#*/30 04-17 * * * sh  /mnt/covid/wrapper.sh >> /var/log/covid.log
#27 18 * * * sh  /mnt/covid/wrapper.sh >> /var/log/covid.log


exitCode=0
db="covid"
db+=`date +'%m%d%H%M'`

rawdataUrl="https://api.covid19india.org/raw_data.json"
dailydata="https://api.covid19india.org/data.json"

####### Create DB #########
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE ${db}"
out=`echo $?`
exitCode=`expr ${exitCode} + ${out}`

####### Get basic stats #########
python /mnt/covid/basicstats.py ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
	echo "Basic stats data collection failed"
fi
exitCode=`expr ${exitCode} + ${out}`

###### Death and recover #########
python /mnt/covid/recoveredDeceased.py ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
        echo "Recover and Deceased data collection failed"
fi

exitCode=`expr ${exitCode} + ${out}`

##### Get raw data #########
curl ${rawdataUrl} > /mnt/covid/rawdata
if [[ `echo $?` != 0 ]];then
        echo "failed"
fi
python /mnt/covid/rawdata.py  ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
        echo "Main data collection failed"
fi
exitCode=`expr ${exitCode} + ${out}`
python /mnt/covid/infectioncause.py ${db}

###### Get daily data #########
curl ${dailydata} > /mnt/covid/dailydata
if [[ `echo $?` != 0 ]];then
        echo "failed"
fi
python /mnt/covid/dailydata.py ${db}
out=`echo $?`
if [[ ${out} != 0 ]];then
        echo "daily trend data collection failed"
fi
exitCode=`expr ${exitCode} + ${out}`

##### Get daily sample test data #############
python /mnt/covid/sampleTestingDdata.py  ${db}
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

