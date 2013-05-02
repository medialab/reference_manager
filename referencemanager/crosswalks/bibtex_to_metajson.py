#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from referencemanager.metajson import Document
from referencemanager.services import contributor_service
from pybtex.database.input import bibtex
from pybtex.database import BibliographyData
from pybtex.database import Person
from pybtex.database import Entry
import re


def convert_bibtext_file_to_metasjon_document_list(bibtex_filename):
    bibtexparser = bibtex.Parser()
    bib_data = bibtexparser.parse_file(bibtex_filename)
    document_list = []
    for key in bib_data.entries.keys():
        document = convert_bibtext_entry_to_metajson_document(bib_data.entries[key], bibtex_filename)
        document_list.append(document)
    return document_list


def convert_bibtext_entry_to_metajson_document(entry, source):
    # todo convert bibtext to metajson
    document = Document()
    document["contributors"] = extract_contributors(entry)
    document["title"] = get_field(entry, 'title')
    document["date_issued"] = get_field(entry, 'year')
    is_part_of_title = get_field(entry, 'journal')
    if is_part_of_title:
        is_part_of = Document()
        is_part_of["rec_type"] = "journal"
        is_part_of["title"] = is_part_of_title
        document["is_part_of"] = [is_part_of]
    document["description"] = get_field(entry, 'abstract')

    myfile = get_field(entry, 'file')
    keywords = re.split(r',', get_field(entry, 'keywords').lower())

    return document


def extract_contributors(entry):
    if "author" in entry.persons:
        contributors = []
        authors = entry.persons["author"]
        for author in authors:
            formatted_name = unicode(author).encode('utf-8')
            formatted_name = formatted_name.replace("{", "").replace("}", "")
            contributor = contributor_service.convert_formatted_name_to_contributor(formatted_name, "person", "aut")
            contributors.append(contributor)
            return contributors
    else:
        return None


def get_field(entry, field):
    if field in entry.fields and entry.fields[field]:
        tmp = unicode(entry.fields[field]).encode('utf-8')
        tmp = tmp.replace("{", "").replace("}", "").replace("\&", "and").replace("\\", "")
        return tmp
    else:
        return None
