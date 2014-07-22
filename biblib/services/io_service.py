#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import collections
import csv
import logging
import os
import types
import xml.etree.ElementTree as ET

from pybtex.database.input import bibtex
from pymarc import MARCReader

from biblib.metajson import Collection
from biblib.services import metajson_service
from biblib.util import constants
from biblib.util import jsonbson
from biblib.util import xmletree


#######################
# Guess Type & Format #
#######################

def guess_type_from_format(input_format):
    if input_format and input_format in constants.format_to_file_type:
        return constants.format_to_file_type[input_format]


def guess_file_extension_from_format(input_format):
    if input_format and input_format in constants.format_to_file_type:
        input_type = constants.format_to_file_type[input_format]
        if input_type and input_type in constants.file_type_to_file_extension:
            return constants.file_type_to_file_extension[input_type]


def guess_type_from_file(input_file):
    if input_file and input_file.rfind(".") != -1:
        extention = input_file[input_file.rfind(".")+1:]
        if extention in constants.file_extension_to_file_type:
            return constants.file_extension_to_file_type[extention]


def guess_format_from_string(string):
    if string.startswith("TY  -"):
        return constants.FORMAT_RIS
    else:
        return None


def guess_format_from_txt_lines(txt_lines):
    # todo
    return None


def guess_format_from_json(json_data):
    if json_data is not None:
        if "rec_class" in json_data:
            return "metajson"
        else:
            logging.error("Error: input_format can't be determined")


def guess_format_from_xmletree(element):
    if element is not None:
        # input_format determination
        if element.tag.find("{") != -1 and element.tag.rfind("}") != -1:
            xmlns = element.tag[element.tag.find("{") + 1:element.tag.rfind("}")]
            logging.debug("xmlns: {0}".format(xmlns))
            if xmlns in constants.xmlns_to_input_format:
                input_format = constants.xmlns_to_input_format[xmlns]
        else:
            if element.tag in constants.xmltag_to_input_format:
                input_format = constants.xmltag_to_input_format[element.tag]
        if input_format:
            return input_format
        else:
            logging.error("Error: input_format can't be determined")


#############
# File list #
#############
def get_relevant_file_list_by_format(dir_path, input_format):
    file_extension = guess_file_extension_from_format(input_format)
    return get_relevant_file_list_by_extension(dir_path, file_extension)


def get_relevant_file_list_by_extension(dir_path, file_extension):
    logging.debug("Relevant file list for path : {} and file extension: {}".format(dir_path, file_extension))
    if dir_path is None or not os.path.exists(dir_path):
        logging.debug("Nonexistent directory path")
    else:
        files = os.listdir(dir_path)
        if files:
            for file_name in files:
                if not file_name.startswith('.') and file_name.endswith("." + file_extension):
                    file_path = os.path.join(dir_path, file_name)
                    logging.debug("file_path: {}".format(file_path))
                    yield file_path


#########
# Parse #
#########

def parse_bibtex(input_file_path):
    bibtex_parser = bibtex.Parser()
    return bibtex_parser.parse_file(input_file_path)


def parse_csv(input_file_path):
    with open(input_file_path, 'rb') as csv_file:
        # , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL
        return list(csv.DictReader(csv_file, delimiter=';', quotechar='"'))


def parse_json(input_file_path):
    with open(input_file_path) as json_file:
        return jsonbson.load_json_file(json_file)


def parse_json_str(input_string):
    return jsonbson.load_json_str(input_string)


def parse_marc(input_file_path):
    marc_file = open(input_file_path)
    return MARCReader(marc_file, to_unicode=False, force_utf8=False)


def parse_xmletree(input_file_path):
    xml_parser = ET.XMLParser(encoding="utf-8")
    xmletree_tree = ET.parse(input_file_path, xml_parser)
    return xmletree_tree.getroot()


def parse_xmletree_str(input_string):
    xmletree.register_namespaces()
    return ET.fromstring(input_string)


def parse_txt_lines(input_file_path):
    with open(input_file_path) as txt_file:
        return list(txt_file)


def parse_metajson_files(files):
    if files:
        for file_path in files:
            yield parse_metajson_file(file_path)


