#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import base64
import logging
import urllib
import urllib2

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
    #logging.debug(AUTHENTICATE)
    auth = {"username": username, "password": password}
    auth_encoded = urllib.urlencode(auth)
    url = config["endpoint"] + AUTHENTICATE
    logging.debug(url)
    request = urllib2.Request(url, auth_encoded)
    response = urllib2.urlopen(request)
    result = jsonbson.load_json_str(response.read())
    logging.debug(result)
    anta_auth = {"token": result["token"], "user_id": username}
    return anta_auth


def get_all_action(anta_auth):
    #logging.debug(GETALLACTION)
    auth = {"token": anta_auth["token"]}
    auth_encoded = urllib.urlencode(auth)
    url = config["endpoint_frog"] + GETALLACTION + USER + anta_auth["user_id"]
    logging.debug(url)
    request = urllib2.Request(url, auth_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    return result


def get_documents(anta_auth):
    #logging.debug(GETDOCUMENTS)
    auth = {"token": anta_auth["token"]}
    auth_encoded = urllib.urlencode(auth)
    url = config["endpoint_frog"]+GETDOCUMENTS + USER + anta_auth["user_id"]
    logging.debug(url)
    request = urllib2.Request(url, auth_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    logging.debug(result)
    return result


def item_upload(anta_auth, item):
    #logging.debug(ITEMUPLOAD)
    url = config["endpoint"] + ITEMUPLOAD + USER + anta_auth["user_id"]
    logging.debug(url)
    logging.debug(item)
    item_serialize = phpserialize.serialize(item)
    item_base64 = base64.b64encode(item_serialize)
    auth = {"token": anta_auth["token"], "item": item_base64}
    auth_encoded = urllib.urlencode(auth)
    request = urllib2.Request(url, auth_encoded)
    try:
        response = urllib2.urlopen(request)
        result = response.read()
        logging.debug(result)
        return jsonbson.load_json_str(result)
    except:
        logging.debug("*** Error uploading item to anta : %s", item["title"])
        return {"status": "ko"}


def full_text(anta_auth, doc_id):
    #logging.debug(FULLTEXT)
    auth = {"token": anta_auth["token"], "document": doc_id}
    auth_encoded = urllib.urlencode(auth)
    url = config["endpoint_frog"] + FULLTEXT + USER + anta_auth["user_id"]
    logging.debug(url)
    request = urllib2.Request(config["endpoint_frog"] + FULLTEXT + USER + anta_auth["user_id"], auth_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    logging.debug(result)
    return result



#anta_auth = authenticate(config["username"], config["password"])
#logging.debug(get_all_action(anta_auth))
#logging.debug(get_documents(anta_auth))
#logging.debug(full_text(anta_auth, "22"))

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


#logging.debug(item_upload(anta_auth, item))
