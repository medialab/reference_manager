#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json

from bson import json_util

from biblib.services import repository_service
from biblib.util import console


def test_search():
    search_query = {"filter_class": "Document"}
    search_query["filter_date_end"] = "2000"
    search_query["filter_date_start"] = "2013"
    search_query["filter_languages"] = ["en", "fr"]
    search_query["filter_types"] = ["Book", "BookPart"]
    search_query["rec_class"] = "SearchQuery"
    search_query["rec_metajson"] = 1
    search_query["result_batch_size"] = 100
    search_query["result_bibliographic_styles"] = ["mla"]
    search_query["result_offset"] = 0
    search_query["result_sorts"] = [{"field": "rec_type", "order": "asc"}]
    search_query["search_terms"] = [{"index": "title", "operator": "or", "value": "Cheyenne"}]

    print "search_query:"
    print json.dumps(search_query, indent=4, ensure_ascii=False, encoding="utf-8", sort_keys=True)

    search_result = repository_service.search(None, search_query)

    print "search_result:"
    print json_util.dumps(search_result, ensure_ascii=False, indent=4, encoding="utf-8", sort_keys=True)


def test():
    test_search()

console.setup_console()
test()