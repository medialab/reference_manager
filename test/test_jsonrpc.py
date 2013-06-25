#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from twisted.internet import reactor
from txjsonrpc.web.jsonrpc import Proxy
import sys


def printValue(value):
    print "Result: %s" % str(value)


def printError(error):
    print ' !! ERROR: ', error


def shutDown(data):
    print "Shutting down reactor..."
    reactor.stop()


proxy = Proxy("http://127.0.0.1:8080/")
if len(sys.argv) > 2 and sys.argv[2] == "array":
    print sys.argv[1], [a for a in sys.argv[3:]]
    d = proxy.callRemote(sys.argv[1], [a for a in sys.argv[3:]])
else:
    print sys.argv[1], sys.argv[2:]
    d = proxy.callRemote(sys.argv[1], *sys.argv[2:])
d.addCallback(printValue).addErrback(printError)
d.addCallback(shutDown)
reactor.run()

# usage :
# python test_jsonrpc.py echo coucou
