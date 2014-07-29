#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import csv
import datetime
import logging
import os

from stdnum import issn

from biblib.cloud import openurl_client
from biblib.crosswalks import openurl_crosswalk
from biblib.services import corpus_service
from biblib.services import repository_service
from biblib.services import resource_service
from biblib.util import chrono
from biblib.util import console
from biblib.util import constants


console.setup_console()


def validate_perios(documents, csv_file_path):
    if documents:
        source = "Serials Solutions"
        rec_id_prefix = ""
        issn_duplicated = {}
        # restore of the previous state
        previously_dict = {}
        if os.path.isfile(csv_file_path):
            with open(csv_file_path, "rb") as csv_file:
                csvreader = csv.DictReader(csv_file, delimiter=',')
                for csvdict in csvreader:
                    previously_dict[csvdict["rec_id"]] = csvdict["rec_id"]
        with open(csv_file_path, "wb") as csv_file:
            fieldnames = ["rec_id", "rec_type", "title_non_sort", "title", "title_sub", "issn", "issn_status", "rel_eissn", "rel_response", 
                          "856_1_u", "856_1_status", "856_2_u", "856_2_status", "856_3_u", "856_3_status", "856_4_u", "856_4_status", "856_5_u", "856_5_status", 
                          "856_6_u", "856_6_status", "856_7_u", "856_7_status", "856_8_u", "856_8_status", "856_9_u", "856_9_status", "856_10_u", "856_10_status", 
                          "856_11_u", "856_11_status", "856_12_u", "856_12_status", "856_13_u", "856_13_status", "856_14_u", "856_14_status", "856_15_u", "856_15_status", 
                          "856_16_u", "856_16_status", "856_17_u", "856_17_status", "856_18_u", "856_18_status", "856_19_u", "856_19_status", "856_20_u", "856_20_status", 
                          "856_21_u", "856_21_status", "856_22_u", "856_22_status", "856_23_u", "856_23_status", "856_24_u", "856_24_status", "856_25_u", "856_25_status"]
            csvwriter = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)
            csvwriter.writeheader()
            for index, document in enumerate(documents):
                rec_id = document["rec_id"]
                if rec_id in previously_dict:
                    logging.info("# Document with index: {} and rec_id: {} - Previously verified".format(index, rec_id))
                else:
                    logging.info("# Document index: {} and rec_id: {} - Starting verification".format(index, rec_id))
                    csvdict = {}
                    csvdict["rec_id"] = document["rec_id"]
                    #logging.debug(csvdict["rec_id"])
                    csvdict["rec_type"] = document["rec_type"]
                    if "title_non_sort" in document:
                        csvdict["title_non_sort"] = document["title_non_sort"]
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
                    if "resources" in document:
                        for i, resource in enumerate(document["resources"]):
                            if "url" in resource:
                                csvdict["856_" + str(i+1) + "_u"] = resource["url"]
                                # test URL
                                res_dict  = resource_service.fetch_url(resource["url"])[0]
                                if res_dict["error"]:
                                    csvdict["856_" + str(i+1) + "_status"] = "ERROR"
                                else:
                                    csvdict["856_" + str(i+1) + "_status"] = "OK"
                            else:
                                csvdict["856_" + str(i+1) + "_u"] = "EMPTY"
                                csvdict["856_" + str(i+1) + "_status"] = "EMPTY"

                    # revues en ligne / openurl
                    if csvdict["issn_status"] == "OK":
                        openurl_response = openurl_client.request_periodical_by_issn(csvdict["issn"])
                        if openurl_response is not None:
                            openurl_documents = openurl_crosswalk.openurl_xmletree_to_metajson_list(openurl_response, source, rec_id_prefix, True)
                            if openurl_documents:
                                openurl_document = openurl_documents[0]
                                if "identifiers" in openurl_document:
                                    for identifier in openurl_document["identifiers"]:
                                        if identifier["id_type"] == "eissn":
                                            csvdict["rel_eissn"] = identifier["value"]
                                            break
                                if "resources" in openurl_document:
                                    rel_response = []
                                    for resource in openurl_document["resources"]:
                                        if rel_response:
                                            rel_response.append("\n")
                                        if "provider_name" in resource:
                                            rel_response.append(resource["provider_name"])
                                        if "database_name" in resource:
                                            rel_response.append(" - ")
                                            rel_response.append(resource["database_name"])
                                        if "period_begin" in resource or "period_end" in resource:
                                            rel_response.append(" (")
                                            if "period_begin" in resource:
                                                rel_response.append(resource["period_begin"])
                                            else:
                                                rel_response.append("....")
                                            if "period_end" in resource:
                                                rel_response.append(" - ")
                                                rel_response.append(resource["period_end"])
                                            else:
                                                rel_response.append(" - ....")
                                            rel_response.append(")")
                                    if rel_response:
                                        csvdict["rel_response"] = "".join(rel_response)
                    csvwriter.writerow(csvdict)


if __name__ == "__main__":
    date_begin = datetime.datetime.now()

    # conf params
    corpus = "perio"
    source = "Sciences Po | la bibliothèque"
    rec_id_prefix = ""
    input_file_path = os.path.join("data", "unimarc", "periouni.mrc")
    input_format = constants.FORMAT_UNIMARC
    csv_file_name = "".join(["validation-", corpus, ".csv"])
    csv_file_path = os.path.join("data", "result", csv_file_name)

    # conf corpus
    corpus_service.clean_corpus(corpus)
    corpus_service.conf_corpus(corpus, "aime")
    date_clean = datetime.datetime.now()
    chrono.chrono_trace("Clean and conf corpus", date_begin, date_clean, None)

    # import
    corpus_service.import_metadata_file(corpus, input_file_path, input_format, source, rec_id_prefix, True, None)
    date_import = datetime.datetime.now()
    chrono.chrono_trace("Import corpus", date_clean, date_import, None)

    # Validate perio
    documents = repository_service.get_documents(corpus)
    validate_perios(documents, csv_file_path)
    date_validate = datetime.datetime.now()
    chrono.chrono_trace("Validate perio", date_import, date_validate, None)
