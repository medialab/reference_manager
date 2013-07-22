#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import uuid
from biblib.services import crosswalks_service
from biblib.services import metajson_service
from biblib.validation import metajson_validation
from biblib.services import repository_service
from biblib.util import jsonbson


def import_endnote_files(corpus, input_files, error_file_path):
    import_metadata_files(corpus, input_files, "endnotexml", error_file_path, True)


def import_metadata_files(corpus, input_files, input_format, error_file_path, source, save):
    if corpus and input_files:
        with open(error_file_path, "w") as error_file:
            for input_file_path in input_files:
                return import_metadata_file(corpus, input_file_path, input_format, error_file, source, save)


def import_metadata_file(corpus, input_file_path, input_format, error_file, source, save):
    print "import_metadata_file"
    if corpus and input_file_path:
        print "corpus: {}".format(corpus)
        print "input_file_path: {}".format(input_file_path)
        print "input_format: {}".format(input_format)
        document_list = crosswalks_service.convert_file(input_file_path, input_format, "metajson", source, False)
        return import_metajson_list(corpus, document_list, error_file, save)


def import_metajson_list(corpus, metajson_list, error_file, save):
    print "import_metajson_list"
    results = []
    all_errors = []
    for metajson in metajson_list:
        if "rec_id" not in metajson:
            metajson["rec_id"] = str(uuid.uuid1())
        if "rec_source" not in metajson:
            metajson["rec_source"] = "unknown"

        rec_id = metajson["rec_id"]
        rec_source = metajson["rec_source"]

        metajson_service.enhance_metajson(metajson)

        errors = metajson_validation.validate_metajson_document(metajson)
        for error in errors:
            formatted_error = rec_source + ":" + rec_id + ": " + error + "\n"
            all_errors.append(formatted_error)
            if error_file:
                error_file.write(formatted_error)

        results.append(repository_service.save_document(corpus, metajson))

    return results, all_errors


def load_metajson_files(files):
    if files:
        for file_path in files:
            yield load_metajson_file(file_path)


def load_metajson_file(file_path):
    with open(file_path) as metajson_file:
        metajson = jsonbson.load_json_file(metajson_file)
        if "records" in metajson:
            for record in metajson["records"]:
                if record:
                    yield metajson_service.load_dict(record)
