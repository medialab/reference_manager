#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import os
import json
from referencemanager.services import export_service
from referencemanager.services import import_service
from referencemanager.services import repository_service
from referencemanager.util import chrono
from referencemanager.util import console

console.setup_console()


def init_repository():
    print("init_repository")
    #base_dir = os.getcwd()
    base_dir = os.path.dirname(__file__)
    print "base_dir: " + base_dir

    # clean
    date_start = datetime.datetime.now()

    repository_service.empty_db()
    repository_service.init_indexes()

    date_clean = datetime.datetime.now()
    chrono.chrono_trace("clean", date_start, date_clean, None)

    # types
    types_dir = os.path.abspath(os.path.join(base_dir, "conf", "types"))
    print(types_dir)
    for file_name in os.listdir(types_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(types_dir, file_name), 'r') as type_file:
                json_type = json.load(type_file)
                repository_service.save_type(json_type)
    date_types = datetime.datetime.now()
    chrono.chrono_trace("types", date_clean, date_types, None)

    # datafields
    datafields_ui_dir = os.path.abspath(os.path.join(base_dir, "conf", "datafields_ui"))
    print(datafields_ui_dir)
    for file_name in os.listdir(datafields_ui_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(datafields_ui_dir, file_name), 'r') as datafield_file:
                json_datafield = json.load(datafield_file)
                repository_service.save_datafield(json_datafield)
    date_datafields = datetime.datetime.now()
    chrono.chrono_trace("datafields", date_types, date_datafields, None)


def import_references():
    print("import_references")
    #base_dir = os.getcwd()
    base_dir = os.path.dirname(__file__)
    print "base_dir: " + base_dir
    base_dir = os.path.join(base_dir, os.pardir, "data")
    print "base_dir: " + base_dir

    #filenames = ["endnote-aime.xml", "endnote-ref.xml", "endnote-bib.xml"]
    filenames = ["endnote-aime.xml"]
    errors_file = os.path.join(base_dir, "result", "result_validation_errors.txt")
    result_mla = os.path.join(base_dir, "result", "result_mla.html")
    result_metajson = os.path.join(base_dir, "result", "result_metajson.json")

    # import
    date_start = datetime.datetime.now()
    input_files = []
    for filename in filenames:
        input_file = os.path.join(base_dir, "endnotexml", filename)
        input_files.append(input_file)

    import_service.import_metadata_files(input_files, "endnotexml", errors_file, True)

    date_import = datetime.datetime.now()
    chrono.chrono_trace("import", date_start, date_import, None)

    # fetch
    metajson_list = repository_service.get_references()

    date_fetch = datetime.datetime.now()
    chrono.chrono_trace("fetch", date_import, date_fetch, len(metajson_list))

    # export citations
    export_service.export_html_webpage(metajson_list, result_mla)

    date_citations = datetime.datetime.now()
    chrono.chrono_trace("citations", date_fetch, date_citations, len(metajson_list))

    # export json
    export_service.export_metajson(metajson_list, result_metajson)

    date_json = datetime.datetime.now()
    chrono.chrono_trace("json", date_citations, date_json, len(metajson_list))


init_repository()
import_references()
