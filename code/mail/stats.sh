#!/bin/bash

echo "Starting stats.sh" > misc.statlog
date >> misc.statlog

date > iostat.statlog
#iostat -xh 5 >> iostat.statlog &
iostat -h 5 >> iostat.statlog &

date > vmstat.statlog
vmstat 5 >> vmstat.statlog &

sar 5 0 > sar.statlog &

while [ true ]; do
  uptime >> misc.statlog
  free -m >> misc.statlog
  #ps aux | grep dovecot >> misc.statlog
  ps auxww|awk '$1 ~ /dovecot/ || $11 ~ /(pop|imap)/' >> misc.statlog
  echo "-----" >> misc.statlog
  sleep 5
done