def parse_metajson_file(file_path):
    with open(file_path) as metajson_file:
        metajson = jsonbson.load_json_file(metajson_file)
        if "records" in metajson:
            for record in metajson["records"]:
                if record:
                    yield metajson_service.load_dict(record)


#########
# Write #
#########

def write_items(col_id, col_title, items, output_file_path, output_format, all_in_one_file):
    # todo: all_in_one_file
    # items have to be a list of tuple ; rec_id, metadata
    # if not all_in_one_file : output_file_path = output_file_path + rec_id
    #logging.debug("write_items type(items): {}".format(type(items)))
    if all_in_one_file:
        if isinstance(items, Collection):
            write_item(items, output_file_path, output_format)
        elif isinstance(items, ET.Element):
            write_item(items, output_file_path, output_format)
        elif isinstance(items, types.GeneratorType):
            write_item(items.next(), output_file_path, output_format)
        elif isinstance(items, collections.Iterable):
            write_item(items[0], output_file_path, output_format)
    else:
        write_list(col_id, col_title, items, output_file_path, output_format)


def write_list(col_id, col_title, items, output_file_path, output_format):
    #logging.debug("write_list type(items): {}".format(type(items)))
    output_type = guess_type_from_format(output_format)

    if output_type == constants.FILE_TYPE_HTML:
        write_html(col_id, col_title, items, output_file_path, constants.STYLE_MLA)
    else:
        count = 0
        if items is not None:
            for item in items:
                count += 1
                file_name =  item[0] + "." + output_format + "." + guess_file_extension_from_format(output_format)
                file_path = os.path.join(output_file_path, file_name)
                if not os.path.exists(output_file_path):
                    os.mkdir(output_file_path)
                write_item(item[1], file_path, output_format)


def write_item(item, output_file_path, output_format):
    #logging.debug("write_item type(item): {}".format(type(item)))
    output_type = guess_type_from_format(output_format)

    if output_type is not None:
        if output_type == constants.FILE_TYPE_JSON:
            write_json(item, output_file_path)
        elif output_type == constants.FILE_TYPE_TXT:
            write_txt(item, output_file_path)
        elif output_type == constants.FILE_TYPE_XMLETREE:
            write_xml(item, output_file_path)
        elif output_type == constants.FILE_TYPE_BIBTEX:
            write_bibtex(item, output_file_path)
        elif output_type == constants.FILE_TYPE_CSV:
            write_csv(item, output_file_path)
        else:
            logging.error("Error: output_type is not managed: {}".format(output_type))


def write_metajson_collection(col_id, col_title, items, output_file_path):
    if items:
        #logging.debug("write_metajson_collection type(items): {}".format(type(items)))
        collection = metajson_service.create_collection(col_id, col_title, items)
        write_json(collection, output_file_path)


def write_csv(item, output_file_path):
    logging.debug("write_csv type(item): {}".format(type(item)))
    with open(output_file_path, "w") as output_file:
        csvwriter = csv.DictWriter(output_file, delimiter=',', fieldnames=constants.csv_metajson_fieldnames)
        csvwriter.writeheader()
        for csv_document in item:
            csvwriter.writerow(csv_document)


def write_json(item, output_file_path):
    #logging.debug("write_json type(item): {}".format(type(item)))
    with open(output_file_path, "w") as output_file:
        dump = jsonbson.dumps_bson(item, True)
        if dump:
            output_file.write(dump)


def write_txt(item, output_file_path):
    #logging.debug("write_txt type(item): {}".format(type(item)))
    with open(output_file_path, "w") as output_file:
        for txt in item:
            if txt:
                output_file.write(txt)


def write_xml(item, output_file_path):
    #logging.debug("write_xml type(item): {}".format(type(item)))
    with open(output_file_path, "w") as output_file:
        xmletree_tree = ET.ElementTree(item)
        xmletree_tree.write(output_file, "utf-8")


def write_bibtex(item, output_file_path):
    #logging.debug("write_bibtex type(item): {}".format(type(item)))
    # todo
    logging.error("Error: write_bibtex is not working")
    pass


def write_html(item, output_file_path):
    #logging.debug("write_html type(item): {}".format(type(item)))
    with open(output_file_path, "w") as output_file:
        output_file.write(item)
