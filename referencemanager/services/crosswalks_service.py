#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from referencemanager.crosswalks import bibtex_to_metajson
from referencemanager.crosswalks import crossref_unixref_to_metajson
from referencemanager.crosswalks import endnote_to_metajson
from referencemanager.crosswalks import metajson_to_openurl
from referencemanager.crosswalks import mods_to_metajson
from referencemanager.crosswalks import summon_json_to_metajson


def convert_document(input_data, input_format, output_format, source):
    # 1: Convert to metajson
    if input_format == "metajson":
        metajson_document = input_data
    elif input_format == "bibtex":
        metajson_document = bibtex_to_metajson.convert_bibtext_entry_to_metajson_document(input_data)
    elif input_format == "unixref":
        metajson_document = crossref_unixref_to_metajson.convert_crossref_unixref_record_to_metajson_document(input_data)
    elif input_format == "mods":
        metajson_document = mods_to_metajson.convert_mods_string_to_metajson_document(input_data, source)
    elif input_format == "summonjson":
        metajson_document = summon_json_to_metajson.convert_summon_json_document_to_metajson_document(input_data)

    if metajson_document is not None:
        if output_format == "metajson":
            return metajson_document
        if output_format == "openurl":
            return metajson_to_openurl.convert_metajson_document_to_openurl(metajson_document)
        elif output_format == "bibtex":
            return None
        # todo


def convert_file(input_file, input_format, output_format):
    if input_format is None:
        # todo : file_extension type determination
        print "Unknown input_format"
        pass

    metajson_document_list = None

    # convert to metajson
    if input_format == "endnotexml":
        metajson_document_list = endnote_to_metajson.convert_endnote_file_to_metajson_document_list(input_file)

    elif input_format == "bibtex":
        pass
    # export to the output_format
    if output_format is None or output_format == "metajson":
        return metajson_document_list


def convert_stream(input_stream, input_format, output_format, source):
    # todo
    pass
