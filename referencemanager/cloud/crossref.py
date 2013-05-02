#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import urllib2
from referencemanager.crosswalks import crossref_unixref_to_metajson
from referencemanager.services import config_service

CROSSREF_HEADERS = {'User-Agent': 'Mozilla/5.0'}
config = config_service.config["crossref_openurl"]


def query_openurl_and_retrieve_metadata(openurl, only_first_result):
    unixref = query_openurl(openurl)
    return crossref_unixref_to_metajson.convert_crossref_unixref_string_to_metajson_document(unixref, "crossref", only_first_result)


def query_openurl(openurl):
    """Query CrossRef openurl service with pre-formatted openurl"""
    # example :
    # http://www.crossref.org/openurl?pid=julien.rault@sciences-po.fr&url_ver=Z39.88-2004&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rft.atitle=Isolation of a common receptor for coxsackie B&rft.jtitle=Science&rft.aulast=Bergelson&rft.auinit=J&rft.date=1997&rft.volume=275&rft.spage=1320&rft.epage=1323&format=unixref&redirect=false

    print "CrossRef Query OpenURL {0}".format(openurl)

    url = config["endpoint"] + "?pid=" + config["pid"]
    url += "&" + openurl.replace(" ", "%20") + "&redirect=false&format=" + config["format"]
    print url

    request = urllib2.Request(url, headers=CROSSREF_HEADERS)
    response = urllib2.urlopen(request)
    unixref = response.read()
    print unixref
    return unixref


def query_openurl_elements(journal=False, volume=False, issue=False, spage=False, date=False):
    """Query CrossRef openurl service with openurl elements"""
    # example :
    # http://www.crossref.org/openurl?pid=julien.rault@sciences-po.fr&aulast=Maas%20LRM&title=%20JOURNAL%20OF%20PHYSICAL%20OCEANOGRAPHY&volume=32&issue=3&spage=870&date=2002&format=unixref&redirect=false

    print "CrossRef Query: journal : {0} ; volume : {1} ; issue : {2} ; spage : {3} ; date : {4} ;".format(journal, volume, issue, spage, date)

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
    print url

    request = urllib2.Request(url, headers=CROSSREF_HEADERS)
    response = urllib2.urlopen(request)
    unixref = response.read()
    print unixref
    return unixref
