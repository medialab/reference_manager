#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from nose.tools import *

#import biblib.__main__ as refman
from biblib.util import console

from cloud import test_crossref
from cloud import test_google_scholar
from cloud import test_oaipmh_harvester
from cloud import test_summon
from services import test_crosswalks_service


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_all():
    test_services()
    test_cloud()
    test_main()


def test_services():
    test_crosswalks_service.test()
    pass


def test_cloud():
    test_crossref.test()
    test_google_scholar.test()
    test_oaipmh_harvester.test()
    test_summon.test()


def text_main():
    pass

console.setup_console()
test_all()
