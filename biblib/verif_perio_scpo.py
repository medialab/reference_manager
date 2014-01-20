#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import csv
import datetime
import logging
import os

from stdnum import issn

from biblib.services import corpus_service
from biblib.services import repository_service
from biblib.util import chrono
from biblib.util import console
from biblib.util import constants


console.setup_console()


def validate_perios(documents):
    if documents:
        issn_duplicated = {}
        csv_file_name = "".join(["validation-", corpus, ".csv"])
        csv_file_path = os.path.join(os.path.dirname(__file__), os.pardir, "log", csv_file_name)
        with open(csv_file_path, "wb") as csv_file:
            fieldnames = ["rec_id", "title", "title_sub", "issn", "issn_status", "856_1_u", "856_1_status", "856_2_u", "856_2_status", "856_3_u", "856_3_status", "856_4_u", "856_4_status", "rel_title_status", "rel_issn_status"]
            csvwriter = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)
            csvwriter.writeheader()
            for document in documents:
                csvdict = {}
                csvdict["rec_id"] = document["rec_id"]
                if "title" in document:
                    csvdict["title"] = document["title"]
                if "title_sub" in document:
                    csvdict["title_sub"] = document["title_sub"]
                if "identifiers" in document:
                    for identifier in  document["identifiers"]:
                        if identifier["id_type"] == "issn":
                            csvdict["issn"] = identifier["value"]
                            try:
                                issn.validate(identifier["value"])
                                if identifier["value"] in issn_duplicated:
                                    csvdict["issn_status"] = "DUPLICATED"
                                else:
                                    issn_duplicated[identifier["value"]] = ""
                                    csvdict["issn_status"] = "OK"
                            except:
                                csvdict["issn_status"] = "INVALID"
                            break
                if "issn" not in csvdict:
                    csvdict["issn_status"] = "EMPTY"

                # 856 : list, status
                # revues en ligne : issn, title
                csvwriter.writerow(csvdict)



if __name__ == "__main__":
    date_begin = datetime.datetime.now()

    # conf corpus
    corpus = "perio"
    corpus_service.clean_corpus(corpus)
    corpus_service.conf_corpus(corpus, "aime")
    date_clean = datetime.datetime.now()
    chrono.chrono_trace("Clean and conf corpus", date_begin, date_clean, None)

    # import
    input_file_path = "data/unimarc/periouni.mrc"
    input_format = "unimarc"
    corpus_service.import_metadata_file(corpus, input_file_path, input_format, None, True, None)
    date_import = datetime.datetime.now()
    chrono.chrono_trace("Import corpus", date_clean, date_import, None)

    # Validate
    #error_file_name = "".join(["validation-", corpus, ".txt"])
    #error_file_path = os.path.join(os.path.dirname(__file__), os.pardir, "log", error_file_name)
    #corpus_service.validate_corpus(corpus, error_file_path)
    #date_validate = datetime.datetime.now()
    #chrono.chrono_trace("Validate corpus", date_import, date_validate, None)

    # Validate perio
    # fetch
    documents = repository_service.get_documents(corpus)
    validate_perios(documents)
    date_validate = datetime.datetime.now()
    chrono.chrono_trace("Validate perio", date_import, date_validate, None)
