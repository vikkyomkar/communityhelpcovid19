#!/bin/sh
date=`date +'%Y-%m-%dT%H:%M' --date='1 minutes ago'`
grep "path=" /var/log/grafana/grafana.log |grep ${date} >/mnt/covid/routineJobs/sitestats/traffic.txt
python /mnt/covid/routineJobs/sitestats/sitestats.py
