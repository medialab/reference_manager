#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# based on :
#
# gscholar - Get bibtex entries from Goolge Scholar
# Copyright (C) 2011  Bastian Venthur <venthur at debian org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""Google Scholar DAO

"""

import random
import re
import urllib2
import hashlib
from htmlentitydefs import name2codepoint
from bs4 import BeautifulSoup
from referencemanager.services import config_service


config = config_service.config["google_scholar"]

# Fake google id (looks like it is a 16 elements hex)
google_id = hashlib.md5(str(random.random())).hexdigest()[:16]

# Cookie looks like:
# 'Cookie' : 'GSP=ID=%s:CF=4' % google_id }
# where CF is the format (e.g. bibtex).
GOOGLE_HEADERS = {'User-Agent': 'Mozilla/5.0', 'Cookie': 'GSP=ID=%s' % google_id}

FORMAT_BIBTEX = 4
FORMAT_ENDNOTE = 3
FORMAT_REFMAN = 2
FORMAT_WENXIANWANG = 5


def query_and_retrieve_metadata(q, only_first_result):
    """Search Google Scholar with a pre-formatted query like :
    intitle:"{0}"
    and extract the metadata in the specified format.
    if only_first_result == True only the first result in retrieve."""

    meta_format = FORMAT_BIBTEX

    html = query(q, meta_format)

    cited_by_list = extract_cited_by_list(html)
    h = calcul_h_index(cited_by_list)
    print h

    metadata_links = extract_metadata_links(html, meta_format)

    if only_first_result is True and len(metadata_links) != 0:
        metadata_links = [metadata_links[0]]

    return retrieve_metadata_list(metadata_links)


def query(query, meta_format):
    """Query Google Scholar and just return the html response"""

    print "Google Sholar Query: {0} ; metadata format: {1}".format(query, meta_format)

    query = '/scholar?q='+urllib2.quote(query)
    url = config["endpoint"] + query

    headers = GOOGLE_HEADERS
    headers['Cookie'] = headers['Cookie'] + ":CF=%d" % meta_format

    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
    html.decode('ascii', 'ignore')
    #print html
    return html


def extract_metadata_links(html, meta_format):
    """Extract metadata URL from the html for a specified metadata format"""

    if meta_format == FORMAT_BIBTEX:
        meta_re = re.compile(r'<a href="(/scholar\.bib\?[^>]*)">')
    elif meta_format == FORMAT_ENDNOTE:
        meta_re = re.compile(r'<a href="(/scholar\.enw\?[^>]*)">')
    elif meta_format == FORMAT_REFMAN:
        meta_re = re.compile(r'<a href="(/scholar\.ris\?[^>]*)">')
    elif meta_format == FORMAT_WENXIANWANG:
        meta_re = re.compile(r'<a href="(/scholar\.ral\?[^>]*)">')

    links = meta_re.findall(html)

    # escape html enteties
    links = [re.sub('&(%s);' % '|'.join(name2codepoint), lambda m:
        unichr(name2codepoint[m.group(1)]), s) for s in links]
    return links


def retrieve_metadata_list(links):
    """Just download metadata from a list of links"""

    results = []
    for link in links:
        url = config["endpoint"] + link
        request = urllib2.Request(url, headers=GOOGLE_HEADERS)
        response = urllib2.urlopen(request)
        metadata = response.read()
        print
        print
        print metadata
        results.append(metadata)
    return results


def extract_cited_by_list(html):
    cited_by_list = []
    soup = BeautifulSoup(html)
    for record in soup('p', {'class': 'g'}):
        match = re.search("Cited by ([^<]*)", str(record))
        if match is not None:
            cited_by = int(match.group(1))
            print
            print "Cited by %s" % cited_by
            cited_by_list.append(cited_by)
    return cited_by_list


def calcul_h_index(cited_by_list):
    cited_by_list.sort()
    cited_by_list.reverse()

    h = 0
    for cited_by in cited_by_list:
        if cited_by > h:
            h += 1
    print h
    return h
