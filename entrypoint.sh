#!/bin/sh
echo "Starting server..."
twistd -noy /reference_manager/biblib/services/jsonrpc_service.tac -l /logs/server.log
