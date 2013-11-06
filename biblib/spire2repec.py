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


def harvest_by_set(target_set):
    print("harvest_by_set: {}".format(target_set))
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


def harvest_by_ids(ids):
    print("harvest_by_ids: {}".format(ids))

    date_begin = datetime.datetime.now()

    data_dir = os.path.join(os.path.dirname(__file__), os.pardir, "data")
    print "data_dir: " + data_dir
    error_file_path = os.path.join(data_dir, "result", "result_validation_errors.txt")
    result_file_path = os.path.join(data_dir, "result", "result_didl_metajson_spire.json")

    target = Target()
    target['identifier'] = 'spire'
    target['title'] = 'Sciences Po Institutional Repository'
    target['type'] = 'oaipmh'
    target['url'] = 'http://spire.sciences-po.fr/dissemination/oaipmh2-publications.xml'
    target['metadata_prefix'] = 'didl'

    # harvest
    results = []
    for identifier in ids:
        results.append(oaipmh_harvester.get_record(target,identifier))

    date_import = datetime.datetime.now()
    chrono.chrono_trace("harvest spire and convert to metajson", date_begin, date_import, len(ids))

    # export
    export_service.export_metajson_collection("test", "test", results, result_file_path)
    date_export = datetime.datetime.now()
    chrono.chrono_trace("Export collection", date_import, date_export, len(ids))

if __name__ == "__main__":
    ids = [
        "oai:spire.sciences-po.fr:2441/dambferfb7dfprc9m26c8c8o3",
        "oai:spire.sciences-po.fr:2441/eo6779thqgm5r489makgoai85",
        "oai:spire.sciences-po.fr:2441/5l6uh8ogmqildh09h6m8hj429",
        "oai:spire.sciences-po.fr:2441/3fm4jv3k2s99lms9jb5i5asil",
        "oai:spire.sciences-po.fr:2441/f4rshpf3v1umfa09lb0joe5g5",
        "oai:spire.sciences-po.fr:2441/dambferfb7dfprc9m2h2og5ig",
        "oai:spire.sciences-po.fr:2441/53r60a8s3kup1vc9k0skmec8o",
        "oai:spire.sciences-po.fr:2441/eo6779thqgm5r489matggisrp",
        "oai:spire.sciences-po.fr:2441/eo6779thqgm5r489m6ock14ik",
        "oai:spire.sciences-po.fr:2441/eo6779thqgm5r489mam352ps9",
        "oai:spire.sciences-po.fr:2441/eo6779thqgm5r489m4m2k6d4l",
        "oai:spire.sciences-po.fr:2441/7t638g2jjsquujs9mcc0mcg2k",
        "oai:spire.sciences-po.fr:2441/eu4vqp9ompqllr09hh1amcck6",
        "oai:spire.sciences-po.fr:2441/c8dmi8nm4pdjkuc9g8mb1088n",
        "oai:spire.sciences-po.fr:2441/5rkqqmvrn4tl22s9mc0sob64l",
        "oai:spire.sciences-po.fr:2441/eu4vqp9ompqllr09hd5rha0il",
        "oai:spire.sciences-po.fr:2441/eu4vqp9ompqllr09ij4jnag10",
        "oai:spire.sciences-po.fr:2441/dambferfb7dfprc9lj6bo200k",
        "oai:spire.sciences-po.fr:2441/c6t1fl36hv9s7q89j8pa2cp3i"
    ]
    harvest_by_ids(ids)
