#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import xml.etree.ElementTree as ET

from biblib.metajson import Creator
from biblib.metajson import Document
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Resource
from biblib.metajson import Rights
from biblib.services import country_service
from biblib.services import creator_service
from biblib.services import date_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import constants
from biblib.util import xmletree


def ddi_xmletree_to_metajson_list(ddi_root, source, only_first_record):
    """  DDI xmletree -> MetaJSON Document list"""
    if ddi_root is not None:
        yield ddi_xmletree_to_metajson(ddi_root, source)


def ddi_xmletree_to_metajson(ddi_root, source):
    """ DDI xmletree -> MetaJSON Document """
    if ddi_root is None:
        return None
    
    document = Document()

    document["rec_type"] = constants.DOC_TYPE_DATASETQUALI

    if source:
        document["rec_source"] = source

    # stdyDscr/citation/titlStmt/titl
    ddi_stdydscr = ddi_root.find(xmletree.prefixtag("ddi", "stdyDscr"))
    ddi_stdydscr_citation = ddi_stdydscr.find(xmletree.prefixtag("ddi", "citation"))
    ddi_stdydscr_citation_titlstmt = ddi_stdydscr_citation.find(xmletree.prefixtag("ddi", "titlStmt"))
    ddi_stdydscr_citation_titlstmt_titl = ddi_stdydscr_citation_titlstmt.find(xmletree.prefixtag("ddi", "titl"))
    title = ddi_stdydscr_citation_titlstmt_titl.text
    document["title"] = title

    return document
