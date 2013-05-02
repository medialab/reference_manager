#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import json
from datetime import datetime
from referencemanager.cloud import oaipmh_harvester
from referencemanager.metajson import Target


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
    test_identifier = 'oai:spire.sciences-po.fr:2441/dambferfb7dfprc9m263lgtsl'
    test_set = 'SHS:ART'

    result = oaipmh_harvester.identifiy(target_spire)
    dump_result(result)

    result = oaipmh_harvester.list_metadata_formats(target_spire, test_identifier)
    dump_result(result)

    result = oaipmh_harvester.list_sets(target_spire)
    dump_result(result)

    result = oaipmh_harvester.get_record(target_spire, identifier=test_identifier)
    dump_result(result)

    result = oaipmh_harvester.list_identifiers(target_spire, test_date_from, test_date_until, test_set)
    dump_result(result)

    result = oaipmh_harvester.list_records(target_spire, test_date_from, test_date_until, test_set)
    dump_result(result)


def dump_result(result):
    print json.dumps(result, indent=4, ensure_ascii=False, encoding="utf-8", sort_keys=True)
