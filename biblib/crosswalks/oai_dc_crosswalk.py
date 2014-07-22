#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import xml.etree.ElementTree as ET

from biblib import metajson
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


######################
# oai_dc -> MetaJSON #
######################

DC_TYPE_EU_REPO_TO_METAJSON_DOCUMENT_TYPE = {
    # registered info:eu-repo/semantics types
    "info:eu-repo/semantics/annotation": constants.DOC_TYPE_ANNOTATIONARTICLE,
    "info:eu-repo/semantics/article": constants.DOC_TYPE_JOURNALARTICLE,
    "info:eu-repo/semantics/bachelorThesis": constants.DOC_TYPE_MASTERTHESIS,
    "info:eu-repo/semantics/book": constants.DOC_TYPE_BOOK,
    "info:eu-repo/semantics/bookPart": constants.DOC_TYPE_BOOKPART,
    "info:eu-repo/semantics/bookReview": constants.DOC_TYPE_BOOKREVIEW,
    "info:eu-repo/semantics/conferenceContribution": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "info:eu-repo/semantics/conferenceItem": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "info:eu-repo/semantics/conferenceObject": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "info:eu-repo/semantics/conferencePaper": constants.DOC_TYPE_CONFERENCEPAPER,
    "info:eu-repo/semantics/conferencePoster": constants.DOC_TYPE_CONFERENCEPOSTER,
    "info:eu-repo/semantics/conferenceProceedings": constants.DOC_TYPE_CONFERENCEPROCEEDINGS,
    "info:eu-repo/semantics/contributionToPeriodical": constants.DOC_TYPE_NEWSPAPERARTICLE,  # or DOC_TYPE_MAGAZINEARTICLE
    "info:eu-repo/semantics/doctoralThesis": constants.DOC_TYPE_DOCTORALTHESIS,
    "info:eu-repo/semantics/lecture": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "info:eu-repo/semantics/masterThesis": constants.DOC_TYPE_MASTERTHESIS,
    "info:eu-repo/semantics/other": constants.DOC_TYPE_UNPUBLISHEDDOCUMENT,
    "info:eu-repo/semantics/patent": constants.DOC_TYPE_PATENT,
    "info:eu-repo/semantics/preprint": constants.DOC_TYPE_PREPRINT,
    "info:eu-repo/semantics/report": constants.DOC_TYPE_REPORT,
    "info:eu-repo/semantics/reportPart": constants.DOC_TYPE_REPORTPART,
    "info:eu-repo/semantics/researchProposal": constants.DOC_TYPE_RESEARCHPROPOSAL,
    "info:eu-repo/semantics/review": constants.DOC_TYPE_BOOKREVIEW,
    "info:eu-repo/semantics/studentThesis": constants.DOC_TYPE_MASTERTHESIS,
    "info:eu-repo/semantics/technicalDocumentation": constants.DOC_TYPE_TECHREPORT,
    "info:eu-repo/semantics/workingPaper": constants.DOC_TYPE_WORKINGPAPER,
    # not registered info:eu-repo/semantics types
    "info:eu-repo/semantics/audiovisual": constants.DOC_TYPE_VIDEORECORDING,
    "info:eu-repo/semantics/interview": constants.DOC_TYPE_INTERVIEWARTICLE,
    "info:eu-repo/semantics/map": constants.DOC_TYPE_MAP,
    "info:eu-repo/semantics/periodicalIssue": constants.DOC_TYPE_PERIODICALISSUE,
    "info:eu-repo/semantics/professoralThesis": constants.DOC_TYPE_PROFESSORALTHESIS,
    "info:eu-repo/semantics/series": constants.DOC_TYPE_SERIES,
    "info:eu-repo/semantics/unspecified": constants.DOC_TYPE_UNPUBLISHEDDOCUMENT,
    "info:eu-repo/semantics/website": constants.DOC_TYPE_WEBSITE,
    "info:eu-repo/semantics/websiteContribution": constants.DOC_TYPE_WEBPAGE
}

