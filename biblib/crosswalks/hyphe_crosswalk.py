#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Document
from biblib.services import date_service


def hyphe_webentity_result_to_metajson(hyphe_result, source, only_first_record=False):
    if "code" in hyphe_result and hyphe_result["code"] == "success" and "result" in hyphe_result:
        return hyphe_webentity_to_metajson(hyphe_result["result"], source)


def hyphe_webentities_result_to_metajson_list(hyphe_result, source, only_first_record=False):
    if "code" in hyphe_result and hyphe_result["code"] == "success" and "result" in hyphe_result:
        return hyphe_webentities_to_metajson_list(hyphe_result["result"], source, only_first_record)


def hyphe_webentities_to_metajson_list(webentities, source, only_first_record=False, status_list=None):
    if status_list:
        if len(status_list) == 1:
            status = status_list[0]
            for webentity in (y for y in webentities if webentity["status"] == status):
                yield hyphe_webentity_to_metajson(webentity, source)
        elif len(status_list) > 1:
            for webentity in (y for y in webentities if webentity["status"] in status_list):
                yield hyphe_webentity_to_metajson(webentity, source)
    else:
        for webentity in webentities:
            yield hyphe_webentity_to_metajson(webentity, source)


def hyphe_webentity_to_metajson(webentity, source):
    document = Document()

    document["rec_type"] = "WebEntity"
    if source:
        document["source"] = source

    if webentity["lru_prefixes"]:
        document["rec_id"] = webentity["lru_prefixes"][0]
    #document["rec_created_date"] = date_service.parse_timestamp(webentity["creation_date"])
    #document["rec_modified_date"] = date_service.parse_timestamp(webentity["last_modification_date"])
    
    document["title"] = webentity["name"]

    hyphe = {}
    hyphe["webentity_id"] = webentity["id"]
    hyphe["crawling_status"] = webentity["crawling_status"]
    if webentity["homepage"]:
        hyphe["homepage"] = webentity["homepage"]
    hyphe["indexing_status"] = webentity["indexing_status"]
    hyphe["lru_prefixes"] = webentity["lru_prefixes"]
    if webentity["startpages"]:
        hyphe["startpages"] = webentity["startpages"]
    hyphe["status"] = webentity["status"]
    
    # todo : tags to metajson specific
    if webentity["tags"]:
        hyphe["tags"] = webentity["tags"]

    document["hyphe"] = hyphe

    return document
