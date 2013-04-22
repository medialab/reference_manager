#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from metadatas import metajson_validation
from crosswalks import endnote_to_metajson
from repository import mongodb_repository


def import_endnote_files(files, error_file_name):
    with open(error_file_name, "w") as error_file:

        for current_file in files:
            document_list = endnote_to_metajson.convert_endnote_file_to_metajson_document_list(current_file)
            for document in document_list:
                rec_id = document["rec_id"]
                rec_source = document["rec_source"]

                errors = metajson_validation.validate_metajson_document(document)
                for error in errors:
                    error_file.write(rec_source+":"+rec_id+": "+error+"\n")

                mongodb_repository.save_metajson(document)
