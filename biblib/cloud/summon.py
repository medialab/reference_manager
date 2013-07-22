#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# https://gist.github.com/chtran/1995150

"""
Search Summon API with Python.
See Dough Chesnut's Code4Lib mailing list post: http://serials.infomotions.com/code4lib/archive/2010/201010/2408.html
"""
import httplib2
import urllib
from datetime import datetime
import hmac
import base64
import hashlib
from biblib.services import config_service
from biblib.util import jsonbson


config = config_service.config["summon"]


def summon_headers(query_string):
    accept = "application/json"
    summon_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    query_sorted = "&".join(sorted(query_string.split('&')))
    query_sorted = urllib.unquote_plus(query_sorted)

    constructed_id = accept + "\n" + summon_date + "\n" + config["host"].encode("utf-8") + "\n" + config["path"].encode("utf-8") + "\n" + query_sorted + "\n"
    constructed_id_digest = base64.encodestring(hmac.new(config["secret_key"].encode("utf-8"), constructed_id, hashlib.sha1).digest())

    authorization = "Summon " + config["access_id"] + ';' + constructed_id_digest
    authorization = authorization.replace('\n', '')

    return {"Host": config["host"],
            "Accept": accept,
            "x-summon-date": summon_date,
            "Authorization": authorization}


def summon_query(query_string):
    url = "http://%s%s?%s" % (config["host"], config["path"], query_string)
    headers = summon_headers(query_string)
    print headers

    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers=headers)
    print response
    print content
    result = jsonbson.load_json_str(content)
    print jsonbson.dumps_json(result, True)
    return result
