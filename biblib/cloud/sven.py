#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import urllib
import urllib2
from biblib.util import config_service
from biblib.util import jsonbson

config = config_service.config["sven"]

DOCUMENTS = "document/"
AUTHENTICATE = "authenticate/"


def authenticate(username, password):
    logging.debug(AUTHENTICATE)
    data = {"username": username, "password": password}
    data_encoded = urllib.urlencode(data)
    url = config["endpoint"] + AUTHENTICATE
    logging.debug(url)
    request = urllib2.Request(url, data_encoded)
    response = urllib2.urlopen(request)
    result = jsonbson.load_json_str(response.read())
    logging.debug(result)
    auth_dict = {"token": result["token"], "user_id": username}
    return auth_dict


def document(item):
    logging.debug(DOCUMENTS)
    url = config["endpoint"] + DOCUMENTS
    logging.debug(url)
    logging.debug(item)
    if "tags" in item:
        tags = jsonbson.dumps_json(item["tags"])
        del item["tags"]
        logging.debug(tags)
        item["tags"] = tags
    params_encoded = urllib.urlencode(item)
    logging.debug(params_encoded)
    request = urllib2.Request(url, params_encoded)
    response = urllib2.urlopen(request)
    result = response.read()
    logging.debug(result)
    return jsonbson.load_json_str(result)
    try:
        pass
    except:
        logging.error("*** Error uploading item to sven : {}".format(item["title"]))
        return {"status": "error"}
