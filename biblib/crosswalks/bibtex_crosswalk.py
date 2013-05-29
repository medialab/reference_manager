#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Document
from biblib.services import creator_service
from pybtex.database.input import bibtex
from pybtex.database import BibliographyData
from pybtex.database import Person
from pybtex.database import Entry
import re


def bibtex_root_to_metasjon_list(bibtex_root, source, only_first_record):
    print "bibtex_root_to_metasjon_list"
    for entry_key in bibtex_root.entries.keys():
        bibtex_entry = bibtex_root.entries[entry_key]
        metajson = bibtex_entry_to_metajson(bibtex_entry, source)
        yield metajson


def bibtex_entry_to_metajson(entry, source):
    print "bibtex_entry_to_metajson"
    # todo convert bibtext to metajson
    document = Document()
    document["creators"] = extract_creators(entry)
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


def extract_creators(entry):
    if "author" in entry.persons:
        creators = []
        authors = entry.persons["author"]
        for author in authors:
            formatted_name = unicode(author).encode('utf-8')
            formatted_name = formatted_name.replace("{", "").replace("}", "")
            creator = creator_service.formatted_name_to_creator(formatted_name, "person", "aut")
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
