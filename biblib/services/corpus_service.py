#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import logging
import os
import uuid
import copy

from biblib.services import config_service
from biblib.services import crosswalks_service
from biblib.services import io_service
from biblib.services import repository_service
from biblib.validation import metajson_validation
from biblib.util import chrono
from biblib.util import constants
from biblib.util import jsonbson


#########
# Clean #
#########

def clean_corpus(corpus):
    if not corpus:
        logging.error("Error: empty corpus")
    else:
        logging.info("clean corpus: {}".format(corpus))

        date_begin = datetime.datetime.now()

        repository_service.create_corpus(corpus)
        repository_service.empty_corpus(corpus)
        repository_service.init_corpus_indexes(corpus)

        date_end = datetime.datetime.now()
        chrono.chrono_trace("clean_corpus", date_begin, date_end, None)


########
# Conf #
########

def conf_corpus(corpus, corpus_conf_dir_name):
    if not corpus:
        logging.error("Error: empty corpus")
    else:
        logging.info("init corpus: {}".format(corpus))

        if not corpus_conf_dir_name:
            corpus_conf_dir_name = corpus

        date_begin = datetime.datetime.now()

        # types
        results_types_common = conf_types(corpus, "common")
        results_types_corpus = conf_types(corpus, corpus_conf_dir_name)
        date_types = datetime.datetime.now()
        total_count = 0
        logging.debug("# Import common types:")
        if results_types_common:
            for entry in results_types_common:
                total_count += 1
                logging.info("type_id: {}, _id: {}".format(entry["type_id"], entry["_id"]))
        else:
            logging.debug("Empty common types")
        logging.info("# Import {} types:".format(corpus))
        if results_types_corpus:
            for entry in results_types_corpus:
                total_count += 1
                logging.info("type_id: {}, _id: {}".format(entry["type_id"], entry["_id"]))
        else:
            logging.info("Empty {} types".format(corpus))
        chrono.chrono_trace("conf_types", date_begin, date_types, total_count)

        # datafields
        results_fields_common = conf_fields(corpus, "common")
        results_fields_corpus = conf_fields(corpus, corpus)
        date_fields = datetime.datetime.now()
        total_count = 0
        logging.info("# Import common fields:")
        if results_fields_common:
            for entry in results_fields_common:
                total_count += 1
                logging.info("rec_type: {}, _id: {}".format(entry["rec_type"], entry["_id"]))
        else:
            logging.info("Empty common fields")
        logging.info("# Import {} fields:".format(corpus))
        if results_fields_corpus:
            for entry in results_fields_corpus:
                total_count += 1
                logging.info("rec_type: {}, _id: {}".format(entry["rec_type"], entry["_id"]))
        else:
            logging.info("Empty {} fields".format(corpus))
        chrono.chrono_trace("conf_fields", date_types, date_fields, total_count)


##########
# Export #
##########

def export_corpus(corpus, output_file_path, output_format, all_in_one_file, numer_export=False):
    if corpus and output_file_path:
        # fetch
        metajson_list = repository_service.get_documents(corpus)
        
        # one record per physical resource
        if numer_export:
            final_list = []
            for document in metajson_list:
                if document is not None and "resources" in document and document["resources"] is not None:
                    res_phys_count = 0
                    res_phys_numer_count = 0
                    for resource in document["resources"]:
                        # only for physical resources
                        if "rec_type" in resource and resource["rec_type"] == "physical":
                            res_phys_count += 1
                            if "note" in resource and resource["note"][:5].lower() == "numer":
                                res_phys_numer_count += 1
                    if res_phys_count > 0:
                        for resource in document["resources"]:
                            if "rec_type" in resource and resource["rec_type"] == "physical":
                                new_doc = copy.deepcopy(document)
                                if "physical_copy_number" in resource and resource["physical_copy_number"] is not None:
                                    new_doc["rec_id"] = new_doc["rec_id"] + "_" + resource["physical_copy_number"]
                                if res_phys_numer_count == 0:
                                    # Add all physical resources
                                    new_doc["resources"] = [resource]
                                    final_list.append(new_doc)
                                else:
                                    # Only numer physical resources
                                    if "note" in resource and resource["note"][:5].lower() == "numer":
                                        new_doc["resources"] = [resource]
                                        final_list.append(new_doc)
            metajson_list = final_list

        # convert
        results = crosswalks_service.convert_metajson_list(metajson_list, output_format, all_in_one_file)

        # export
        io_service.write_items(corpus, corpus, results, output_file_path, output_format, all_in_one_file)


##########
# Format #
##########

def format_corpus(corpus, output_title, output_file_path, output_style):
    if corpus and output_file_path:
        # fetch
        metajson_list = repository_service.get_documents(corpus)
        # format
        io_service.write_html(corpus, output_title, metajson_list, output_file_path, output_style)


##########
# Import #
##########

def import_metadata_files(corpus, input_file_paths, input_format, source, rec_id_prefix, save, role):
    if corpus and input_file_paths:
        results = []
        for input_file_path in input_file_paths:
            results.extend(import_metadata_file(corpus, input_file_path, input_format, source, rec_id_prefix, save, role))
        return results


def import_metadata_file(corpus, input_file_path, input_format, source, rec_id_prefix, save, role):
    logging.info("import_metadata_file")
    if corpus and input_file_path:
        logging.info("corpus: {}".format(corpus))
        logging.info("input_file_path: {}".format(input_file_path))
        logging.info("input_format: {}".format(input_format))
        logging.info("source: {}".format(source))
        document_list = crosswalks_service.parse_and_convert_file(input_file_path, input_format, constants.FORMAT_METAJSON, source, rec_id_prefix, False, False)
        return import_metajson_list(corpus, document_list, save, role)


def import_metajson_list(corpus, document_list, save, role):
    logging.info("import_metajson_list")
    results = []
    if document_list is not None:
        for document in document_list:
            if document:
                if "rec_id" not in document:
                    document["rec_id"] = str(uuid.uuid1())
                results.append(repository_service.save_document(corpus, document, role))

    return results


############
# Validate #
############

def validate_corpus(corpus, error_file_path):
    if corpus and error_file_path:
        with open(error_file_path, "w") as error_file:
            # fetch
            document_list = repository_service.get_documents(corpus)

            # validate
            all_errors = []
            for document in document_list:

                rec_id = document["rec_id"]
                rec_source = "empy"
                if "rec_source" in document:
                    rec_source = document["rec_source"]

                errors = metajson_validation.validate_metajson_document(document)
                for error in errors:
                    formatted_error = "".join([corpus, ":", rec_source, ":", rec_id, ":", error, "\n"])
                    all_errors.append(formatted_error)
                    if error_file:
                        error_file.write(formatted_error)

            return all_errors

########
# Type #
########

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
                            logging.error("ERROR: Type file is not valid JSON : {} {} {}".format(folder, file_name, e))
            return results


#########
# Field #
#########

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
                            logging.error("ERROR: Field file is not valid JSON : {} {} {}".format(folder, file_name, e))
            return results
