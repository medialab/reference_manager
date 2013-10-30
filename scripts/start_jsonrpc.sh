#!/bin/bash

# usage:
# path = /somewhere/biblib
# env = /home/someone/.virtualenv/BIBLIB/bin/
# $path/scripts/start_jsonrpc.sh $env $path

# AIME usage:
# dev: /home/jra/reference_manager/scripts/start_jsonrpc.sh /home/jra/.virtualenv/AIME/bin/ /home/jra/reference_manager
# prodv4: /var/opt/biblib/prod_v4/scripts/start_jsonrpc.sh /home/jra/.virtualenv/AIMEPROD/bin/ /var/opt/biblib/prod_v4

# Fronccast usage:
# frontcast: /store/opt/biblib/scripts/start_jsonrpc.sh /home/biblib/.virtualenvs/BIBLIB/bin/ /store/opt/biblib

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
cd $path
${env}twistd -noy ${path}/biblib/services/jsonrpc_service.tac -l ${path}/log/server.log &
exit 0
