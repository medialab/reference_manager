#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from referencemanager.services import crosswalks_service
from referencemanager.services import metajson_service
from referencemanager.validation import metajson_validation
from referencemanager.services import repository_service


def import_endnote_files(files, error_file_path):
    import_metadata_files(files, "endnotexml", error_file_path, True)


def import_metadata_files(files, input_format, error_file_path, save):
    if files:
        with open(error_file_path, "w") as error_file:
            for file_path in files:
                return import_metadata_file(file_path, input_format, error_file, save)


def import_metadata_file(file_path, input_format, error_file, save):
    if file_path:
        document_list = crosswalks_service.convert_file(file_path, input_format, "metajson")
        return import_metajson_list(document_list, error_file, save)


def import_metajson_list(metajson_list, error_file, save):
    if metajson_list:
            all_errors = []
            for metajson in metajson_list:
                rec_id = metajson["rec_id"]
                rec_source = metajson["rec_source"]

                errors = metajson_validation.validate_metajson_document(metajson)
                for error in errors:
                    formatted_error = rec_source + ":" + rec_id + ": " + error + "\n"
                    all_errors.append(formatted_error)
                    if error_file:
                        error_file.write(formatted_error)

                repository_service.save_reference(metajson)

            return metajson_list, all_errors


def load_metajson_files(files):
    if files:
        document_list = []
        for file_path in files:
            document_list.extend(load_metajson_file(file_path))
        return document_list


def load_metajson_file(file_path):
    document_list = []
    with open(file_path) as metajson_file:
        metajson = json.load(metajson_file)
        if "records" in metajson:
            for record in metajson["records"]:
                if record:
                    document_list.append(metajson_service.load_dict(record))
    return document_list
