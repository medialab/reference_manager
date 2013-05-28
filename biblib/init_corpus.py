#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import os
import json
from biblib.services import repository_service
from biblib.util import chrono
from biblib.util import console

console.setup_console()


def init(corpus):
    if not corpus:
        print("Error: empty corpus")
    else:
        print("init corpus: {}".format(corpus))
        #base_dir = os.getcwd()
        base_dir = os.path.dirname(__file__)
        print "base_dir: " + base_dir

        # clean
        date_start = datetime.datetime.now()

        repository_service.create_corpus(corpus)
        repository_service.empty_corpus(corpus)
        repository_service.init_corpus_indexes(corpus)

        date_clean = datetime.datetime.now()
        chrono.chrono_trace("clean", date_start, date_clean, None)

        # types
        types_dir = os.path.abspath(os.path.join(base_dir, "conf", "types"))
        print(types_dir)
        for file_name in os.listdir(types_dir):
            if file_name.endswith(".json"):
                with open(os.path.join(types_dir, file_name), 'r') as type_file:
                    json_type = json.load(type_file)
                    repository_service.save_type(corpus, json_type)
        date_types = datetime.datetime.now()
        chrono.chrono_trace("types", date_clean, date_types, None)

        # datafields
        uifields_dir = os.path.abspath(os.path.join(base_dir, "conf", "uifields"))
        print(uifields_dir)
        for file_name in os.listdir(uifields_dir):
            if file_name.endswith(".json"):
                with open(os.path.join(uifields_dir, file_name), 'r') as uifield_file:
                    json_uifield = json.load(uifield_file)
                    repository_service.save_uifield(corpus, json_uifield)
        date_uifields = datetime.datetime.now()
        chrono.chrono_trace("uifields", date_types, date_uifields, None)