DC_TYPE_EPRINT_TO_METAJSON_DOCUMENT_TYPE = {
    # registered http://purl.org/eprint/type/ types
    "http://purl.org/eprint/type/Book": constants.DOC_TYPE_BOOK,
    "http://purl.org/eprint/type/BookItem": constants.DOC_TYPE_BOOKPART,
    "http://purl.org/eprint/type/BookReview": constants.DOC_TYPE_BOOKREVIEW,
    "http://purl.org/eprint/type/ConferenceItem": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "http://purl.org/eprint/type/ConferencePaper": constants.DOC_TYPE_CONFERENCEPAPER,
    "http://purl.org/eprint/type/ConferencePoster": constants.DOC_TYPE_CONFERENCEPOSTER,
    "http://purl.org/eprint/type/JournalArticle": constants.DOC_TYPE_JOURNALARTICLE,
    "http://purl.org/eprint/type/JournalItem": constants.DOC_TYPE_PERIODICALISSUE,
    "http://purl.org/eprint/type/NewsItem": constants.DOC_TYPE_NEWSPAPERARTICLE,
    "http://purl.org/eprint/type/Patent": constants.DOC_TYPE_PATENT,
    "http://purl.org/eprint/type/Report": constants.DOC_TYPE_REPORT,
    "http://purl.org/eprint/type/SubmittedJournalArticle": constants.DOC_TYPE_PREPRINT,
    "http://purl.org/eprint/type/Thesis": constants.DOC_TYPE_DOCTORALTHESIS,
    "http://purl.org/eprint/type/WorkingPaper": constants.DOC_TYPE_WORKINGPAPER
}

DC_TYPE_MARCGT_TO_METAJSON_DOCUMENT_TYPE = {
    # registered marcgt genre
    "abstract or summary": constants.DOC_TYPE_BOOKREVIEW,
    "article": constants.DOC_TYPE_JOURNALARTICLE,
    "atlas": constants.DOC_TYPE_MAP,
    "autobiography": constants.DOC_TYPE_BOOK,
    "bibliography": constants.DOC_TYPE_BIBLIOGRAPHY,
    "biography": constants.DOC_TYPE_BOOK,
    "book": constants.DOC_TYPE_BOOK,
    "conference publication": constants.DOC_TYPE_CONFERENCEPROCEEDINGS,
    "catalog": constants.DOC_TYPE_BOOK,
    "chart": constants.DOC_TYPE_CHART,
    "comic strip": constants.DOC_TYPE_BOOK,
    "database": constants.DOC_TYPE_DATABASE,
    "dictionary": constants.DOC_TYPE_DICTIONARY,
    "directory": constants.DOC_TYPE_BOOK,
    "drama": constants.DOC_TYPE_BOOK,
    "encyclopedia": constants.DOC_TYPE_ENCYCLOPEDIA,
    "essay": constants.DOC_TYPE_BOOK,
    "festschrift": constants.DOC_TYPE_BOOK,
    "fiction": constants.DOC_TYPE_BOOK,
    "folktale": constants.DOC_TYPE_BOOK,
    "globe": constants.DOC_TYPE_MAP,
    "graphic": constants.DOC_TYPE_CHART,
    "handbook": constants.DOC_TYPE_BOOK,
    "history": constants.DOC_TYPE_BOOK,
    "humor, satire": constants.DOC_TYPE_BOOK,
    "index": constants.DOC_TYPE_BOOK,
    "instruction": constants.DOC_TYPE_MANUEL,
    "issue": constants.DOC_TYPE_PERIODICALISSUE,
    "interview": constants.DOC_TYPE_INTERVIEWARTICLE,
    "journal": constants.DOC_TYPE_JOURNAL,
    "kit": constants.DOC_TYPE_BOOK,
    "language instruction": constants.DOC_TYPE_AUDIORECORDING,
    "law report or digest": constants.DOC_TYPE_ANNOTATIONARTICLE,
    "legislation": constants.DOC_TYPE_STATUTE,
    "letter": constants.DOC_TYPE_LETTER,
    "loose-leaf": constants.DOC_TYPE_PERIODICALISSUE,
    "map": constants.DOC_TYPE_MAP,
    "motion picture": constants.DOC_TYPE_FILM,
    "memoir": constants.DOC_TYPE_BOOK,
    "newspaper": constants.DOC_TYPE_NEWSPAPER,
    "novel": constants.DOC_TYPE_BOOK,
    "numeric data": constants.DOC_TYPE_DATASETQUANTI,
    "online system or service": constants.DOC_TYPE_WEBSITE,
    "patent": constants.DOC_TYPE_PATENT,
    "periodical": constants.DOC_TYPE_JOURNAL,
    "picture": constants.DOC_TYPE_IMAGE,
    "poetry": constants.DOC_TYPE_BOOK,
    "programmed text": constants.DOC_TYPE_SOFTWARE,
    "rehearsal": constants.DOC_TYPE_BOOK,
    "remote sensing image": constants.DOC_TYPE_MAP,
    "report": constants.DOC_TYPE_REPORT,
    "reporting": constants.DOC_TYPE_REPORT,
    "review": constants.DOC_TYPE_BOOKREVIEW,
    "series": constants.DOC_TYPE_SERIES,
    "short story": constants.DOC_TYPE_BOOK,
    "slide": constants.DOC_TYPE_SLIDE,
    "sound": constants.DOC_TYPE_AUDIORECORDING,
    "speech": constants.DOC_TYPE_SPEECH,
    "statistics": constants.DOC_TYPE_DATASETQUANTI,
    "survey of literature": constants.DOC_TYPE_BOOKREVIEW,
    "technical drawing": constants.DOC_TYPE_DRAWING,
    "technical report": constants.DOC_TYPE_TECHREPORT,
    "thesis": constants.DOC_TYPE_DOCTORALTHESIS,
    "treaty": constants.DOC_TYPE_TREATY,
    "videorecording": constants.DOC_TYPE_VIDEORECORDING,
    "web site": constants.DOC_TYPE_WEBSITE,
    "websiteContribution": constants.DOC_TYPE_WEBPAGE
}

