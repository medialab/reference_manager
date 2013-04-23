#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import json
from util import other_util
other_util.setup_console()
import datetime
from ingest import file_ingest
from repository import mongodb_repository
from dissemination import file_export


def init_repository():
    # clean
    date_start = datetime.datetime.now()

    mongodb_repository.empty_db()
    mongodb_repository.init_indexes()

    date_clean = datetime.datetime.now()
    other_util.chrono_trace("clean", date_start, date_clean, None)

    # types
    types_dir = os.path.abspath(os.path.join(os.getcwd(), "metajson", "types"))
    print(types_dir)
    for file_name in os.listdir(types_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(types_dir, file_name), 'r') as type_file:
                json_type = json.load(type_file)
                mongodb_repository.save_type(json_type)
    date_types = datetime.datetime.now()
    other_util.chrono_trace("types", date_clean, date_types, None)

    # datafields
    datafields_ui_dir = os.path.abspath(os.path.join(os.getcwd(), "metajson", "datafields_ui"))
    print(datafields_ui_dir)
    for file_name in os.listdir(datafields_ui_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(datafields_ui_dir, file_name), 'r') as datafield_file:
                json_datafield = json.load(datafield_file)
                mongodb_repository.save_datafield(json_datafield)
    date_datafields = datetime.datetime.now()
    other_util.chrono_trace("datafields", date_types, date_datafields, None)


def import_references():
    # conf
    base_dir = "test/data/"
    #filenames = ["endnote-fusion.xml", "endnote-ref.xml", "endnote-bib.xml"]
    filenames = ["endnote-fusion.xml"]
    errors_file = base_dir + "result_validation_errors.txt"
    result_mla = base_dir + "result_mla.html"
    result_metajson = base_dir + "result_metajson.json"

    # import
    date_start = datetime.datetime.now()
    input_files = []
    for filename in filenames:
        input_files.append(base_dir + filename)

    file_ingest.import_endnote_files(input_files, errors_file)

    date_import = datetime.datetime.now()
    other_util.chrono_trace("import", date_start, date_import, None)

    # fetch
    metajson_list = mongodb_repository.get_references()

    date_fetch = datetime.datetime.now()
    other_util.chrono_trace("fetch", date_import, date_fetch, len(metajson_list))

    # export citations
    file_export.export_html_webpage(metajson_list, result_mla)

    date_citations = datetime.datetime.now()
    other_util.chrono_trace("citations", date_fetch, date_citations, len(metajson_list))

    # export json
    file_export.export_metajson(metajson_list, result_metajson)

    date_json = datetime.datetime.now()
    other_util.chrono_trace("json", date_citations, date_json, len(metajson_list))


init_repository()
import_references()
