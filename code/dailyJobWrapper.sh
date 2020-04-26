#!/bin/sh

#
# Flush the table before running it
#


exitCode=0
db="covid_static"

rawdataUrl="https://api.covid19india.org/raw_data.json"
deathRecoverdata="https://api.covid19india.org/csv/latest/death_and_recovered.csv"
###### Death and recover #########
#curl ${deathRecoverdata} > /mnt/covid/code/deathRecoverdata
#if [[ `echo $?` != 0 ]];then
#        echo "failed"
#fi
#python /mnt/covid/code/recoveredDeceased.py ${db}
#out=`echo $?`
#if [[ ${out} != 0 ]];then
#        echo "Recover and Deceased data collection failed"
#fi

#exitCode=`expr ${exitCode} + ${out}`


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

