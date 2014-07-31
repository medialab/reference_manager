#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import logging
import os

from biblib.services import corpus_service
from biblib.services import io_service
from biblib.util import chrono
from biblib.util import console
from biblib.util import constants


console.setup_console()


if __name__ == "__main__":
    date_begin = datetime.datetime.now()

    # conf params
    corpus = "num"
    source = "FNSP"
    rec_id_prefix = "sc"
    input_dir_path = os.path.join("data", "num", "input")
    input_format = constants.FORMAT_UNIMARC
    output_dir_path = os.path.join("data", "num", "output")
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)
    error_file_name = "".join(["validation-", corpus, ".txt"])
    error_file_path = os.path.join(output_dir_path, error_file_name)
    #logging.debug("error_file_path: {}".format(error_file_path))

    # conf corpus
    corpus_service.clean_corpus(corpus)
    corpus_service.conf_corpus(corpus, "aime")
    date_clean = datetime.datetime.now()
    chrono.chrono_trace("Clean and conf corpus", date_begin, date_clean, None)

    # import
    input_file_paths = io_service.get_relevant_file_list_by_format(input_dir_path, input_format)
    results = corpus_service.import_metadata_files(corpus, input_file_paths, input_format, source, rec_id_prefix, True, None)
    date_import = datetime.datetime.now()
    chrono.chrono_trace("Import corpus", date_clean, date_import, None)

    # Validate
    corpus_service.validate_corpus(corpus, error_file_path)
    date_validate = datetime.datetime.now()
    chrono.chrono_trace("Validate corpus", date_import, date_validate, None)

    # Export oai_dc
    corpus_service.export_corpus(corpus, output_dir_path, constants.FORMAT_OAI_DC, False, True)
    date_export_oai_dc = datetime.datetime.now()
    chrono.chrono_trace("Export corpus oai_dc", date_validate, date_export_oai_dc, None)

    # Export mods
    corpus_service.export_corpus(corpus, output_dir_path, constants.FORMAT_MODS, False, True)
    date_export_mods = datetime.datetime.now()
    chrono.chrono_trace("Export corpus mods", date_export_oai_dc, date_export_mods, None)

    # Export CSV
    #corpus_service.export_corpus(corpus, output_dir_path, constants.FORMAT_CSV_METAJSON, True, True)
    #date_export_csv = datetime.datetime.now()
    #chrono.chrono_trace("Export corpus csv", date_export_mods, date_export_csv, None)
