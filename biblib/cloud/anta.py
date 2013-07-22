#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import urllib
import urllib2
import base64
import phpserialize
from biblib.services import config_service
from biblib.util import jsonbson


config = config_service.config["anta"]

# ANTA PATH
USER = "/user/"
AUTHENTICATE = "authenticate"
ITEMUPLOAD = "item-upload"
GETDOCUMENTS = "get-documents"
GETALLACTION = "get-all-action"
FULLTEXT = "full-text"


def authenticate(username, password):
    print "\n" + AUTHENTICATE
    auth = {"username": username, "password": password}
    auth_encoded = urllib.urlencode(auth)
    url = config["endpoint"] + AUTHENTICATE
    print url
    request = urllib2.Request(url, auth_encoded)
    response = urllib2.urlopen(request)
    result = jsonbson.load_json_str(response.read())
    print result
    anta_auth = {"token": result["token"], "user_id": username}
    return anta_auth


def get_all_action(anta_auth):
    print "\n" + GETALLACTION
    auth = {"token": anta_auth["token"]}
    auth_encoded = urllib.urlencode(auth)
    url = config["endpoint_frog"] + GETALLACTION + USER + anta_auth["user_id"]
    print url
    request = urllib2.Request(url, auth_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    print result


def get_documents(anta_auth):
    print "\n" + GETDOCUMENTS
    auth = {"token": anta_auth["token"]}
    auth_encoded = urllib.urlencode(auth)
    url = config["endpoint_frog"]+GETDOCUMENTS + USER + anta_auth["user_id"]
    print url
    request = urllib2.Request(url, auth_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    print result
    return result


def item_upload(anta_auth, item):
    print "\n" + ITEMUPLOAD
    url = config["endpoint"] + ITEMUPLOAD + USER + anta_auth["user_id"]
    print url
    print item
    item_serialize = phpserialize.serialize(item)
    item_base64 = base64.b64encode(item_serialize)
    auth = {"token": anta_auth["token"], "item": item_base64}
    auth_encoded = urllib.urlencode(auth)
    request = urllib2.Request(url, auth_encoded)
    try:
        response = urllib2.urlopen(request)
        result = response.read()
        print result
        return jsonbson.load_json_str(result)
    except:
        print "*** Error uploading item to anta : %s" % item["title"]
        return {"status": "ko"}


def full_text(anta_auth, doc_id):
    print "\n" + FULLTEXT
    auth = {"token": anta_auth["token"], "document": doc_id}
    auth_encoded = urllib.urlencode(auth)
    url = config["endpoint_frog"] + FULLTEXT + USER + anta_auth["user_id"]
    print url
    request = urllib2.Request(config["endpoint_frog"] + FULLTEXT + USER + anta_auth["user_id"], auth_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    print result
    return result



#anta_auth = authenticate(config["username"], config["password"])
#print get_all_action(anta_auth)
#print get_documents(anta_auth)
#print full_text(anta_auth, "22")

#item = {}
#item["title"] = "test biblib"
#item["language"] = "en"
#item["content"] = "raw utf8"
#item["ref_url"] = "http://www.example.org/test.txt"
#item["mimetype"] = "text/plain"
#item["date"] = "2013-01-01 00:00:00"
#metadata = {}
#metadata["author"] = ["Author A", "Author B"]
#metadata["institution"] = ["Institution A"]


#print item_upload(anta_auth, item)
