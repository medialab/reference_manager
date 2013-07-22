#!/bin/bash

envname=$1

if [ -z "$envname" ]; then
  exit 1
fi
echo $envname
source `which virtualenvwrapper.sh`
workon $envname
if [ -f twistd.pid ]
then
	kill `cat twistd.pid`
fi
twistd -noy biblib/services/jsonrpc_service.tac -l server.log &
deactivate
exit 0
