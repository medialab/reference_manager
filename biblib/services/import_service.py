#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from biblib.services import crosswalks_service
from biblib.services import metajson_service
from biblib.validation import metajson_validation
from biblib.services import repository_service


def import_endnote_files(corpus, files, error_file_path):
    import_metadata_files(corpus, files, "endnotexml", error_file_path, True)


def import_metadata_files(corpus, files, input_format, error_file_path, source, save):
    if corpus and files:
        with open(error_file_path, "w") as error_file:
            for file_path in files:
                return import_metadata_file(corpus, file_path, input_format, error_file, source, save)


def import_metadata_file(corpus, file_path, input_format, error_file, source, save):
    print "import_metadata_file"
    if corpus and file_path:
        document_list = crosswalks_service.convert_file(file_path, input_format, "metajson", source, False)
        return import_metajson_list(corpus, document_list, error_file, save)


def import_metajson_list(corpus, metajson_list, error_file, save):
    print "import_metajson_list"
    if metajson_list:
            all_errors = []
            for metajson in metajson_list:
                rec_id = metajson["rec_id"]
                rec_source = metajson["rec_source"]

                metajson_service.enhance_metajson(metajson)

                errors = metajson_validation.validate_metajson_document(metajson)
                for error in errors:
                    formatted_error = rec_source + ":" + rec_id + ": " + error + "\n"
                    all_errors.append(formatted_error)
                    if error_file:
                        error_file.write(formatted_error)

                repository_service.save_document(corpus, metajson)

            return metajson_list, all_errors


def load_metajson_files(files):
    if files:
        for file_path in files:
            yield load_metajson_file(file_path)


def load_metajson_file(file_path):
    with open(file_path) as metajson_file:
        metajson = json.load(metajson_file)
        if "records" in metajson:
            for record in metajson["records"]:
                if record:
                    yield metajson_service.load_dict(record)
