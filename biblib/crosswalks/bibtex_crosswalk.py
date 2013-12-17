#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import re

from pybtex.database.input import bibtex
from pybtex.database import BibliographyData
from pybtex.database import Person
from pybtex.database import Entry

from biblib.metajson import Document
from biblib.services import creator_service
from biblib.services import date_service
from biblib.services import metajson_service
from biblib.util import constants
from biblib.util import string

TYPE_ARTICLE = "article"
TYPE_BOOK = "book"
TYPE_BOOKLET = "booklet"
TYPE_CONFERENCE = "conference"
TYPE_ICOMM = "ICOMM"
TYPE_INBOOK = "inbook"
TYPE_INCOLLECTION = "incollection"
TYPE_INPROCEEDINGS = "inproceedings"
TYPE_MANUAL = "manual"
TYPE_MASTERSTHESIS = "mastersthesis"
TYPE_MISC = "misc"
TYPE_PHDTHESIS = "phdthesis"
TYPE_PROCEEDINGS = "proceedings"
TYPE_TECHREPORT = "techreport"
TYPE_UNPUBLISHED = "unpublished"

bibtex_document_type_to_metajson_document_type = {
    TYPE_ARTICLE: constants.DOC_TYPE_JOURNALARTICLE,
    TYPE_BOOK: constants.DOC_TYPE_BOOK,
    TYPE_BOOKLET: constants.DOC_TYPE_BOOKLET,
    TYPE_CONFERENCE: constants.DOC_TYPE_CONFERENCEPAPER,
    TYPE_ICOMM: constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    TYPE_INBOOK: constants.DOC_TYPE_BOOKPART,
    TYPE_INCOLLECTION: constants.DOC_TYPE_BOOKPART,
    TYPE_INPROCEEDINGS: constants.DOC_TYPE_CONFERENCEPAPER,
    TYPE_MANUAL: constants.DOC_TYPE_MANUEL,
    TYPE_MASTERSTHESIS: constants.DOC_TYPE_MASTERTHESIS,
    TYPE_MISC: constants.DOC_TYPE_UNPUBLISHEDDOCUMENT,
    TYPE_PHDTHESIS: constants.DOC_TYPE_DOCTORALTHESIS,
    TYPE_PROCEEDINGS: constants.DOC_TYPE_CONFERENCEPROCEEDINGS,
    TYPE_TECHREPORT: constants.DOC_TYPE_TECHREPORT,
    TYPE_UNPUBLISHED: constants.DOC_TYPE_UNPUBLISHEDDOCUMENT
}


def bibtex_root_to_metasjon_list(bibtex_root, source, only_first_record):
    for entry_key in bibtex_root.entries.keys():
        bibtex_entry = bibtex_root.entries[entry_key]
        yield bibtex_entry_to_metajson(bibtex_entry, source)


