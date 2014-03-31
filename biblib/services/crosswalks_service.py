#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging

from biblib.crosswalks import bibjson_crosswalk
from biblib.crosswalks import bibtex_crosswalk
from biblib.crosswalks import csv_crosswalk
from biblib.crosswalks import ddi_crosswalk
from biblib.crosswalks import didl_crosswalk
from biblib.crosswalks import endnotexml_crosswalk
from biblib.crosswalks import mets_crosswalk
from biblib.crosswalks import mods_crosswalk
from biblib.crosswalks import openurl_crosswalk
from biblib.crosswalks import repec_crosswalk
from biblib.crosswalks import researcherml_crosswalk
from biblib.crosswalks import ris_crosswalk
from biblib.crosswalks import summonjson_crosswalk
from biblib.crosswalks import tei_crosswalk
from biblib.crosswalks import unimarc_crosswalk
from biblib.crosswalks import unixref_crosswalk
from biblib.services import io_service
from biblib.services import metajson_service
from biblib.util import constants


###########
# Convert #
###########

def convert_native(input_data, input_format, output_format, source, only_first_record, all_in_one_file):
    """ Convert native format
        xml : xmletree root element
        json : dict
        bibtex : bibtex root
        txt : list of line
    """
    if input_format is not None:
        input_type = io_service.guess_type_from_format(input_format)

        if input_type is not None:
            metajson_list = None
            if input_type == constants.FILE_TYPE_XMLETREE:
                # xml
                metajson_list = convert_xmletree(input_data, input_format, source, only_first_record)

            elif input_type == constants.FILE_TYPE_JSON:
                # json
                metajson_list = convert_json(input_data, input_format, source, only_first_record)

            elif input_type == constants.FILE_TYPE_BIBTEX:
                # bibtex
                metajson_list = convert_bibtext(input_data, input_format, source, only_first_record)

            elif input_type == constants.FILE_TYPE_TXT:
                # txt
                metajson_list = convert_txt_lines(input_data, input_format, source, only_first_record)

            elif input_type == constants.FILE_TYPE_CSV:
                # csv
                metajson_list = convert_csv(input_data, input_format, source, only_first_record)

            elif input_type == constants.FILE_TYPE_MARC:
                # marc
                metajson_list = convert_marc(input_data, input_format, source, only_first_record)

            if metajson_list:
                # enhance metajson list
                metajson_list = metajson_service.enhance_metajson_list(metajson_list)
                return convert_metajson_list(metajson_list, output_format, all_in_one_file)


def convert_bibtext(input_data, input_format, source, only_first_record):
    return bibtex_crosswalk.bibtex_root_to_metasjon_list(input_data, source, only_first_record)


def convert_csv(input_data, input_format, source, only_first_record):
    return csv_crosswalk.csv_dict_reader_to_metasjon_list(input_data, input_format, source, only_first_record)


def convert_json(input_data, input_format, source, only_first_record):
    if input_data is not None:
        if input_format is None:
            input_format = io_service.guess_format_from_json(input_data)

        if input_format is not None:
            logging.info("input_format: {0}".format(input_format))

            if input_format == constants.FORMAT_METAJSON:
                # metajson
                if input_data["rec_class"] == constants.CLASS_COLLECTION:
                    return input_data["records"]
                else:
                    return [input_data]

            elif input_format == constants.FORMAT_BIBJSON:
                # bibjson
                return bibjson_crosswalk.bibjson_to_metajson_list(input_data, source, only_first_record)

            elif input_format == constants.FORMAT_SUMMONJSON:
                # summon
                return summonjson_crosswalk.summonjson_to_metajson_list(input_data, source, only_first_record)
 
            else:
                logging.error("Error: {} input_format not managed".format(input_format))


def convert_marc(input_data, input_format, source, only_first_record):
    return unimarc_crosswalk.unimarc_marcreader_to_metasjon_list(input_data, source, only_first_record)


