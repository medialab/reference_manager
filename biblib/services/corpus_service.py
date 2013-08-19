#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import os
from biblib.services import repository_service
from biblib.services import config_service
from biblib.util import chrono
from biblib.util import jsonbson


def clean_corpus(corpus):
    if not corpus:
        print("Error: empty corpus")
    else:
        print("clean corpus: {}".format(corpus))

        date_start = datetime.datetime.now()

        repository_service.create_corpus(corpus)
        repository_service.empty_corpus(corpus)
        repository_service.init_corpus_indexes(corpus)

        date_end = datetime.datetime.now()
        chrono.chrono_trace("clean_corpus", date_start, date_end, None)


def conf_corpus(corpus):
    if not corpus:
        print("Error: empty corpus")
    else:
        print("init corpus: {}".format(corpus))

        date_start = datetime.datetime.now()

        # types
        results_types_common = conf_types(corpus, "common")
        results_types_corpus = conf_types(corpus, corpus)
        date_types = datetime.datetime.now()
        total_count = 0
        print "# types common:"
        if results_types_common:
            for entry in results_types_common:
                total_count += 1
                print "type_id: {}, _id: {}".format(entry["type_id"], entry["_id"])
        else:
            print "Empty common types"
        print "# types corpus:"
        if results_types_corpus:
            for entry in results_types_corpus:
                total_count += 1
                print "type_id: {}, _id: {}".format(entry["type_id"], entry["_id"])
        else:
            print "Empty corpus types"
        chrono.chrono_trace("conf_types", date_start, date_types, total_count)

        # datafields
        results_uifields_common = conf_uifields(corpus, "common")
        results_uifields_corpus = conf_uifields(corpus, corpus)
        date_uifields = datetime.datetime.now()
        total_count = 0
        print "# uifields common:"
        if results_uifields_common:
            for entry in results_uifields_common:
                total_count += 1
                print "rec_type: {}, _id: {}".format(entry["rec_type"], entry["_id"])
        else:
            print "Empty common uifields"
        print "# uifields corpus:"
        if results_uifields_corpus:
            for entry in results_uifields_corpus:
                total_count += 1
                print "rec_type: {}, _id: {}".format(entry["rec_type"], entry["_id"])
        else:
            print "Empty corpus uifields"
        chrono.chrono_trace("conf_uifields", date_types, date_uifields, total_count)


def conf_types(corpus, folder):
    types_dir = os.path.abspath(os.path.join(config_service.config_path, "corpus", folder, "types"))
    if os.path.exists(types_dir):
        files = os.listdir(types_dir)
        if files:
            results = []
            for file_name in os.listdir(types_dir):
                if file_name.endswith(".json"):
                    with open(os.path.join(types_dir, file_name), 'r') as type_file:
                        try:
                            json_type = jsonbson.load_json_file(type_file)
                            results.append(repository_service.save_type(corpus, json_type))
                        except ValueError as e:
                            print "ERROR: Type file is not valid JSON", folder, file_name, e
            return results


def conf_uifields(corpus, folder):
    uifields_dir = os.path.abspath(os.path.join(config_service.config_path, "corpus", folder, "uifields"))
    if os.path.exists(uifields_dir):
        files = os.listdir(uifields_dir)
        if files:
            results = []
            for file_name in os.listdir(uifields_dir):
                if file_name.endswith(".json"):
                    with open(os.path.join(uifields_dir, file_name), 'r') as uifield_file:
                        try:
                            json_uifield = jsonbson.load_json_file(uifield_file)
                            results.append(repository_service.save_uifield(corpus, json_uifield))
                        except ValueError as e:
                            print "ERROR: UIField file is not valid JSON", folder, file_name, e
            return results
