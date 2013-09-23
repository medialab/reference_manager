#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os

from biblib.services import crosswalks_service
from biblib.services import export_service
from biblib.util import constants
from biblib.util import console


def input_format_to_file_extension(input_format):
    if input_format and input_format in constants.input_format_to_type:
        input_type = constants.input_format_to_type[input_format]
        if input_type and input_type in constants.type_to_file_extension:
            return constants.type_to_file_extension[input_type]


def relevant_file_list(dir_path, file_extension):
    print "Relevant file list for path : {0}".format(dir_path)
    if dir_path is None or not os.path.exists(dir_path):
        print "Nonexistent directory path"
    else:
        files = os.listdir(dir_path)
        if files:
            for file_name in files:
                print file_name
                if not file_name.startswith('.') and file_name.endswith("." + file_extension):
                    file_path = os.path.join(dir_path, file_name)
                    print file_path
                    yield file_path


def test_crosswalk(input_format):
    print "*** Test crosswalk : {0}".format(input_format)
    base_dir = os.path.join(os.getcwd(), "data")
    input_dir = os.path.join(base_dir, input_format)
    output_path = os.path.join(base_dir, "result", "result_" + input_format + "_metajon.json")

    file_extension = input_format_to_file_extension(input_format)
    file_list = relevant_file_list(input_dir, file_extension)
    if file_list:
        metajson_list = crosswalks_service.convert_file_list(file_list, input_format, "metajson", "test", False)
        print export_service.export_metajson_collection("test_" + input_format, "Test " + input_format, metajson_list, output_path)


def test():
    test_crosswalk(constants.FORMAT_BIBTEX)
    test_crosswalk(constants.FORMAT_DIDL)
    test_crosswalk(constants.FORMAT_DDI)
    test_crosswalk(constants.FORMAT_ENDNOTEXML)
    test_crosswalk(constants.FORMAT_METS)
    test_crosswalk(constants.FORMAT_MODS)
    test_crosswalk(constants.FORMAT_RESEARCHERML)
    test_crosswalk(constants.FORMAT_RIS)
    test_crosswalk(constants.FORMAT_SUMMONJSON)
    test_crosswalk(constants.FORMAT_UNIMARC)
    test_crosswalk(constants.FORMAT_UNIXREF)

console.setup_console()
test()
