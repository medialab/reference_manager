#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import os
import json
from biblib.services import repository_service
from biblib.services import config_service
from biblib.util import chrono


def init_corpus(corpus):
    if not corpus:
        print("Error: empty corpus")
    else:
        print("init corpus: {}".format(corpus))

        # clean
        date_start = datetime.datetime.now()

        repository_service.create_corpus(corpus)
        repository_service.empty_corpus(corpus)
        repository_service.init_corpus_indexes(corpus)

        # types
        init_types(corpus, "common")
        init_types(corpus, corpus)

        # datafields
        init_uifields(corpus, "common")
        init_uifields(corpus, corpus)

        date_end = datetime.datetime.now()
        chrono.chrono_trace("init_corpus", date_start, date_end, None)


def init_types(corpus, folder):
    types_dir = os.path.abspath(os.path.join(config_service.config_path, "corpus", folder, "types"))
    files = os.listdir(types_dir)
    if files:
        for file_name in os.listdir(types_dir):
            if file_name.endswith(".json"):
                with open(os.path.join(types_dir, file_name), 'r') as type_file:
                    try:
                        json_type = json.load(type_file)
                        repository_service.save_type(corpus, json_type)
                    except ValueError as e:
                        print "ERROR: Type file is not valid JSON", folder, file_name, e


def init_uifields(corpus, folder):
    uifields_dir = os.path.abspath(os.path.join(config_service.config_path, "corpus", folder, "uifields"))
    files = os.listdir(uifields_dir)
    if files:
        for file_name in os.listdir(uifields_dir):
            if file_name.endswith(".json"):
                with open(os.path.join(uifields_dir, file_name), 'r') as uifield_file:
                    try:
                        json_uifield = json.load(uifield_file)
                        repository_service.save_uifield(corpus, json_uifield)
                    except ValueError as e:
                        print "ERROR: UIField file is not valid JSON", folder, file_name, e