# Last chance...
DC_TYPE_FREE_TO_METAJSON_DOCUMENT_TYPE = {
    "journal article": constants.DOC_TYPE_JOURNALARTICLE,
    "Website": constants.DOC_TYPE_WEBSITE
}

DC_TYPE_DCMITYPE_TO_METAJSON_DOCUMENT_TYPE = {
    "Collection" : constants.DOC_TYPE_COLLECTION,
    "Dataset" : constants.DOC_TYPE_DATASET,
    "Event" : constants.DOC_TYPE_EVENT,
    "Image": constants.DOC_TYPE_IMAGE,
    "MovingImage": constants.DOC_TYPE_VIDEORECORDING,
    "StillImage": constants.DOC_TYPE_IMAGE,
    "InteractiveResource": constants.DOC_TYPE_MULTIMEDIA,
    "PhysicalObject": constants.DOC_TYPE_PHYSICALOBJECT,
    "Service": constants.DOC_TYPE_SERVICE,
    "Software": constants.DOC_TYPE_SOFTWARE,
    "Sound": constants.DOC_TYPE_AUDIORECORDING,
    "Text": constants.DOC_TYPE_DOCUMENT
}

def oai_dc_xmletree_to_metajson_list(oai_dc_root, source, only_first_record):
    """  oai_dc xmletree -> MetaJSON Document list"""
    if oai_dc_root is not None:
        if oai_dc_root.tag.endswith("oai_dc"):
            yield oai_dc_xmletree_to_metajson(oai_dc_root, source)


def oai_dc_xmletree_to_metajson(oai_dc, source):
    """ oai_dc xmletree -> MetaJSON Document """
    if oai_dc is None:
        return None

    document = Document()

    # source
    if source:
        document["rec_source"] = source

    metajson_service.pretty_print_document(document)
    return document



######################
# MetaJSON -> oai_dc #
######################


def metajson_to_oai_dc_xmletree(document, with_schema_location=True):
    """ MetaJSON Document -> oai_dc xmletree """
    rec_id = document["rec_id"]
    xmletree.register_namespaces()
    # oai_dc root
    oai_dc = ET.Element(xmletree.prefixtag("oai_dc", "oai_dc"))
    if with_schema_location:
        oai_dc.set(xmletree.prefixtag("xsi", "schemaLocation"), constants.xmlns_map["oai_dc"] + " " + constants.xmlns_schema_map["oai_dc"])

    # title
    if "title" in document:
        dc_title = ET.SubElement(oai_dc, xmletree.prefixtag("dc", "title"))
        dc_title.text = document["title"]

    # creators
    if "creators" in document and document["creators"]:
        for creator in document["creators"]:
            if "roles" in creator and creator["roles"] and creator["roles"][0]:
                creator_role = creator["roles"][0]
                if creator_role in creator_service.role_type and creator_service.role_type[creator_role] == creator_service.role_type_creator:
                    dc_creator = ET.SubElement(oai_dc, xmletree.prefixtag("dc", "creator"))
                    dc_creator.text = creator.formatted_name(metajson.STYLE_FAMILY_COMMA_GIVEN)
                    continue
            dc_contributor = ET.SubElement(oai_dc, xmletree.prefixtag("dc", "contributor"))
            dc_contributor.text = creator.formatted_name(metajson.STYLE_FAMILY_COMMA_GIVEN)

    return (rec_id, oai_dc)

