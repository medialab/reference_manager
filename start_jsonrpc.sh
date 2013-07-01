#!/bin/bash

source `which virtualenvwrapper.sh`
workon AIMEPROD
cd /var/opt/biblib/reference_manager/biblib/services/
if [ -f /var/opt/biblib/reference_manager/biblib/services/twistd.pid ]
then
	kill `cat /var/opt/biblib/reference_manager/biblib/services/twistd.pid`
fi
twistd -noy /var/opt/biblib/reference_manager/biblib/services/jsonrpc_service.tac -l server.log &
deactivate
exit 0
