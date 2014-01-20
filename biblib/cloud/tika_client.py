#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import mimetypes
import os
import time
import zipfile
from StringIO import StringIO

import requests

from biblib.crosswalks import tika_crosswalk
from biblib.services import config_service
from biblib.util import console


console.setup_console()
config_tika = config_service.config["tika"]

tika_endpoint = config_tika["endpoint"]
tika_endpoint_all = tika_endpoint + "all"
tika_endpoint_meta = tika_endpoint + "meta"
tika_endpoint_text = tika_endpoint + "tika"

# First, start the tika REST server
# tika-rest-server
# Examples:
# curl -T test.pdf http://localhost:9998/meta
# curl -T test.pdf http://localhost:9998/tika
# curl -T test.pdf http://localhost:9998/all > tika-response.zip
# curl -X PUT -d @test.doc http://localhost:9998/tika --header "Content-Type: application/msword"


def extract_meta(file_path):
    response = request_tika(tika_endpoint_meta, file_path)
    meta = response.decode('utf-8')
    logging.debug("tika meta: {}".format(meta))
    return meta


def extract_text(file_path):
    response = request_tika(tika_endpoint_text, file_path)
    text = response.decode('utf-8')
    logging.debug("tika text: {}".format(text))
    return text


def extract_all(file_path):
    zipdata = StringIO()
    zipdata.write(request_tika(tika_endpoint_all, file_path))
    myzipfile = zipfile.ZipFile(zipdata)
    metafile = myzipfile.open('__METADATA__')
    meta = metafile.read().decode('utf-8')
    logging.debug("tika meta: {}".format(meta))
    textfile = myzipfile.open('__TEXT__')
    text = textfile.read().decode('utf-8')
    logging.debug("tika text: {}".format(text))
    return meta, text


def request_tika(url, file_path):
    headers = {}
    headers["Content-Length"] = os.stat(file_path).st_size
    headers["Content-Type"] = mimetypes.guess_type(file_path)[0]
    headers["Date"] = time.strftime("%a, %d %b %Y %X GMT", time.gmtime())
    
    files = {'file': open(file_path, 'rb')}

    response = requests.put(url, files=files, headers=headers)
    response.encoding = "utf-8"
    return response.content


def test():
    file_path = os.path.join(os.path.abspath(os.getcwd()), "data", "resources", "test2.pdf")
    meta = extract_meta(file_path)
    metajson = tika_crosswalk.tika_to_metajson(meta, None)
    logging.info(metajson)
    #extract_text(file_path)
    #extract_all(file_path)


test()
