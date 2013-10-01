#!/bin/bash

# usage:
# path = /var/opt/biblib/reference_manager
# env = /home/someone/.virtualenv/BIBLIB/bin/
# $path/start_jsonrpc.sh $env $path

# AIME usage:
# dev: /home/jra/reference_manager/start_jsonrpc.sh /home/jra/.virtualenv/AIME/bin/ /home/jra/reference_manager/
# prodv2: /var/opt/biblib/reference_manager/start_jsonrpc.sh /home/jra/.virtualenv/AIMEPROD/bin/ /var/opt/biblib/reference_manager/
# prodv3: /var/opt/biblib/prod_v3/start_jsonrpc.sh /home/jra/.virtualenv/AIMEPROD/bin/ /var/opt/biblib/prod_v3/

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
