#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os

from biblib.metajson import Document
from biblib.metajson import Creator
from biblib.metajson import Subject
from biblib.services import creator_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import console
from biblib.util import constants
from biblib.util import jsonbson

from pymarc import MARCReader


# https://github.com/edsu/pymarc/wiki/Examples
def unimarc_file_to_metasjon_list(unimarc_file):
    reader = MARCReader(unimarc_file, False, False)
    count = 0
    for record in reader:
        count += 1
        unimarc_record_to_metajson(record)
    print count


def unimarc_record_to_metajson(record):
    document = Document()

    #record_dict = record.as_dict()
    #print jsonbson.dumps_json(record_dict, True)

    # leader -> rec_type
    #print record.leader
    print record.leader[6] + " " + record.leader[7]
    document["rec_type"] = "Document"

    # title
    if record['200'] is not None:
        document["title"] = record['200']['a']

    debug = True
    #if debug:
    #    metajson_service.pretty_print_document(document)
    return document


# Temp Test
console.setup_console()
unimarc_file_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data", "unimarc", "sciencespo-catalog-updates-2013-01-09-21-30-01.marc")
with open(unimarc_file_path) as unimarc_file:
    unimarc_file_to_metasjon_list(unimarc_file)
