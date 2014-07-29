#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import xml.etree.ElementTree as ET

from biblib.metajson import Creator
from biblib.metajson import Document
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Project
from biblib.metajson import Resource
from biblib.metajson import Rights
from biblib.services import country_service
from biblib.services import creator_service
from biblib.services import date_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import constants
from biblib.util import xmletree


def tei_xmletree_to_metajson_list(tei_root, source, rec_id_prefix, only_first_record):
    """  TEI xmletree -> MetaJSON Document list"""
    if tei_root is not None:
        # TEI/text
        tei_text = tei_root.find(xmletree.prefixtag("tei", "text"))

        # TEI/text/body
        tei_body = tei_text.find(xmletree.prefixtag("tei", "body"))
        # TEI/text/body/listBibl
        tei_body_listbibl = tei_body.find(xmletree.prefixtag("tei", "listBibl"))
        # TEI/text/body/listBibl/biblFull
        tei_body_listbibl_biblfulls = tei_body_listbibl.findall(xmletree.prefixtag("tei", "biblFull"))

        # TEI/text/back
        tei_back = tei_text.find(xmletree.prefixtag("tei", "back"))
        # TEI/text/back/div
        tei_back_divs = tei_back.findall(xmletree.prefixtag("tei", "div"))
        laboratories = []
        projects = []
        if tei_back_divs:
            for tei_back_div in tei_back_divs:
                if tei_back_div.get("type") == "laboratories":
                    orgs = tei_back_div.findall(xmletree.prefixtag("tei", "org"))
                    for org in orgs:
                        laboratories.append(org_laboratory_to_metajson(org))
                elif tei_back_div.get("type") == "projects":
                    orgs = tei_back_div.findall(xmletree.prefixtag("tei", "org"))
                    for org in orgs:
                        laboratories.append(org_project_to_metajson(org))

        for biblfull in tei_body_listbibl_biblfulls:
            yield biblfull_xmletree_to_metajson(biblfull, laboratories, projects, source)



def biblfull_xmletree_to_metajson(biblfull, laboratories, projects, source):
    """ biblFull xmletree -> MetaJSON Document """
    if biblfull is None:
        return None

    document = Document()

    # titleStmt
    tei_titlestmt = biblfull.find(xmletree.prefixtag("tei", "titleStmt"))
    # editionStmt
    tei_editionstmt = biblfull.find(xmletree.prefixtag("tei", "editionStmt"))
    # extent
    tei_extent = biblfull.find(xmletree.prefixtag("tei", "extent"))
    # publicationStmt
    tei_publicationstmt = biblfull.find(xmletree.prefixtag("tei", "publicationStmt"))
    # seriesStmt
    tei_seriesstmt = biblfull.find(xmletree.prefixtag("tei", "seriesStmt"))
    # notesStmt
    tei_notesstmt = biblfull.find(xmletree.prefixtag("tei", "notesStmt"))
    # sourceDesc
    tei_sourcedescs = biblfull.findall(xmletree.prefixtag("tei", "sourceDesc"))
    # profileDesc
    tei_profiledesc = biblfull.find(xmletree.prefixtag("tei", "profileDesc"))
    tei_langusage = tei_profiledesc.find(xmletree.prefixtag("tei", "langUsage"))
    tei_languages = tei_langusage.findall(xmletree.prefixtag("tei", "language"))
    tei_textclass = tei_profiledesc.find(xmletree.prefixtag("tei", "textClass"))
    tei_keywords = tei_textclass.findall(xmletree.prefixtag("tei", "keywords"))
    tei_classcodes = tei_textclass.findall(xmletree.prefixtag("tei", "classCode"))

    # language
    doc_language = None
    if tei_languages:
        languages = []
        for tei_language in tei_languages:
            language = tei_language.get("ident")
            languages.append(language)
        if languages:
            document["languages"] = languages
            doc_language = languages[0]

    # title
    document.update(get_tei_titles_to_metason(tei_titlestmt, doc_language))

    metajson_service.pretty_print_document(document)
    metajson_service.print_document(document)
    return document


def get_tei_titles_to_metason(tei_element, doc_language):
    result = {}
    title_translated_dict = {}
    title_abbreviated_list = []

    tei_titles = tei_element.findall(xmletree.prefixtag("tei", "title"))

    for tei_title in tei_titles:
        title_type = tei_title.get("type")
        title_text = tei_title.text.strip()
        title_lang = tei_title.get(xmletree.prefixtag("xml", "lang"))

        if title_type == None:
            if title_lang == doc_language:
                result["title"] = title_text
            else:
                if title_lang in title_translated_dict:
                    title_translated = title_translated_dict[title_lang]
                else:
                    title_translated = {}
                title_translated["language"] = title_lang
                title_translated["title"] = title_text
                title_translated_dict[title_lang] = title_translated

        elif title_type == "main":
            result["title"] = title_text

        elif title_type == "alt":
            if title_lang in title_translated_dict:
                title_translated = title_translated_dict[title_lang]
            else:
                title_translated = {}
            title_translated["language"] = title_lang
            title_translated["title"] = title_text
            title_translated_dict[title_lang] = title_translated

        elif title_type == "sub":
            if title_lang == doc_language:
                result["title_sub"] = title_text
            else:
                if title_lang in title_translated_dict:
                    title_translated = title_translated_dict[title_lang]
                else:
                    title_translated = {}
                title_translated["language"] = title_lang
                title_translated["title_sub"] = title_text
                title_translated_dict[title_lang] = title_translated

        elif title_type == "short":
            title_abbreviated = {}
            title_abbreviated["language"] = title_lang
            title_abbreviated["title"] = title_text
            title_abbreviated_list.append(title_abbreviated)

    if title_translated_dict.values():
        result["title_translateds"] = title_translated_dict.values()
    if title_abbreviated_list:
        result["title_abbreviateds"] = title_abbreviated_list
    return result


def author_to_metajson_agent(author):
    pass


def org_laboratory_to_metajson(org_laboratory):
    orgunit = Orgunit()
    return orgunit


def org_project_to_metajson(org_project):
    project = Project()
    return project

