#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import urllib2

from biblib.services import config_service
from biblib.services import crosswalks_service
from biblib.util import constants

CROSSREF_HEADERS = {'User-Agent': 'Mozilla/5.0'}
config = config_service.config["crossref_openurl"]


def query_openurl_and_retrieve_metadata(openurl, only_first_record):
    unixref = query_openurl(openurl)
    all_in_one_file = True
    return crosswalks_service.convert_string(unixref, constants.FORMAT_UNIXREF, constants.FORMAT_METAJSON, "CrossRef", only_first_record, all_in_one_file)


def query_openurl(openurl):
    """Query CrossRef openurl service with pre-formatted openurl"""
    # example :
    # http://www.crossref.org/openurl?pid=julien.rault@sciences-po.fr&url_ver=Z39.88-2004&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rft.atitle=Isolation of a common receptor for coxsackie B&rft.jtitle=Science&rft.aulast=Bergelson&rft.auinit=J&rft.date=1997&rft.volume=275&rft.spage=1320&rft.epage=1323&format=unixref&redirect=false

    logging.debug("CrossRef Query OpenURL {0}".format(openurl))

    url = config["endpoint"] + "?pid=" + config["pid"]
    url += "&" + openurl.replace(" ", "%20") + "&redirect=false&format=" + config["format"]
    logging.debug(url)

    request = urllib2.Request(url, headers=CROSSREF_HEADERS)
    response = urllib2.urlopen(request)
    unixref = response.read()
    logging.debug(unixref)
    return unixref


def query_openurl_elements(journal=False, volume=False, issue=False, spage=False, date=False):
    """Query CrossRef openurl service with openurl elements"""
    # example :
    # http://www.crossref.org/openurl?pid=julien.rault@sciences-po.fr&aulast=Maas%20LRM&title=%20JOURNAL%20OF%20PHYSICAL%20OCEANOGRAPHY&volume=32&issue=3&spage=870&date=2002&format=unixref&redirect=false

    logging.debug("CrossRef Query: journal : {0} ; volume : {1} ; issue : {2} ; spage : {3} ; date : {4} ;".format(journal, volume, issue, spage, date))

    url = config["endpoint"] + "?pid=" + config["pid"]
    if journal:
        url += "&title=%s" % journal.replace(" ", "%20")
    if volume:
        url += "&volume=%i" % int(volume)
    if issue:
        url += "&issue=%i" % int(issue)
    if spage:
        url += "&spage=%i" % int(spage)
    if date:
        url += "&date=%si" % date
    url += "&redirect=false&format=" + config["format"]
    logging.debug(url)

    request = urllib2.Request(url, headers=CROSSREF_HEADERS)
    response = urllib2.urlopen(request)
    unixref = response.read()
    logging.debug(unixref)
    return unixref
