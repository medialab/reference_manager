#!/bin/bash

env=$1
path=$2

if [ -z "$env" ]; then
  exit 1
fi
echo $path $env
#source `which virtualenvwrapper.sh`
#workon $envname
if [ -f $path/twistd.pid ]
then
	kill `cat $path/twistd.pid`
fi
${env} twistd -noy ${path}/biblib/services/jsonrpc_service.tac -l server.log &
exit 0
