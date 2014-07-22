#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import xml.etree.ElementTree as ET

import requests

from biblib.crosswalks import openurl_crosswalk
from biblib.services import config_service
from biblib.util import console
from biblib.util import xmletree

console.setup_console()

config_openurl = config_service.config["openurl"]

openurl_endpoint = config_openurl["endpoint"]


def request_periodical_by_issn(issn):
    # Request periodical by ISSN:
    # http://gl5sm8uv5q.openurl.xml.serialssolutions.com/openurlxml?version=1.0&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&rft.genre=journal&issn=0042-0980
    params = {}
    params["version"] = "1.0"
    params["rft_val_fmt"] = openurl_crosswalk.RFT_VAL_FMT_JOURNAL
    params["rft.genre"] = openurl_crosswalk.GENRE_JOURNAL_JOURNAL
    params["issn"] = issn
    return request_by_openurl_params(params)


def request_periodical_by_title(title):
    # Request periodical by Title:
    # http://gl5sm8uv5q.openurl.xml.serialssolutions.com/openurlxml?version=1.0&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&rft.genre=journal&title=Urban%20studies
    params = {}
    params["version"] = "1.0"
    params["rft_val_fmt"] = openurl_crosswalk.RFT_VAL_FMT_JOURNAL
    params["rft.genre"] = openurl_crosswalk.GENRE_JOURNAL_JOURNAL
    params["title"] = title
    return request_by_openurl_params(params)


def request_article_by_openurl_params(params_input):
    params = {}
    params["version"] = "1.0"
    params["rft_val_fmt"] = openurl_crosswalk.RFT_VAL_FMT_JOURNAL
    params["rft.genre"] = openurl_crosswalk.GENRE_JOURNAL_JOURNAL
    params.update(params_input)
    return request_by_openurl_params(params)


def request_by_document(document):
    openurl_string = openurl_crosswalk.metajson_to_openurl(document)
    return request_by_openurl_string(openurl_string)


def request_by_openurl_params(openurl_params):
    response = requests.get(openurl_endpoint, params=openurl_params)
    response.encoding = "utf-8"
    #logging.debug("url: {}".format(response.url))
    #logging.debug(response.content)
    return response_to_xmletree(response)


def request_by_openurl_string(openurl_string):
    url = openurl_endpoint + openurl_string
    response = requests.get(url)
    response.encoding = "utf-8"
    #logging.debug("url: {}".format(response.url))
    #logging.debug(response.content)
    return response_to_xmletree(response)


def response_to_xmletree(response):
    xmletree.register_namespaces()
    return ET.fromstring(response.content)


def test():
    result_periodical_by_issn = request_periodical_by_issn("0042-0980")
    openurl_crosswalk.openurl_xmletree_to_metajson_list(result_periodical_by_issn, None, False)

    result_periodical_by_title = request_periodical_by_title("Urban studies")
    openurl_crosswalk.openurl_xmletree_to_metajson_list(result_periodical_by_title, None, False)

#test()