#########
# Utils #
#########

def convert_mods_date(mods_date):
    """ Extract and convert MODS date to ISO 8601 """
    if mods_date is not None and mods_date.text is not None:
        encoding = mods_date.get("encoding")
        #point = mods_date.get("point")
        #key_date = mods_date.get("keyDate")
        #qualifier = mods_date.get("qualifier")
        value = mods_date.text.strip()
        if encoding in ["iso8601"]:
            return value
        else:
            # todo
            #parsed_date = date_service.parse_to_iso8601(value)
            #if parsed_date:
            #    return parsed_date
            return value


def convert_mods_string_authorities(mods_string_authorities):
    """ text, authority -> value, authority """
    if mods_string_authorities is not None:
        results = []
        for mods_string_authority in mods_string_authorities:
            if mods_string_authority is not None:
                authority = mods_string_authority.get("authority")
                value = mods_string_authority.text.strip()
                if value is not None:
                    result = {"value": value}
                    if authority is not None:
                        result["authority"] = authority.strip()
                    results.append(result)
        return results


def convert_mods_string_langs(mods_string_langs):
    """ lang, text -> language, value """
    if mods_string_langs is not None:
        results = []
        for mods_string_lang in mods_string_langs:
            if mods_string_lang is not None:
                language = mods_string_lang.get("lang")
                value = mods_string_lang.text.strip()
                if value is not None:
                    result = {"value": value}
                    if language is not None:
                        result["language"] = language.strip()
                    results.append(result)
        return results


def convert_mods_string_lang_types(mods_string_lang_types, type_field):
    if mods_string_lang_types is not None:
        results = []
        for mods_string_lang_type in mods_string_lang_types:
            if mods_string_lang_type is not None and mods_string_lang_type.text is not None:
                language = mods_string_lang_type.get("lang")
                type_value = mods_string_lang_type.get("type")
                value = mods_string_lang_type.text.strip()
                if value is not None:
                    result = {"value": value}
                    if language is not None:
                        result["language"] = language.strip()
                    if type_value is not None:
                        result[type_field] = type_value.strip()
                    results.append(result)
        return results


def get_mods_textlangs_as_list(rml, element):
    """ @xml:lang -> language
        text -> value """
    rml_sls = rml.findall(xmletree.prefixtag("mods", element))
    if rml_sls is not None:
        sls = []
        for rml_sl in rml_sls:
            if rml_sl is not None and rml_sl.text is not None:
                language = rml_sl.get(xmletree.prefixtag("xml", "lang"))
                value = rml_sl.text.strip()
                if value is not None:
                    sl = {"value": value}
                    if language is not None:
                        sl["language"] = language.strip()
                    sls.append(sl)
        if sls:
            return sls


def get_mods_textlangs_and_set_key(rml, element, key):
    """ element -> key
        @xml:lang -> language
        text -> value """
    result = {}
    sls = get_mods_textlangs_as_list(rml, element)
    if sls:
        result[key] = sls
    return result


def get_mods_element_text(rml, element, strip=True):
    element_xmletree = rml.find(xmletree.prefixtag("mods", element))
    return xmletree.get_element_text(element_xmletree, strip)


def get_mods_element_text_as_boolean(rml, element):    
    element_xmletree = rml.find(xmletree.prefixtag("mods", element))
    return xmletree.get_element_text_as_boolean(element_xmletree)


def get_mods_element_text_and_set_key(rml, element, key, strip=True):
    result = {}
    key_value = get_mods_element_text(rml, element, strip)
    if key_value is not None:
        result[key] = key_value
    return result


def get_mods_elements_text(rml, element):
    elements_xmletree = rml.findall(xmletree.prefixtag("mods", element))
    if elements_xmletree is not None:
        results = []
        for element_xmletree in elements_xmletree:
            if element_xmletree is not None:
                results.append(xmletree.get_element_text(element_xmletree))
        if results:
            return results
    return None


def get_mods_elements_text_and_set_key(rml, element, key):
    result = {}
    values = get_mods_elements_text(rml, element)
    if values is not None:
        result[key] = values
    return result
