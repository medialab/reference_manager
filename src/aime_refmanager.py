#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
from util import other_util
from ingest import file_ingest
from repository import mongodb_repository
from dissemination import file_export

other_util.setup_console()

def clean_import():
    # conf
    base_dir = "test/data/"
    #filenames = ["endnote-fusion.xml", "endnote-ref.xml", "endnote-bib.xml"]
    filenames = ["endnote-fusion.xml"]
    errors_file = base_dir + "result_validation_errors.txt"
    result_mla = base_dir + "result_mla.html"
    result_metajson = base_dir + "result_metajson.json"

    # clean
    date_start = datetime.datetime.now()

    mongodb_repository.empty_db()

    date_clean = datetime.datetime.now()
    other_util.chrono_trace("clean", date_start, date_clean, None)

    # import
    input_files = []
    for filename in filenames:
        input_files.append(base_dir + filename)

    file_ingest.import_endnote_files(True, input_files, errors_file)

    date_import = datetime.datetime.now()
    other_util.chrono_trace("import", date_clean, date_import, None)

    # fetch
    metajson_list = mongodb_repository.get_all()

    date_fetch = datetime.datetime.now()
    other_util.chrono_trace("fetch", date_import, date_fetch, len(metajson_list))

    # export citations
    file_export.export_html_webpage(metajson_list,result_mla)

    date_citations = datetime.datetime.now()
    other_util.chrono_trace("citations", date_fetch, date_citations, len(metajson_list))

    # export json
    file_export.export_metajson(metajson_list, result_metajson)

    date_json = datetime.datetime.now()
    other_util.chrono_trace("json", date_citations, date_json, len(metajson_list))

clean_import()
