#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import os
from biblib.services import crosswalks_service
from biblib.services import export_service
from biblib.services import import_service
from biblib.services import repository_service
from biblib.util import chrono
from biblib.util import console
from biblib.util import constants
from biblib import init_corpus
from biblib.cloud import oaipmh_harvester
from biblib.metajson import Target

console.setup_console()


def main():
    print("spire2repec")
    # init corpus
    date_begin = datetime.datetime.now()

    data_dir = os.path.join(os.path.dirname(__file__), os.pardir, "data")
    print "data_dir: " + data_dir
    error_file_path = os.path.join(data_dir, "result", "result_validation_errors.txt")
    result_file_path = os.path.join(data_dir, "result", "result_repec.txt")

    target = Target()
    target['identifier'] = 'spire'
    target['title'] = 'Sciences Po Institutional Repository'
    target['type'] = 'oaipmh'
    target['url'] = 'http://spire.sciences-po.fr/dissemination/oaipmh2-publications.xml'
    target['metadata_prefix'] = 'didl'
    #target_set = 'SHS:ECO'
    target_set = 'SHS:STAT'

    corpus = "spire"
    init_corpus.init(corpus)

    date_init = datetime.datetime.now()
    chrono.chrono_trace("Initialize corpus", date_begin, date_init, None)

    # import
    with open(error_file_path, "w") as error_file:
        result_import = import_service.import_metajson_list(corpus, oaipmh_harvester.list_records(target, None, None, target_set), error_file, True, None)
    date_import = datetime.datetime.now()
    chrono.chrono_trace("harvest spire, convert metadata and save to MongoDB", date_init, date_import, len(result_import[0]))

    # fetch MongoDB
    metajson_list = repository_service.get_documents(corpus)
    date_fetch = datetime.datetime.now()
    chrono.chrono_trace("Fetch MongoDB", date_import, date_fetch, len(metajson_list))

    # export RePEc template
    export_service.export_textline(crosswalks_service.convert_metajson_list(metajson_list, constants.FORMAT_REPEC), result_file_path)
    date_export = datetime.datetime.now()
    chrono.chrono_trace("Export RePEc publications templates", date_fetch, date_export, None)


if __name__ == "__main__":
    main()
