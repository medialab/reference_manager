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

    # rec_id
    rec_id = ""
    if record['002'] is not None:
        rec_id_prefix = "sciencespo_catalog_"
        rec_id = rec_id_prefix + record['002'].data
    if record['991'] is not None and record['991']['e'] is not None:
        rec_id += "_" + record['991']['e']
    if rec_id:
        print "rec_id: {}".format(rec_id)
        document["rec_id"] = rec_id

    # leader -> rec_type
    rec_type = extract_unimarc_type(record)
    document["rec_type"] = rec_type

    # identifiers
    identifiers = []
    if record['001'] is not None and record['001'].data is not None:
        identifiers.append({"id_type": "ppn", "value": record['001'].data})
    if record['010'] is not None and record['010']['a'] is not None:
        identifiers.append({"id_type": "isbn", "value": record['010']['a']})
    if record['011'] is not None and record['011']['a'] is not None:
        identifiers.append({"id_type": "issn", "value": record['011']['a']})
    if record['013'] is not None and record['013']['a'] is not None:
        identifiers.append({"id_type": "ismn", "value": record['013']['a']})
    if record['016'] is not None and record['016']['a'] is not None:
        identifiers.append({"id_type": "isrc", "value": record['016']['a']})
    #if record['020'] is not None and record['020']['b'] is not None:
    #    identifiers.append({"id_type": "lccn", "value": record['020']['b']})
    if record['040'] is not None and record['040']['a'] is not None:
        identifiers.append({"id_type": "coden", "value": record['040']['a']})
    if record['073'] is not None and record['073']['a'] is not None:
        identifiers.append({"id_type": "ean", "value": record['073']['a']})
    if record['945'] is not None and record['945']['b'] is not None:
        identifiers.append({"id_type": "callnumber", "value": record['945']['b']})
    if identifiers:
        document["identifiers"] = identifiers

    # title
    if record['200'] is not None:
        if record['200']['a'] is not None:
            title_non_sort_pos = int(record['200'].indicator2)
            if title_non_sort_pos != 0:
                document["title_non_sort"] = record['200']['a'][:title_non_sort_pos]
                document["title"] = record['200']['a'][title_non_sort_pos:]
            else:
                document["title"] = record['200']['a']
            #print "title: {}".format(document["title"])
        if record['200']['d'] is not None:
            document["title_alternative"] = {"title": record['200']['d']}
        if record['200']['e'] is not None:
            document["title_sub"] = record['200']['e']
        if record['200']['h'] is not None:
            document["part_number"] = record['200']['h']
        if record['200']['i'] is not None:
            document["part_name"] = record['200']['i']

    # date_issued
    if record['100'] is not None and record['100']['a'] is not None:
        date_issued = record['100']['a'][9:13]
        if date_issued:
            document["date_issued"] = date_issued

    # publishers, publication_places
    publication_places = []
    publishers = []
    for field210 in record.get_fields('210'):
        for field210a in field210.get_subfields('a'):
            if field210a is not None and field210a not in publication_places:
                publication_places.append(field210a)
        for field210c in field210.get_subfields('c'):
            if field210c is not None and field210c not in publishers:
                publishers.append(field210c)
    if publication_places:
        document["publication_places"] = publication_places
    if publishers:
        document["publishers"] = publishers

    debug = True
    if debug:
        metajson_service.pretty_print_document(document)
    return document


def extract_unimarc_type(record):
    rec_type = None

    # leader
    leader6 = record.leader[6]
    leader7 = record.leader[7]

    # 100$a/17-19
    # 100$a/20
    field100ap1719 = None
    field100ap20 = None
    if record['100'] is not None and record['100']['a'] is not None:
        field100ap1719 = record['100']['a'][17:20]
        field100ap20 = record['100']['a'][20:21]

    # 105/4-7
    field105ap48 = None
    if record['105'] is not None and record['105']['a'] is not None:
        field105ap48 = record['105']['a'][4:8]

    # 106$a
    field106a = None
    if record['106'] is not None and record['106']['a'] is not None:
        field106a = record['106']['a']

    # 110$a/1
    field110ap1 = None
    if record['110'] is not None and record['110']['a'] is not None:
        field110ap1 = record['110']['a'][1:2]

    # 115$a/0
    field115ap0 = None
    if record['115'] is not None and record['115']['a'] is not None:
        field115ap0 = record['115']['a'][0:1]

    # 116/0
    field116ap0 = None
    if record['116'] is not None and record['116']['a'] is not None:
        field116ap0 = record['116']['a'][0:1]

    # 121$a/0
    field121ap0 = None
    if record['121'] is not None and record['121']['a'] is not None:
        field121ap0 = record['121']['a'][0:1]

    # 124$b
    field124b = None
    if record['124'] is not None and record['124']['b'] is not None:
        field124b = record['124']['b']

    # 126$a/0
    field126ap0 = None
    if record['126'] is not None and record['126']['a'] is not None:
        field126ap0 = record['126']['a'][0:1]

    # 135/0
    field135ap0 = None
    if record['135'] is not None and record['135']['a'] is not None:
        field135ap0 = record['135']['a'][0:1]

    debug = True
    if debug:
        print "leader6: {}".format(leader6)
        print "leader7: {}".format(leader7)
        print "100$a/17-19: {}".format(field100ap1719)
        print "100$a/20: {}".format(field100ap20)
        print "105/4-7: {}".format(field105ap48)
        print "106$a: {}".format(field106a)
        print "110$a/1: {}".format(field110ap1)
        print "115$a/0: {}".format(field115ap0)
        print "116/0: {}".format(field116ap0)
        print "121$a/0: {}".format(field121ap0)
        print "124$b: {}".format(field124b)
        print "126$a/0: {}".format(field126ap0)
        print "135/0: {}".format(field135ap0)

    if leader6 == "a":
        if leader7 == "a":
            rec_type = constants.DOC_TYPE_JOURNALARTICLE
        elif leader7 == "c":
            rec_type = "PressClipping"
        elif leader7 == "m":
            rec_type = constants.DOC_TYPE_BOOK
        elif leader7 == "s":
            rec_type = constants.DOC_TYPE_JOURNAL
    elif leader6 == "b":
        rec_type = constants.DOC_TYPE_MANUSCRIPT
    elif leader6 in ["c", "d"]:
        rec_type = constants.DOC_TYPE_MUSICALSCORE
    elif leader6 in ["e", "f"]:
        rec_type = constants.DOC_TYPE_MAP
    elif leader6 == "g":
        rec_type = constants.DOC_TYPE_VIDEORECORDING
    elif leader6 == "i":
        rec_type = constants.DOC_TYPE_AUDIORECORDING
    elif leader6 == "j":
        rec_type = constants.DOC_TYPE_MUSICRECORDING
    elif leader6 == "k":
        rec_type = constants.DOC_TYPE_IMAGE
    elif leader6 == "l":
        rec_type = "ElectronicResource"
    elif leader6 == "m":
        rec_type = "Kit"
    elif leader6 == "r":
        rec_type = constants.DOC_TYPE_PHYSICALOBJECT
    else:
        rec_type = constants.DOC_TYPE_DOCUMENT

    return rec_type
