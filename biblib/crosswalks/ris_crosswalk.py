#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging

from biblib.metajson import Document
from biblib.metajson import Resource
from biblib.services import creator_service
from biblib.services import metajson_service
from biblib.util import constants

RIS_TYPE_ABST = "ABST"
RIS_TYPE_AGGR = "AGGR"
RIS_TYPE_ADVS = "ADVS"
RIS_TYPE_ANCIENT = "ANCIENT"
RIS_TYPE_ART = "ART"
RIS_TYPE_BILL = "BILL"
RIS_TYPE_BLOG = "BLOG"
RIS_TYPE_BOOK = "BOOK"
RIS_TYPE_CASE = "CASE"
RIS_TYPE_CHAP = "CHAP"
RIS_TYPE_CHART = "CHART"
RIS_TYPE_CLSWK = "CLSWK"
RIS_TYPE_COMP = "COMP"
RIS_TYPE_CONF = "CONF"
RIS_TYPE_CPAPER = "CPAPER"
RIS_TYPE_CTLG = "CTLG"
RIS_TYPE_DATA = "DATA"
RIS_TYPE_DBASE = "DBASE"
RIS_TYPE_DICT = "DICT"
RIS_TYPE_EBOOK = "EBOOK"
RIS_TYPE_ECHAP = "ECHAP"
RIS_TYPE_EDBOOK = "EDBOOK"
RIS_TYPE_EJOUR = "EJOUR"
RIS_TYPE_ELEC = "ELEC"
RIS_TYPE_ENCYC = "ENCYC"
RIS_TYPE_EQUA = "EQUA"
RIS_TYPE_FIGURE = "FIGURE"
RIS_TYPE_GEN = "GEN"
RIS_TYPE_GOVDOC = "GOVDOC"
RIS_TYPE_GRNT = "GRNT"
RIS_TYPE_HEAR = "HEAR"
RIS_TYPE_ICOMM = "ICOMM"
RIS_TYPE_INPR = "INPR"
RIS_TYPE_JFULL = "JFULL"
RIS_TYPE_JOUR = "JOUR"
RIS_TYPE_LEGAL = "LEGAL"
RIS_TYPE_MANSCPT = "MANSCPT"
RIS_TYPE_MAP = "MAP"
RIS_TYPE_MGZN = "MGZN"
RIS_TYPE_MPCT = "MPCT"
RIS_TYPE_MULTI = "MULTI"
RIS_TYPE_MUSIC = "MUSIC"
RIS_TYPE_NEWS = "NEWS"
RIS_TYPE_PAMP = "PAMP"
RIS_TYPE_PAT = "PAT"
RIS_TYPE_PCOMM = "PCOMM"
RIS_TYPE_RPRT = "RPRT"
RIS_TYPE_SER = "SER"
RIS_TYPE_SLIDE = "SLIDE"
RIS_TYPE_SOUND = "SOUND"
RIS_TYPE_STAND = "STAND"
RIS_TYPE_STAT = "STAT"
RIS_TYPE_THES = "THES"
RIS_TYPE_UNBILl = "UNBILl"
RIS_TYPE_UNPB = "UNPB"
RIS_TYPE_VIDEO = "VIDEO"