def convert_metajson_list(metajson_list, output_format, all_in_one_file):
    if metajson_list:
        if all_in_one_file:
            if output_format == constants.FORMAT_METAJSON or output_format == constants.FORMAT_HTML:
                yield metajson_service.create_collection(None, None, metajson_list)

            elif output_format == constants.FORMAT_MODS:
                yield mods_crosswalk.metajson_list_to_mods_xmletree(metajson_list)

            elif output_format == constants.FORMAT_REPEC:
                yield repec_crosswalk.metajson_list_to_repec(metajson_list)

            else:
                logging.error("ERROR Not managed format: {}".format(output_format))
        else:
            for metajson in metajson_list:
                yield convert_metajson(metajson, output_format)


def convert_metajson(metajson, output_format):
    if output_format == constants.FORMAT_METAJSON or output_format == constants.FORMAT_HTML:
        return metajson

    elif output_format == constants.FORMAT_OPENURL:
        # openurl
        return openurl_crosswalk.metajson_to_openurl(metajson)

    elif output_format == constants.FORMAT_OPENURLCOINS:
        # openurlcoins
        return openurl_crosswalk.metajson_to_openurlcoins(metajson)

    elif output_format == constants.FORMAT_REPEC:
        # repec
        return repec_crosswalk.metajson_to_repec(metajson)

    elif output_format == constants.FORMAT_MODS:
        # mods
        return mods_crosswalk.metajson_to_mods_xmletree(metajson)

    elif output_format == constants.FORMAT_BIBTEX:
        # bibtex
        return bibtex_crosswalk.metajson_to_bibtex_entry(metajson)

    else:
        logging.error("ERROR Not managed format: {}".format(output_format))


def convert_txt_lines(txt_lines, input_format, source, only_first_record):
    if txt_lines is not None:
        #if input_format is None:
        #    input_format = io_service.guess_format_from_txt_lines(txt_lines)

        if input_format is not None:
            logging.info("input_format: {0}".format(input_format))
            if input_format == constants.FORMAT_RIS:
                return ris_crosswalk.ris_txt_lines_to_metajson_list(txt_lines, source, only_first_record)
            else:
                logging.error("Error: {} input_format not managed".format(input_format))


def convert_xmletree(xmletree_root, input_format, source, only_first_record):
    if xmletree_root is not None:
        if input_format is None:
            input_format = io_service.guess_format_from_xmletree(xmletree_root)

        if input_format is not None:
            logging.info("# input_format: {0}".format(input_format))

            if input_format == constants.FORMAT_DDI:
                # ddi
                return ddi_crosswalk.ddi_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            elif input_format == constants.FORMAT_DIDL:
                # didl
                return didl_crosswalk.didl_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            elif input_format == constants.FORMAT_ENDNOTEXML:
                # endnotexml
                return endnotexml_crosswalk.endnotexml_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            elif input_format == constants.FORMAT_METS:
                # mets
                return mets_crosswalk.mets_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            elif input_format == constants.FORMAT_MODS:
                # mods
                return mods_crosswalk.mods_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            elif input_format == constants.FORMAT_OPENURL:
                # openurl
                return openurl_crosswalk.openurl_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            elif input_format == constants.FORMAT_RESEARCHERML:
                # researcherml
                return researcherml_crosswalk.researcherml_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            elif input_format == constants.FORMAT_TEI:
                # tei
                return tei_crosswalk.tei_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            elif input_format == constants.FORMAT_UNIXREF:
                # unixref
                return unixref_crosswalk.unixref_xmletree_to_metajson_list(xmletree_root, source, only_first_record)

            else:
                logging.error("Error: {} input_format not managed".format(input_format))



#########
# Parse #
#########

def parse_and_convert_file_list(input_file_path_list, input_format, output_format, source, only_first_record, all_in_one_file):
    """ Convert from a list of file path """
    results = []
    for input_file_path in input_file_path_list:
        file_results = parse_and_convert_file(input_file_path, input_format, output_format, source, only_first_record, False)
        if file_results:
            results.extend(file_results)
    if results:
        if not all_in_one_file:
            return results

        else:
            if output_format == constants.FORMAT_METAJSON or output_format == constants.FORMAT_HTML:
                return metajson_service.create_collection(None, None, results)

            elif output_format == constants.FORMAT_MODS:
                return mods_crosswalk.create_mods_collection_xmletree(results)        
            else:
                logging.error("ERROR Not managed format: {}".format(output_format))


