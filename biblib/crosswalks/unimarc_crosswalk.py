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


def unimarc_file_path_to_metasjon_list(unimarc_file_path, source, only_first_record):
    with open(unimarc_file_path) as unimarc_file:
        return unimarc_file_to_metasjon_list(unimarc_file, source, only_first_record)


def unimarc_file_to_metasjon_list(unimarc_file, source, only_first_record):
    print unimarc_file
    marc_reader = MARCReader(unimarc_file, False, False)
    return unimarc_marcreader_to_metasjon_list(marc_reader, source, only_first_record)


def unimarc_marcreader_to_metasjon_list(marc_reader, source, only_first_record):
    print "unimarc_marcreader_to_metasjon_list"
    count = 0
    for record in marc_reader:
        count += 1
        yield unimarc_record_to_metajson(record, source)
    print count


def unimarc_record_to_metajson(record, source):
    print "unimarc_record_to_metajson"
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
    if debug:
        pass
        #metajson_service.pretty_print_document(document)
    return document
    print "fin"


# Temp Test
#console.setup_console()
#unimarc_file_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data", "unimarc", "sciencespo-catalog-updates-2013-01-09-21-30-01.marc")
#with open(unimarc_file_path) as unimarc_file:
#    unimarc_file_to_metasjon_list(unimarc_file)