ris_document_type_to_metajson_document_type = {
    RIS_TYPE_ABST: constants.DOC_TYPE_UNPUBLISHEDDOCUMENT,  # ?
    RIS_TYPE_ADVS: constants.DOC_TYPE_VIDEORECORDING,
    RIS_TYPE_AGGR: constants.DOC_TYPE_DATABASE,
    RIS_TYPE_ANCIENT: constants.DOC_TYPE_ANCIENTTEXT,
    RIS_TYPE_ART: constants.DOC_TYPE_ARTWORK,
    RIS_TYPE_BILL: constants.DOC_TYPE_BILL,
    RIS_TYPE_BLOG: constants.DOC_TYPE_WEBSITE,
    RIS_TYPE_BOOK: constants.DOC_TYPE_BOOK,
    RIS_TYPE_CASE: constants.DOC_TYPE_LEGALCASE,
    RIS_TYPE_CHAP: constants.DOC_TYPE_BOOKPART,
    RIS_TYPE_CHART: constants.DOC_TYPE_CHART,
    RIS_TYPE_CLSWK: constants.DOC_TYPE_MUSICALSCORE,
    RIS_TYPE_COMP: constants.DOC_TYPE_SOFTWARE,
    RIS_TYPE_CONF: constants.DOC_TYPE_CONFERENCEPROCEEDINGS,
    RIS_TYPE_CPAPER: constants.DOC_TYPE_CONFERENCEPAPER,
    RIS_TYPE_CTLG: constants.DOC_TYPE_BOOK,  # ?
    RIS_TYPE_DATA: constants.DOC_TYPE_DATASETQUANTI,  # ?
    RIS_TYPE_DBASE: constants.DOC_TYPE_WEBSITE,
    RIS_TYPE_DICT: constants.DOC_TYPE_DICTIONARY,
    RIS_TYPE_EBOOK: constants.DOC_TYPE_BOOKPART,
    RIS_TYPE_ECHAP: constants.DOC_TYPE_EBOOK,
    RIS_TYPE_EDBOOK: constants.DOC_TYPE_BOOK,  # constants.DOC_TYPE_EDITEDBOOK
    RIS_TYPE_EJOUR: constants.DOC_TYPE_JOURNALARTICLE,
    RIS_TYPE_ELEC: constants.DOC_TYPE_WEBPAGE,  # ?
    RIS_TYPE_ENCYC: constants.DOC_TYPE_ENCYCLOPEDIA,
    RIS_TYPE_EQUA: constants.DOC_TYPE_EQUATION,
    RIS_TYPE_FIGURE: constants.DOC_TYPE_IMAGE,
    RIS_TYPE_GEN: constants.DOC_TYPE_UNPUBLISHEDDOCUMENT,  # ?
    RIS_TYPE_GOVDOC: constants.DOC_TYPE_GOVERNMENTPUBLICATION,
    RIS_TYPE_GRNT: constants.DOC_TYPE_GRANT,
    RIS_TYPE_HEAR: constants.DOC_TYPE_HEARING,
    RIS_TYPE_ICOMM: constants.DOC_TYPE_PERSONALCOMMUNICATION,
    RIS_TYPE_INPR: constants.DOC_TYPE_JOURNALARTICLE,  # ?
    RIS_TYPE_JFULL: constants.DOC_TYPE_JOURNAL,
    RIS_TYPE_JOUR: constants.DOC_TYPE_JOURNALARTICLE,
    RIS_TYPE_LEGAL: constants.DOC_TYPE_STATUTE,
    RIS_TYPE_MANSCPT: constants.DOC_TYPE_MANUSCRIPT,
    RIS_TYPE_MAP: constants.DOC_TYPE_MAP,
    RIS_TYPE_MGZN: constants.DOC_TYPE_MAGAZINEARTICLE,
    RIS_TYPE_MPCT: constants.DOC_TYPE_FILM,
    RIS_TYPE_MULTI: constants.DOC_TYPE_WEBPAGE,
    RIS_TYPE_MUSIC: constants.DOC_TYPE_MUSICRECORDING,
    RIS_TYPE_NEWS: constants.DOC_TYPE_NEWSPAPERARTICLE,
    RIS_TYPE_PAMP: constants.DOC_TYPE_BOOK,  # ?
    RIS_TYPE_PAT: constants.DOC_TYPE_PATENT,
    RIS_TYPE_PCOMM: constants.DOC_TYPE_PERSONALCOMMUNICATION,
    RIS_TYPE_RPRT: constants.DOC_TYPE_REPORT,
    RIS_TYPE_SER: constants.DOC_TYPE_BOOK,  # ?
    RIS_TYPE_SLIDE: constants.DOC_TYPE_SLIDE,
    RIS_TYPE_SOUND: constants.DOC_TYPE_AUDIORECORDING,
    RIS_TYPE_STAND: constants.DOC_TYPE_STANDARD,
    RIS_TYPE_STAT: constants.DOC_TYPE_STATUTE,
    RIS_TYPE_THES: constants.DOC_TYPE_DOCTORALTHESIS,
    RIS_TYPE_UNBILl: constants.DOC_TYPE_BILL,  # ?
    RIS_TYPE_UNPB: constants.DOC_TYPE_UNPUBLISHEDDOCUMENT,
    RIS_TYPE_VIDEO: constants.DOC_TYPE_VIDEORECORDING
}

