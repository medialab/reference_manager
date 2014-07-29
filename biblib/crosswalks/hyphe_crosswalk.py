#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Document
from biblib.services import date_service


def hyphe_webentities_to_metajson_list(webentities, source, only_first_record=False, status_list=None):
    for webentity in webentities:
        yield hyphe_webentity_to_metajson(webentity, source)


def hyphe_webentity_to_metajson(webentity, source):
    document = Document()

    # static
    document["rec_type"] = "WebEntity"
    if source:
        document["source"] = source

    # MetaJSON
    # id -> rec_id
    document["rec_id"] = webentity["id"]
    # creation_date -> rec_created_date
    #document["rec_created_date"] = date_service.parse_timestamp(webentity["creation_date"])
    # last_modification_date -> rec_modified_date
    #document["rec_modified_date"] = date_service.parse_timestamp(webentity["last_modification_date"])
    document["title"] = webentity["name"]

    # Hyphe specific
    hyphe = {}
    # id -> hyphe/webentity_id
    hyphe["webentity_id"] = webentity["id"]
    # crawling_status -> hyphe/crawling_status
    hyphe["crawling_status"] = webentity["crawling_status"]
    # indexing_status -> hyphe/indexing_status
    hyphe["indexing_status"] = webentity["indexing_status"]
    # status -> hyphe/status
    hyphe["status"] = webentity["status"]
    # lru_prefixes -> hyphe/lru_prefixes
    hyphe["lru_prefixes"] = webentity["lru_prefixes"]
    # startpages -> hyphe/startpages
    hyphe["startpages"] = webentity["startpages"]
    
    
    # todo : tags to metajson specific
    #if webentity["tags"]:
    #    hyphe["tags"] = webentity["tags"]

    document["hyphe"] = hyphe

    return document
