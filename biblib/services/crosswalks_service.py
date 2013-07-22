#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import xml.etree.ElementTree as ET

from pybtex.database.input import bibtex

from biblib.crosswalks import bibjson_crosswalk
from biblib.crosswalks import bibtex_crosswalk
from biblib.crosswalks import ddi_crosswalk
from biblib.crosswalks import didl_crosswalk
from biblib.crosswalks import endnotexml_crosswalk
from biblib.crosswalks import mets_crosswalk
from biblib.crosswalks import mods_crosswalk
from biblib.crosswalks import openurl_crosswalk
from biblib.crosswalks import repec_crosswalk
from biblib.crosswalks import summonjson_crosswalk
from biblib.crosswalks import unixref_crosswalk
from biblib.util import constants
from biblib.util import jsonbson


def convert_native(input_data, input_format, output_format, source, only_first_record):
    if input_format is not None:
        input_type = guess_format_type(input_format)

        if input_type is not None:
            if input_type == constants.FILE_TYPE_XMLETREE:
                return convert_xmletree(input_data, input_format, output_format, source, only_first_record)
            elif input_type == constants.FILE_TYPE_JSON:
                return convert_json(input_data, input_format, output_format, source, only_first_record)
            elif input_type == constants.FILE_TYPE_BIBTEX:
                return convert_bibtex(input_data, input_format, output_format, source, only_first_record)
            elif input_type == constants.FILE_TYPE_TXT:
                print convert_txt(input_data, input_format, output_format, source, only_first_record)


def convert_file_list(input_file_list, input_format, output_format, source, only_first_record):
    for input_file in input_file_list:
        converted_file = convert_file(input_file, input_format, output_format, source, only_first_record)
        if converted_file:
            yield converted_file


