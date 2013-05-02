#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import referencemanager
from referencemanager.util import console
from crosswalks import test_bibtext_to_metajson
from crosswalks import test_crossref_unixref_to_metajson
from crosswalks import test_endnote_to_metajson
from crosswalks import test_metajson_to_openurl
from crosswalks import test_mods_to_metajson
from crosswalks import test_summon_json_to_metajson
from cloud import test_crossref
from cloud import test_google_scholar
from cloud import test_oaipmh_harvester
from cloud import test_summon
from nose.tools import *


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_all():
    test_crosswalks()
    test_cloud()
    test_main()


def test_crosswalks():
    test_bibtext_to_metajson.test()
    test_crossref_unixref_to_metajson.test()
    test_endnote_to_metajson.test()
    test_metajson_to_openurl.test()
    test_mods_to_metajson.test()
    test_summon_json_to_metajson.test()


def test_cloud():
    test_crossref.test()
    #test_google_scholar.test()
    test_oaipmh_harvester.test()
    test_summon.test()


def test_main():
    referencemanager.init_repository()
    referencemanager.import_references()


console.setup_console()
test_all()