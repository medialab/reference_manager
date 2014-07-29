#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import jsonrpclib
import logging

from biblib.crosswalks import hyphe_crosswalk
from biblib.services import config_service
from biblib.services import repository_service
from biblib.util import console
from biblib.util import jsonbson

console.setup_console()

corpus = config_service.config["default_corpus"]
hyphe_jsonrpc_host = config_service.config["hyphe"]["jsonrpc_host"]
hyphe_jsonrpc_port = config_service.config["hyphe"]["jsonrpc_port"]

hyphe_core = jsonrpclib.Server("{}:{}".format(hyphe_jsonrpc_host, hyphe_jsonrpc_port))

wes = hyphe_core.store.get_webentities_by_status("IN")["result"]
if wes:
    for we in wes:
        we_full = hyphe_core.store.get_webentity(we["id"])["result"][0]
        #logging.debug(jsonbson.dumps_json(we_full, True))
        document = hyphe_crosswalk.hyphe_webentity_to_metajson(we_full, "hyphe")
        #logging.debug(jsonbson.dumps_json(document, True))

        # search if already imported
        mongo_query = {"hyphe.webentity_id": we_full["id"]}
        search_results = repository_service.search_mongo(corpus, mongo_query)
        print search_results
        if search_results is None :
            repository_service.save_document(corpus, document, None)
