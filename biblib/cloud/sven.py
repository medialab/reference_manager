#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import urllib
import urllib2
from biblib.util import config_service
from biblib.util import jsonbson

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
    result = jsonbson.load_json_str(response.read())
    print result
    auth_dict = {"token": result["token"], "user_id": username}
    return auth_dict


def document(item):
    print "\n" + DOCUMENTS
    url = config["endpoint"] + DOCUMENTS
    print url
    print item
    if "tags" in item:
        tags = jsonbson.dumps_json(item["tags"])
        del item["tags"]
        print tags
        item["tags"] = tags
    params_encoded = urllib.urlencode(item)
    print params_encoded
    request = urllib2.Request(url, params_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    print result
    return jsonbson.load_json_str(result)
    try:
        pass
    except:
        print "*** Error uploading item to sven : %s" % item["title"]
        return {"status": "error"}
