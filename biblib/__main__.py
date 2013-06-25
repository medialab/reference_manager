#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import os
from biblib.services import export_service
from biblib.services import import_service
from biblib.services import repository_service
from biblib.services import config_service
from biblib.util import chrono
from biblib.util import console
from biblib import init_corpus

console.setup_console()


def import_references(corpus):
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
    result_metajson = os.path.join(base_dir, "result", "result_aime_metajson.json")

    # import
    date_start = datetime.datetime.now()
    input_files = []
    for filename in filenames:
        input_file = os.path.join(base_dir, "endnotexml", filename)
        input_files.append(input_file)

    import_service.import_metadata_files(corpus, input_files, "endnotexml", errors_file, "EndNote XML File", True)

    date_import = datetime.datetime.now()
    chrono.chrono_trace("import", date_start, date_import, None)

    # fetch
    metajson_list = repository_service.get_documents(corpus)

    date_fetch = datetime.datetime.now()
    chrono.chrono_trace("fetch", date_import, date_fetch, len(metajson_list))

    # export citations
    export_service.export_html_webpage(metajson_list, result_mla)

    date_citations = datetime.datetime.now()
    chrono.chrono_trace("citations", date_fetch, date_citations, len(metajson_list))

    # export json
    export_service.export_metajson_collection("aime", "AIME references", metajson_list, result_metajson)

    date_json = datetime.datetime.now()
    chrono.chrono_trace("json", date_citations, date_json, len(metajson_list))


default_corpus = config_service.config["mongodb"]["default_corpus"]
init_corpus.init(default_corpus)
import_references(default_corpus)