def bibtex_entry_to_metajson(entry, source):
    document = Document()
    # rec_type
    bibtex_type = entry.type
    rec_type = bibtex_document_type_to_metajson_document_type[bibtex_type]
    document["rec_type"] = rec_type

    # author -> creators
    creators = []
    authors = extract_creators(entry, "author", "aut")
    if authors:
        #logging.debug("authors: {}".format(authors))
        creators.extend(authors)

    # editor -> creators
    editors = []
    editors_edt = extract_creators(entry, "editor", "edt")
    if editors_edt:
        editors.extend(editors_edt)
    editors_pbd = extract_creators(entry, "editor", "pbd")
    if editors_pbd:
        editors.extend(editors_pbd)
    if editors:
        #logging.debug("editors: {}".format(editors))
        creators.extend(editors)

    # organization -> creators
    organizations = extract_creators(entry, "organization", "???")
    if organizations:
        #logging.debug("organizations: {}".format(organizations))
        creators.extend(organizations)

    # school -> creators
    schools = extract_creators(entry, "school", "yyy")
    if schools:
        #logging.debug("schools: {}".format(schools))
        creators.extend(schools)

    if creators:
        document["creators"] = creators

    # title
    title = get_field(entry, 'title')
    if title:
        document["title"] = title

    # year, month -> date_issued
    year = get_field(entry, 'year')
    month = get_field(entry, 'month')
    if year:
        date = year
        if month:
            try:
                if int(month) < 10:
                    month = "0" + month
            except ValueError:
                month_lower = month.lower()
                if month_lower in date_service.month_text_to_month_decimal:
                    month = date_service.month_text_to_month_decimal[month_lower]
            date += month
        document["date_issued"] = date

    # journal -> is_part_ofs
    journal = get_field(entry, 'journal')
    if journal:
        is_part_of = Document()
        is_part_of["rec_type"] = "Journal"
        is_part_of["title"] = journal
        document["is_part_ofs"] = [is_part_of]

    # booktitle -> is_part_ofs
    booktitle = get_field(entry, 'booktitle')
    if booktitle:
        is_part_of = Document()
        is_part_of["rec_type"] = "Book"
        is_part_of["title"] = booktitle
        document["is_part_ofs"] = [is_part_of]

    # abstract -> descriptions
    abstract = get_field(entry, 'abstract')
    note = get_field(entry, 'note')
    descriptions = []
    if abstract:
        descriptions.append({"language": "und", "value": abstract})
    if note:
        descriptions.append({"language": "und", "value": note})
    if descriptions:
        document["descriptions"] = descriptions

    # chapter -> part_chapter_number
    chapter = get_field(entry, 'chapter')
    if chapter:
        document["part_chapter_number"] = chapter

    # volume -> part_volume
    volume = get_field(entry, 'volume')
    if volume:
        document["part_volume"] = volume

    # number -> part_issue
    number = get_field(entry, 'number')
    if number:
        document["part_issue"] = number

    # pages -> part_page_begin, part_page_end
    pages = get_field(entry, 'pages')
    if pages:
        pages_list = pages.split("-")
        document["part_page_begin"] = pages_list[0]
        if len(pages_list) > 1:
            document["part_page_end"] = pages_list[1]

    # publisher -> publishers
    publisher = get_field(entry, 'publisher')
    if publisher:
        document["publishers"] = [publisher]

    # institution -> publishers
    institution = get_field(entry, 'institution')
    if institution:
        document["publishers"] = [institution]

    # address -> publisher_places
    address = get_field(entry, 'address')
    if address:
        document["publisher_places"] = [address]

    # howpublished
    howpublished = get_field(entry, 'howpublished')
    if howpublished:
        document["published_how"] = howpublished

    # edition -> edition
    edition = get_field(entry, 'edition')
    if edition:
        document["edition"] = edition

    # series -> todo part_number or series[0]["title"] ?
    series = get_field(entry, 'series')
    if series:
        document["part_number"] = series

    # isbn -> identifiers[].id_value = isbn
    isbn = get_field(entry, 'isbn')

    # file -> todo
    myfile = get_field(entry, 'file')

    # keywords -> todo
    keywords_field = get_field(entry, 'keywords')
    if keywords_field:
        keywords = re.split(r',', get_field(entry, 'keywords').lower())

    logging.info("# BibTeX type: {}".format(bibtex_type))
    metajson_service.pretty_print_document(document)
    return document


def extract_creators(entry, key, role):
    if key in entry.persons:
        creators = []
        authors = entry.persons[key]
        for author in authors:
            formatted_name = unicode(author).encode('utf-8')
            formatted_name = formatted_name.replace("{", "").replace("}", "")
            creator = creator_service.formatted_name_to_creator(formatted_name, "person", role)
            creators.append(creator)
            return creators
    else:
        return None


def get_field(entry, field):
    if field in entry.fields and entry.fields[field]:
        tmp = unicode(entry.fields[field]).encode('utf-8')
        tmp = tmp.replace("{", "").replace("}", "").replace("\&", "and").replace("\\", "")
        return tmp
    else:
        return None


def metajson_list_to_bibtex_root():
    pass


def metajson_to_bibtex_entry():
    pass
