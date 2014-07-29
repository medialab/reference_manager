#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import jsonrpclib
import os
import csv
import logging

from biblib.crosswalks import csv_crosswalk
from biblib.crosswalks import hyphe_crosswalk
from biblib.services import config_service
from biblib.services import repository_service
from biblib.util import console
from biblib.util import constants
from biblib.util import jsonbson

console.setup_console()

corpus = config_service.config["default_corpus"]
hyphe_jsonrpc_host = config_service.config["hyphe"]["jsonrpc_host"]
hyphe_jsonrpc_port = config_service.config["hyphe"]["jsonrpc_port"]

csv_path = os.path.join("data", "csv_sitpol", "csv_sitpol.csv")

hyphe_core = jsonrpclib.Server("{}:{}".format(hyphe_jsonrpc_host, hyphe_jsonrpc_port))

with open(csv_path, 'rb') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        # title url webentity_type  classifications_sitpol  classifications_ddc specific_agents specific_actor_type descriptions@lang=fr    keywords@lang=fr    keywords@lang=en    creators@role=pbl   languages   publication_countrie    rec_type_cerimes    target_audiences_cerimes    rec_created_use notes@lang=fr
        url = row["url"]
        we_id = hyphe_core.store.get_webentity_for_url(url)["result"]["id"]
        print we_id
        document = csv_crosswalk.csv_dict_reader_to_metasjon(row, constants.FORMAT_CSV_SITPOL, "csv", "")
        #logging.debug(jsonbson.dumps_json(document, True))
        # search we
        mongo_query = {"hyphe.webentity_id": we_id}
        search_results = repository_service.search_mongo(corpus, mongo_query)
        print search_results
        # merge