def parse_and_convert_file(input_file_path, input_format, output_format, source, only_first_record, all_in_one_file):
    """ Convert from a file path """
    # input_format type determination
    input_type = io_service.guess_type_from_format(input_format)

    if input_type is None:
        # file_extension type determination
        input_type = io_service.guess_type_from_file(input_file_path)

    logging.info("parse_and_convert_file input_file_path: {}; input_format: {}; input_type: {}".format(input_file_path, input_format, input_type))
    if input_type is not None:
        metajson_list = None
        if input_type == constants.FILE_TYPE_XMLETREE:
            # xml
            metajson_list = parse_and_convert_xmletree(input_file_path, input_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_JSON:
            # json
            metajson_list = parse_and_convert_json(input_file_path, input_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_BIBTEX:
            # bibtex
            metajson_list = parse_and_convert_bibtex(input_file_path, input_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_TXT:
            # txt
            metajson_list = parse_and_convert_txt_lines(input_file_path, input_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_MARC:
            # marc
            metajson_list = parse_and_convert_marc(input_file_path, input_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_CSV:
            # csv
            metajson_list = parse_and_convert_csv(input_file_path, input_format, source, only_first_record)

        if metajson_list:
            # enhance metajson list
            metajson_list = metajson_service.enhance_metajson_list(metajson_list)
            return convert_metajson_list(metajson_list, output_format, all_in_one_file)


def parse_and_convert_string(input_string, input_format, output_format, source, only_first_record, all_in_one_file):
    # input_format type determination
    input_type = io_service.guess_type_from_format(input_format)
    if input_type is None:
        # string type determination
        input_type = io_service.guess_format_from_string(input_string)

    if input_type is not None:
        metajson_list = None
        if input_type == constants.FILE_TYPE_XMLETREE:
            # xml
            metajson_list =  parse_and_convert_xmletree_str(input_string, input_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_JSON:
            # json
            metajson_list = parse_and_convert_json_str(input_string, input_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_BIBTEX:
            # bibtex
            metajson_list = parse_and_convert_bibtex(input_string, input_format, source, only_first_record)

        elif input_type == constants.FILE_TYPE_TXT:
            # txt
            metajson_list = parse_and_convert_txt_lines(input_string.splitlines(), input_format, source, only_first_record)

        if metajson_list:
            # enhance metajson list
            metajson_list = metajson_service.enhance_metajson_list(metajson_list)
            return convert_metajson_list(metajson_list, output_format, all_in_one_file)


def parse_and_convert_bibtex(input_file_path, input_format, source, only_first_record):
    bibtex_root = io_service.parse_bibtex(input_file_path)
    return convert_bibtext(bibtex_root, input_format, source, only_first_record)


def parse_and_convert_csv(input_file_path, input_format, source, only_first_record):
    try:
        csv_dict_reader = io_service.parse_csv(input_file_path)
        return convert_csv(csv_dict_reader, input_format, source, only_first_record)
    finally:
        pass

def parse_and_convert_json(input_file_path, input_format, source, only_first_record):
    json_data = io_service.parse_json(input_file_path)
    return convert_json(json_data, input_format, source, only_first_record)


def parse_and_convert_json_str(input_string, input_format, source, only_first_record):
    json_data = io_service.parse_json_str(input_string)
    return convert_json(json_data, input_format, source, only_first_record)


def parse_and_convert_marc(input_file_path, input_format, source, only_first_record):
    try:
        marc_reader = io_service.parse_marc(input_file_path)
        return convert_marc(marc_reader, input_format, source, only_first_record)
    finally:
        pass


def parse_and_convert_txt_lines(input_file_path, input_format, source, only_first_record):
    txt_lines = io_service.parse_txt_lines(input_file_path)
    return convert_txt_lines(txt_lines, input_format, source, only_first_record)


def parse_and_convert_xmletree(input_file_path, input_format, source, only_first_record):
    xmletree_root = io_service.parse_xmletree(input_file_path)
    return convert_xmletree(xmletree_root, input_format, source, only_first_record)


def parse_and_convert_xmletree_str(input_string, input_format, source, only_first_record):
    xmletree_root = io_service.parse_xmletree_str(input_string)
    return convert_xmletree(xmletree_root, input_format, source, only_first_record)
