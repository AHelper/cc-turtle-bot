#!/bin/bash

run_rpc() {
  echo -n "$1 "
  if [ "$2" == "" ]; then
    curl http://localhost:34299/$1 -s >OUT
    E=$?
  else
    curl http://localhost:34299/$1 -s -d "$2" >OUT
    E=$?
  fi
  if [ $E != 0 ]; then
    echo "FAILED"
    cat OUT
    echo ""
    rm OUT
    exit 1
  else
    grep "$3" OUT >/dev/null
    E=$?
    if [ $E != 0 ]; then
      echo "FAILED"
      cat OUT
      rm OUT
      echo ""
      exit 1
    else
      echo "OK"
      rm OUT
    fi
  fi
}

echo Registering turtle
run_rpc turtle/1/register '{"x":0,"y":0,"z":0,"facing":0}' success
run_rpc turtle/1/status '' success
run_rpc turtle/1/getAction '' '203'

echo Adding goal
run_rpc goals/add '{"goal":"find new plot"}' success
run_rpc goals '' 'active={find new plot'

echo Running all goal actions
run_rpc turtle/1/getAction '' 'action="explore"'
run_rpc turtle/1/response '{"id":1,"type":"success"}' success
run_rpc turtle/1/getAction '' 'action="discover"'
run_rpc turtle/1/response '{"id":2,"type":"success"}' success
run_rpc turtle/1/getAction '' '203'

echo Adding another goal
run_rpc goals/add '{"goal":"find new plot"}' success
run_rpc goals '' 'active={find new plot'

echo Adding another turtle, verifying this new turtle can\'t be used for this goal
run_rpc turtle/2/register '{"x":0,"y":0,"z":0,"facing":0}' success
run_rpc turtle/2/status '' success
run_rpc turtle/2/getAction '' '203'

echo Running all goals for the first turtle
run_rpc turtle/1/getAction '' 'action="explore"'
run_rpc turtle/1/response '{"id":1,"type":"success"}' success
run_rpc turtle/1/getAction '' 'action="discover"'
run_rpc turtle/1/response '{"id":2,"type":"success"}' success
run_rpc turtle/1/getAction '' '203'