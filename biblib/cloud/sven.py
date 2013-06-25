#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
import urllib
import urllib2
from biblib.util import config_service


config = config_service.config["sven"]

DOCUMENTS = "document/"
AUTHENTICATE = "authenticate/"


def authenticate(username, password):
    print "\n" + AUTHENTICATE
    data = {"username": username, "password": password}
    data_encoded = urllib.urlencode(data)
    url = config["endpoint"] + AUTHENTICATE
    print url
    request = urllib2.Request(url, data_encoded)
    response = urllib2.urlopen(request)
    result = json.loads(response.read())
    print result
    auth_dict = {"token": result["token"], "user_id": username}
    return auth_dict


def document(item):
    print "\n" + DOCUMENTS
    url = config["endpoint"] + DOCUMENTS
    print url
    print item
    if "tags" in item:
        tags = json.dumps(item["tags"])
        del item["tags"]
        print tags
        item["tags"] = tags
    params_encoded = urllib.urlencode(item)
    print params_encoded
    request = urllib2.Request(url, params_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    print result
    return json.loads(result)
    try:
        pass
    except:
        print "*** Error uploading item to sven : %s" % item["title"]
        return {"status": "error"}