def convert_file(input_file, input_format, output_format, source, only_first_record):
    # input_format type determination
    input_type = guess_format_type(input_format)
    if input_type is None:
        # file_extension type determination
        input_type = guess_file_type(input_file)

    if input_type is not None:
        if input_type == constants.FILE_TYPE_XMLETREE:
            xmlparser = ET.XMLParser(encoding="utf-8")
            xmletree_tree = ET.parse(input_file, xmlparser)
            xmletree_root = xmletree_tree.getroot()
            return convert_xmletree(xmletree_root, input_format, output_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_JSON:
            with open(input_file) as json_file:
                json_data = jsonbson.load_json_file(json_file)
                # jsonbson.load_json_str(json_file.read())
                return convert_json(json_data, input_format, output_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_BIBTEX:
            bibtex_parser = bibtex.Parser()
            bibtex_root = bibtex_parser.parse_file(input_file)
            return convert_bibtex(bibtex_root, input_format, output_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_TXT:
            with open(input_file) as txt_file:
                txt_data = txt_file.readall()
                return convert_txt(txt_data, input_format, output_format, source, only_first_record)


def convert_string(input_string, input_format, output_format, source, only_first_record):
    # input_format type determination
    input_type = guess_format_type(input_format)
    if input_type is None:
        # string type determination
        input_type = guess_string_type(input_string)

    if input_type is not None:
        if input_type == constants.FILE_TYPE_XMLETREE:
            register_namespaces()
            xmletree = ET.fromstring(input_string)
            return convert_xmletree(xmletree, input_format, output_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_JSON:
            json_data = jsonbson.load_json_str(input_string)
            return convert_json(json_data, input_format, output_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_BIBTEX:
            bibtexparser = bibtex.Parser()
            bib_data = bibtexparser.parse_file(input_string)
            return convert_bibtex(bib_data, input_format, output_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_TXT:
            return convert_txt(input_string, input_format, output_format, source, only_first_record)


def convert_bibtex(bibtex_root, input_format, output_format, source, only_first_record):
    if bibtex_root:
        metajson_list = bibtex_crosswalk.bibtex_root_to_metasjon_list(bibtex_root, source, only_first_record)

        if metajson_list:
            if output_format == constants.FORMAT_METAJSON:
                return metajson_list
            else:
                return convert_metajson_list(metajson_list, output_format)


def convert_txt(txt, input_format, output_format, source, only_first_record):
    print "Error txt crosswalks not managed"
    pass


def convert_json(jsondict, input_format, output_format, source, only_first_record):
    if jsondict is not None:
        if input_format is None:
            input_format = guess_json_format(jsondict)

        if input_format is not None:
            print "input_format: {0}".format(input_format)
            metajson_list = None
            if input_format == constants.FORMAT_METAJSON:
                metajson_list = [jsondict]
            elif input_format == constants.FORMAT_SUMMONJSON:
                metajson_list = summonjson_crosswalk.summonjson_to_metajson_list(jsondict, source, only_first_record)
            elif input_format == constants.FORMAT_BIBJSON:
                metajson_list = bibjson_crosswalk.bibjson_to_metajson_list(jsondict, source, only_first_record)
            else:
                print "Error: {} input_format not managed".format(input_format)

            if metajson_list:
                if output_format == constants.FORMAT_METAJSON:
                    return metajson_list
                else:
                    return convert_metajson_list(metajson_list, output_format)


def convert_xmletree(xmletree, input_format, output_format, source, only_first_record):
    if xmletree is not None:
        if input_format is None:
            input_format = guess_xmletree_format(xmletree)

        if input_format is not None:
            print "input_format: {0}".format(input_format)
            metajson_list = None
            if input_format == constants.FORMAT_ENDNOTEXML:
                metajson_list = endnotexml_crosswalk.endnotexml_xmletree_to_metajson_list(xmletree, source, only_first_record)
            elif input_format == constants.FORMAT_MODS:
                metajson_list = mods_crosswalk.mods_xmletree_to_metajson_list(xmletree, source, only_first_record)
            elif input_format == constants.FORMAT_DIDL:
                metajson_list = didl_crosswalk.didl_xmletree_to_metajson_list(xmletree, source, only_first_record)
            elif input_format == constants.FORMAT_DDI:
                metajson_list = ddi_crosswalk.ddi_xmletree_to_metajson_list(xmletree, source, only_first_record)
            elif input_format == constants.FORMAT_UNIXREF:
                metajson_list = unixref_crosswalk.unixref_xmletree_to_metajson_list(xmletree, source, only_first_record)
            elif input_format == constants.FORMAT_METS:
                metajson_list = mets_crosswalk.mets_xmletree_to_metajson_list(xmletree, source, only_first_record)
            else:
                print "Error: {} input_format not managed".format(input_format)

            if metajson_list:
                if output_format == constants.FORMAT_METAJSON:
                    return metajson_list
                else:
                    return convert_metajson_list(metajson_list, output_format)


def convert_metajson_list(metajson_list, output_format):
    if metajson_list:
        for metajson in metajson_list:
            yield convert_metajson(metajson, output_format)


def convert_metajson(metajson, output_format):
    if output_format == constants.FORMAT_METAJSON:
        return metajson
    elif output_format == constants.FORMAT_OPENURL:
        return openurl_crosswalk.metajson_to_openurl(metajson)
    elif output_format == constants.FORMAT_OPENURLCOINS:
        return openurl_crosswalk.metajson_to_openurlcoins(metajson)
    elif output_format == constants.FORMAT_REPEC:
        return repec_crosswalk.metajson_to_repec(metajson)
    elif output_format == constants.FORMAT_BIBTEX:
        return None


def register_namespaces():
    for key in constants.xmlns_map:
        ET.register_namespace(key, constants.xmlns_map[key])


def guess_format_type(input_format):
    if input_format and input_format in constants.input_format_to_type:
        return constants.input_format_to_type[input_format]


def guess_file_type(input_file):
    if input_file and input_file.rfind(".") != -1:
        extention = input_file[input_file.rfind(".")+1:]
        if extention in constants.file_extension_to_type:
            return constants.file_extension_to_type[extention]


def guess_string_type(string):
    # todo
    return None


def guess_json_format(jsondict):
    if jsondict is not None:
        if "rec_class" in jsondict:
            return "metajson"
        else:
            print "Error: input_format can't be determined"


def guess_xmletree_format(element):
    if element is not None:
        # input_format determination
        print "element".format(element.tag)
        if element.tag.find("{") != -1 and element.tag.rfind("}") != -1:
            xmlns = element.tag[element.tag.find("{") + 1:element.tag.rfind("}")]
            print "xmlns: {0}".format(xmlns)
            if xmlns in constants.xmlns_to_input_format:
                input_format = constants.xmlns_to_input_format[xmlns]
        else:
            if element.tag in constants.xmltag_to_input_format:
                input_format = constants.xmltag_to_input_format[element.tag]
        if input_format:
            return input_format
        else:
            print "Error: input_format can't be determined"
