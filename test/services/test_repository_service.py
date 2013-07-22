#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.services import repository_service
from biblib.util import console
from biblib.util import jsonbson


def test_search_mongo():
    mongo_query = {"$or": [{"title": {"$options": "i", "$regex": "Cheyenne"}}, {"title": {"$options": "i", "$regex": "technique"}}]}
    mongo_query = {"$and": [{"$or": [{"title": {"$options": "i", "$regex": "Cheyenne"}}, {"title": {"$options": "i", "$regex": "technique"}}]}, {"publishers": {"$regex": "press", "$options": 'i'}}]}
    search_result = repository_service.search_mongo(None, mongo_query)
    print "search_result:"
    print jsonbson.dumps_bson(search_result, True)


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
    search_query["search_terms"] = [{"index": "title", "operator": "and", "value": "Cheyenne"}, {"index": "title", "operator": "or", "value": "technique"}]

    print "search_query:"
    print jsonbson.dumps_json(search_query, True)

    search_result = repository_service.search(None, search_query)

    print "search_result:"
    print jsonbson.dumps_bson(search_result, True)


def test():
    #test_search_mongo()
    test_search()

console.setup_console()
test()
