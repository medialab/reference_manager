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

        date_begin = datetime.datetime.now()

        repository_service.create_corpus(corpus)
        repository_service.empty_corpus(corpus)
        repository_service.init_corpus_indexes(corpus)

        date_end = datetime.datetime.now()
        chrono.chrono_trace("clean_corpus", date_begin, date_end, None)


def conf_corpus(corpus):
    if not corpus:
        print("Error: empty corpus")
    else:
        print("init corpus: {}".format(corpus))

        date_begin = datetime.datetime.now()

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
        chrono.chrono_trace("conf_types", date_begin, date_types, total_count)

        # datafields
        results_fields_common = conf_fields(corpus, "common")
        results_fields_corpus = conf_fields(corpus, corpus)
        date_fields = datetime.datetime.now()
        total_count = 0
        print "# fields common:"
        if results_fields_common:
            for entry in results_fields_common:
                total_count += 1
                print "rec_type: {}, _id: {}".format(entry["rec_type"], entry["_id"])
        else:
            print "Empty common fields"
        print "# fields corpus:"
        if results_fields_corpus:
            for entry in results_fields_corpus:
                total_count += 1
                print "rec_type: {}, _id: {}".format(entry["rec_type"], entry["_id"])
        else:
            print "Empty corpus fields"
        chrono.chrono_trace("conf_fields", date_types, date_fields, total_count)


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


def conf_fields(corpus, folder):
    fields_dir = os.path.abspath(os.path.join(config_service.config_path, "corpus", folder, "fields"))
    if os.path.exists(fields_dir):
        files = os.listdir(fields_dir)
        if files:
            results = []
            for file_name in os.listdir(fields_dir):
                if file_name.endswith(".json"):
                    with open(os.path.join(fields_dir, file_name), 'r') as field_file:
                        try:
                            json_field = jsonbson.load_json_file(field_file)
                            results.append(repository_service.save_field(corpus, json_field))
                        except ValueError as e:
                            print "ERROR: Field file is not valid JSON", folder, file_name, e
            return results
