#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from metadatas.metajson import Common, Document, Contributor, Identifier, Resource

from pybtex.database.input import bibtex

def convert_bibtext_entry_to_metajson_document(bibtextentry, source):
    document = Document()
    # todo
    return document

def convert_bibtext_file_to_metasjon_document_list(bibtex_filename):
    bibtexparser = bibtex.Parser()
    bib_data = bibtexparser.parse_file(bibtexfilename)
    document_list = []
    for key in bib_data.entries.keys() :
      document = convert_bibtext_entry_to_metajson_document(bib_data.entries[key])
      document_list.append(document)
    return document_list
    

    