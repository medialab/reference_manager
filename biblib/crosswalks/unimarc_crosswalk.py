#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os

from biblib.util import console
from biblib.util import constants

from pymarc import MARCReader


# https://github.com/edsu/pymarc/wiki/Examples
def unimarc_file_to_metasjon_list(unimarc_file):
    reader = MARCReader(unimarc_file)
    count = 0
    for record in reader:
        count += 1
        unimarc_record_to_metajson(record)
    print count


def unimarc_record_to_metajson(record):
    title = author = date = subject = oclc = publisher = ''

    # title
    if record['200'] is not None:
        title = record['200']['a']
        if record['200']['b'] is not None:
            title = title + " " + record['200']['b']

    # determine author
    if record['100'] is not None:
        author = record['100']['a']
    elif record['110'] is not None:
        author = record['110']['a']
    elif record['700'] is not None:
        author = record['700']['a']
    elif record['710'] is not None:
        author = record['710']['a']

    # date
    if record['260'] is not None:
        date = record['260']['c']

    # subject
    if record['650'] is not None:
        subject = record['650']['a']

    # oclc number
    if record['035'] is not None:
        if len(record.get_fields('035')[0].get_subfields('a')) > 0:
            oclc = record['035']['a'].replace('(OCoLC)', '')

    # publisher
    if record['260'] is not None:
        publisher = record['260']['b']

    print title


# Temp Test
console.setup_console()
unimarc_file_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data", "unimarc", "sciencespo-catalog-updates-2013-01-09-21-30-01.marc")
with open(unimarc_file_path) as unimarc_file:
    unimarc_file_to_metasjon_list(unimarc_file)
