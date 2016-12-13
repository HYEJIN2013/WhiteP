#!/bin/sh

app="/path/to/app"
pid_file="$app/shared/pids/qc.pid"

if [ "$1" == "start" ]; then
  if [ ! -e "$pid_file" ]; then
    cd $app/current && RAILS_ENV=production bundle exec rake qc:work &
    touch $pid_file && echo "$!" > $pid_file
  else
    echo "Process seems to be running. Please make sure it is not and restart manually or delete the pid file and try again"
  fi
fi

if [ "$1" == "stop" ]; then
  if [ -e "$pid_file" ]; then
    kill -s SIGKILL $(cat "$pid_file")
    rm $pid_file
  else
    echo "No PID file found"
  fi
fi