ris_document_type_to_metajson_document_is_part_of_type = {
    RIS_TYPE_CHAP: constants.DOC_TYPE_BOOK,
    RIS_TYPE_CPAPER: constants.DOC_TYPE_CONFERENCEPROCEEDINGS,
    RIS_TYPE_JOUR: constants.DOC_TYPE_JOURNAL,
    RIS_TYPE_MGZN: constants.DOC_TYPE_MAGAZINE,
    RIS_TYPE_NEWS: constants.DOC_TYPE_NEWSPAPER,
    RIS_TYPE_THES: constants.DOC_TYPE_JOURNAL
}

RIS_KEY_BEGIN = "TY"
RIS_KEY_END = "ER"


def ris_txt_lines_to_metajson_list(txt_lines, source, rec_id_prefix, only_first_record):
    document = None
    ris_type = None
    rec_type = None
    is_part_of_rec_type = None
    previous_key = None
    previous_value = None
    for line in txt_lines:
        if line:
            line = line.rstrip('\r\n')
            #logging.debug("line: {}".format(line))

            # multi line management
            if previous_key:
                key = previous_key
                value = previous_value + line
                previous_key = None
                previous_value = None
            else:
                key = line[:2].strip()
                value = line[6:].strip()
            if value.endswith("/") and key not in ["Y1", "PY"]:
                #logging.debug("multi line")
                previous_key = key
                previous_value = value.rstrip('/')
                continue

            if key is None or len(key) == 0:
                # empty line -> continue
                #logging.debug("empty line")
                continue
            elif key == RIS_KEY_BEGIN:
                # record begin with document type -> create document
                # init
                document = Document()
                is_part_of_rec_type = None

                if source:
                    document["rec_source"] = source
                ris_type = value
                rec_type = ris_document_type_to_metajson_document_type[ris_type]
                document["rec_type"] = rec_type
                if ris_type in ris_document_type_to_metajson_document_is_part_of_type:
                    is_part_of_rec_type = ris_document_type_to_metajson_document_is_part_of_type[ris_type]
                    is_part_of = Document()
                    is_part_of["rec_type"] = is_part_of_rec_type
                    document["is_part_ofs"] = [is_part_of]
            elif key == RIS_KEY_END:
                # record end -> return the result
                # verify the is_part_ofs[0]["title"]
                if "is_part_ofs" in document and "title" not in document["is_part_ofs"][0] and "title_abbreviateds" in document["is_part_ofs"][0]:
                    document["is_part_ofs"][0]["title"] = document["is_part_ofs"][0]["title_abbreviateds"][0]["title"]
                    del document["is_part_ofs"][0]["title_abbreviateds"]

                logging.info("# RIS type: {}".format(ris_type))
                metajson_service.pretty_print_document(document)
                yield document
            else:
                # process key value
                #logging.debug("key: {}; value: {}".format(key, value))
                if key == "ID":
                    document["rec_id"] = value
                elif key in ["T1", "TI", "CT"] or (key == "BT" and ris_type in [RIS_TYPE_BOOK, RIS_TYPE_UNPB]):
                    # Title Primary -> title
                    document["title"] = value
                elif key in ["JF", "JO"] or (key == "BT" and ris_type not in [RIS_TYPE_BOOK, RIS_TYPE_UNPB]):
                    # Title Secondary -> is_part_of["title"]
                    document.add_is_part_of_title(value)
                elif key in ["JA", "J1", "J2", "T2"]:
                    # Title Secondary -> is_part_of["title_abbreviateds"][O]["title"]
                    document.add_is_part_of_title_abbreviated(value)
                elif key == "T3":
                    # Title Series
                    document.add_series_title(value)
                elif key in ["A1", "AU"]:
                    document.add_creator(creator_service.formatted_name_to_creator(value, None, "aut"))
                elif key in ["A2", "ED"]:
                    if is_part_of_rec_type:
                        document.add_is_part_of_creator(creator_service.formatted_name_to_creator(value, None, "edt"))
                    else:
                        document.add_creator(creator_service.formatted_name_to_creator(value, None, "edt"))
                elif key == "A3":
                    document.add_series_creator(creator_service.formatted_name_to_creator(value, None, "aut"))
                elif key == "A4":
                    document.add_creator(creator_service.formatted_name_to_creator(value, None, "ctb"))
                elif key in ["PY", "Y1", "DA"]:
                    index_slash = value.find("/")
                    if index_slash != -1:
                        # YYYY/MM/DD/other info (like season)
                        # todo
                        document["date_issued"] = value.strip("/")
                    else:
                        document["date_issued"] = value
                elif key == "SP":
                    document["part_page_begin"] = value
                elif key == "EP":
                    document["part_page_end"] = value
                elif key == "VL":
                    document["part_volume"] = value
                elif key in ["IS", "CP"]:
                    document["part_issue"] = value
                elif key in ["AB", "N2"]:
                    document["descriptions"] = [{"language": "und", "value": value}]
                elif key == "N1":
                    document["notes"] = [{"language": "und", "value": value}]
                elif key == "PB":
                    document.add_item_to_key(value, "publishers")
                elif key == "CY":
                    document.add_item_to_key(value, "publication_places")
                elif key == "RP":
                    document["publication_status"] = value
                elif key == "ET":
                    document["edition"] = value
                elif key == "UR":
                    resource = Resource()
                    resource["url"] = value
                    document.add_item_to_key(resource, "resources")
                elif key == "AN":
                    # Accession Number
                    identifier = metajson_service.create_identifier("accessionnumber", value)
                    document.add_identifier(identifier)
                elif key == "CN":
                    # Call Number
                    identifier = metajson_service.create_identifier("callnumber", value)
                    document.add_identifier(identifier)
                elif key == "DO":
                    # DOI
                    identifier = metajson_service.create_identifier("doi", value)
                    document.add_identifier(identifier)
                elif key == "SN":
                    # ISBN or ISSN ?
                    id_type = None
                    if rec_type in [constants.DOC_TYPE_JOURNALARTICLE, constants.DOC_TYPE_MAGAZINEARTICLE, constants.DOC_TYPE_NEWSPAPERARTICLE, constants.DOC_TYPE_JOURNAL]:
                        id_type = "issn"
                    else:
                        id_type = "isbn"
                    identifier = metajson_service.create_identifier(id_type, value)
                    if is_part_of_rec_type is None:
                        document.add_identifier(identifier)
                    else:
                        document["is_part_ofs"][0].add_identifier(identifier)
                elif key == "CA":
                    document["caption"] = value
                elif key == "DB":
                    # Name of Database -> rec_source ?
                    document["rec_source"] = value
                elif key == "DP":
                    # NDatabase Provider -> rec_source ?
                    document["rec_source"] = value
                elif key == "KW":
                    if "keywords" not in document:
                        document["keywords"] = {"und": []}
                    document["keywords"]["und"].append(value)
                else:
                    logging.debug("Not managed key: {} with value: {}".format(key, value))
