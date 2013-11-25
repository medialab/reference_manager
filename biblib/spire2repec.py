#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import os

from biblib.services import corpus_service
from biblib.util import chrono
from biblib.util import console
from biblib.util import constants
from biblib.cloud import oaipmh_harvester
from biblib.metajson import Target

console.setup_console()


def harvest_by_set(corpus, target, target_set):
    print("harvest_by_set: {}".format(target_set))
    date_begin = datetime.datetime.now()

    # harvest
    metajson_list = oaipmh_harvester.list_records(target, None, None, target_set)
    date_harvest = datetime.datetime.now()
    chrono.chrono_trace("harvest spire and convert to metajson", date_begin, date_harvest, len(ids))
    
    # import
    result_import = corpus_service.import_metajson_list(corpus, metajson_list, True, None)
    date_import = datetime.datetime.now()
    chrono.chrono_trace("harvest spire, convert metadata and save to MongoDB", date_harvest, date_import, len(result_import[0]))



def harvest_by_ids(corpus, target, ids):
    print("harvest_by_ids: {}".format(ids))
    date_begin = datetime.datetime.now()

    # harvest
    metajson_list = []
    for identifier in ids:
        metajson_list.append(oaipmh_harvester.get_record(target, identifier))
    date_harvest = datetime.datetime.now()
    chrono.chrono_trace("harvest spire and convert to metajson", date_begin, date_harvest, len(ids))

    # import
    result_import = corpus_service.import_metajson_list(corpus, metajson_list, True, None)
    date_import = datetime.datetime.now()
    chrono.chrono_trace("import", date_harvest, date_import, len(result_import))


if __name__ == "__main__":
    date_begin = datetime.datetime.now()

    # conf corpus
    corpus = "spire"
    corpus_service.clean_corpus(corpus)
    date_clean = datetime.datetime.now()
    chrono.chrono_trace("Initialize corpus", date_begin, date_clean, None)

    target = Target()
    target['identifier'] = 'spire'
    target['title'] = 'Sciences Po Institutional Repository'
    target['type'] = 'oaipmh'
    target['url'] = 'http://spire.sciences-po.fr/dissemination/oaipmh2-publications.xml'
    target['metadata_prefix'] = 'didl'

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
    harvest_by_ids(corpus, target, ids)
    #harvest_by_set(corpus, target, "SHS:STAT")

    # path
    data_result_dir = os.path.join(os.path.dirname(__file__), os.pardir, "data", "result")
    print "data_result_dir: " + data_result_dir
    error_file_path = os.path.join(data_result_dir, "result_validation_errors.txt")
    metajson_file_path = os.path.join(data_result_dir, "result_didl_metajson_spire.json")
    mods_file_path = os.path.join(data_result_dir, "result_didl_mods_spire.json")
    repec_file_path = os.path.join(data_result_dir, "result_repec.txt")

    date_path = datetime.datetime.now()

    # validate
    corpus_service.validate_corpus(corpus, error_file_path)
    date_validate = datetime.datetime.now()
    chrono.chrono_trace("Validate corpus", date_path, date_validate, None)

    # export MetaJSON
    corpus_service.export_corpus(corpus, metajson_file_path, constants.FORMAT_METAJSON, True)
    date_export_metajson = datetime.datetime.now()
    chrono.chrono_trace("Export corpus as MetaJSON", date_validate, date_export_metajson, None)

    # export MODS
    corpus_service.export_corpus(corpus, mods_file_path, constants.FORMAT_MODS, True)
    date_export_mods = datetime.datetime.now()
    chrono.chrono_trace("Export corpus as MODS", date_export_metajson, date_export_mods, None)

    # export RePEc
    corpus_service.export_corpus(corpus, repec_file_path, constants.FORMAT_REPEC, True)
    date_export_repec = datetime.datetime.now()
    chrono.chrono_trace("Export corpus as RePEc", date_export_mods, date_export_repec, None)

