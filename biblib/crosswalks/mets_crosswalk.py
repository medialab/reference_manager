#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging

from biblib.metajson import Document
from biblib.metajson import Resource
from biblib.metajson import Warpper
from biblib.services import language_service
from biblib.util import constants
from biblib.util import xmletree


mdtype_to_format = {
    'MODS': constants.FORMAT_MODS,
    'EAD': constants.FORMAT_EAD,
    'DC': constants.FORMAT_OAIDC,
    'NISOIMG': constants.FORMAT_MIX,
    'LC-AV': None,
    'VRA': None,
    'TEIHDR': None,
    'DDI': constants.FORMAT_DDI,
    'FGDC': None,
    'LOM': constants.FORMAT_LOM,
    'PREMIS': constants.FORMAT_PREMIS,
    'PREMIS:OBJECT': constants.FORMAT_PREMIS,
    'PREMIS:AGENT': constants.FORMAT_PREMIS,
    'PREMIS:RIGHTS': constants.FORMAT_PREMIS,
    'PREMIS:EVENT': constants.FORMAT_PREMIS,
    'TEXTMD': None,
    'METSRIGHTS': None,
    'OTHER': None
}


def mets_xmletree_to_metajson_list(mets, source, only_first_record):
    yield mets_xmletree_to_metajson(mets, source)


def mets_xmletree_to_metajson(mets, source):
    document = Document()

    # source
    document["rec_source"] = source

    # mets

    # metsHdr

    # dmdSec
    document["dmds"] = extract_dmdsecs(mets)

    # techMD

    # sourceMD

    # digiprovMD

    # fileGrp

    # structMap
    return document


def extract_dmdsecs(mets):
    logging.debug("dmdsecs")
    dmdsecs = mets.findall(xmletree.prefixtag("mets", "dmdSec"))
    if dmdsecs:
        warppers = []
        for dmdsec in dmdsecs:
            warpper = Warpper()

            warpper['rec_id'] = dmdsec.get("ID")
            warpper['rec_id_group'] = dmdsec.get("GROUPID")

            mdwrap = dmdsec.find(xmletree.prefixtag("mets", "mdWrap"))
            warpper['meta_type'] = mdwrap.get("MDTYPE")
            xmldatas = mdwrap.findall(xmletree.prefixtag("mets", "xmlData/*"))
            if xmldatas is not None:
                warpper['records'] = []
                for xmldata in xmldatas:
                    metajson = convert_xmldata(xmldata, warpper['meta_type'])
                    warpper['records'].append(metajson)

            warppers.append(warpper)

        return warppers


def convert_xmldata(xmlData, mdtype):
    # mdtype to input_format
    # xmlData to metajson
    return None
