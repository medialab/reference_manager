#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import json
from datetime import datetime
from biblib.cloud import oaipmh_harvester
from biblib.metajson import Target


def test():
    base_dir = os.path.join(os.getcwd(), "data")
    print "base_dir: " + base_dir

    target_spire = Target()
    target_spire['identifier'] = 'spire'
    target_spire['title'] = 'Sciences Po Institutional Repository'
    target_spire['type'] = 'oaipmh'
    target_spire['url'] = 'http://spire.sciences-po.fr/dissemination/oaipmh2-publications.xml'
    target_spire['metadata_prefix'] = 'mods'

    test_date_from = datetime(2012, 10, 1, 12, 30, 59, tzinfo=None)
    test_date_until = datetime(2013, 4, 30, 17, 50, 1, tzinfo=None)
    test_identifier_book = 'oai:spire.sciences-po.fr:2441/dambferfb7dfprc9m26c8c8o3'
    test_identifier_bookPart = 'oai:spire.sciences-po.fr:2441/eo6779thqgm5r489makgoai85'
    test_identifier_masterThesis = 'oai:spire.sciences-po.fr:2441/5l6uh8ogmqildh09h6m8hj429'
    test_identifier_doctoralThesis = 'oai:spire.sciences-po.fr:2441/3fm4jv3k2s99lms9jb5i5asil'
    test_identifier_professoralThesis = 'oai:spire.sciences-po.fr:2441/f4rshpf3v1umfa09lb0joe5g5'
    
    test_set = 'SHS:ART'

    #result = oaipmh_harvester.identifiy(target_spire)
    #dump_result(result)

    #result = oaipmh_harvester.list_metadata_formats(target_spire, test_identifier_01)
    #dump_result(result)

    #result = oaipmh_harvester.list_sets(target_spire)
    #dump_result(result)

    result = oaipmh_harvester.get_record(target_spire, identifier=test_identifier_bookPart)
    dump_result(result)

    #result = oaipmh_harvester.list_identifiers(target_spire, test_date_from, test_date_until, test_set)
    #dump_result(result)

    #result = oaipmh_harvester.list_records(target_spire, test_date_from, test_date_until, test_set)
    #dump_result(result)


def dump_result(result):
    print json.dumps(result, indent=4, ensure_ascii=False, encoding="utf-8", sort_keys=True)

