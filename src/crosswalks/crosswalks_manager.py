#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from crosswalks import metajson_to_openurl

def convert_document(input_data, input_format, output_data):
    if input_format == "metajson":

        if output_format == "openurl":
            return metajson_to_openurl.convert_metajson_document_to_openurl(input_data)

    elif input_format == "bibtex":
        pass
        # todo
    

def convert_file(input_file, input_format, output_format):
    metajson_document_list = None

    # convert to metajson
    if input_format == "endnote":
        metajson_document_list = endnote_to_metajson.convert_endnote_file_to_metajson_document_list(input_data)

    elif input_format == "bibtex":

    # export to the output_format
    if output_format == "metajson":
        
        return metajson_document_list