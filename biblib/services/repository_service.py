#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# mongod --dbpath /Users/jrault/Documents/SciencesPo/Projets/biblib/mongodb

import uuid
import pymongo
from bson.objectid import ObjectId
from biblib.services import config_service
from biblib.services import metajson_service

config = config_service.config["mongodb"]
default_corpus = config["default_corpus"]

mongodb = pymongo.MongoClient(config['host'], config['port'])

COL_DOCUMENTS = "documents"
COL_AGENTS = "agents"
COL_TYPES = "types"
COL_DATAFIELDS = "datafields"
COL_UIFIELDS = "uifields"

# examples:
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': {'$in': update_ids}}, {'$set': {'crawling_status': crawling_statuses.RUNNING}}, multi=True, safe=True)
# update_ids = [job['_id'] for job in mongodb[config['mongo-scrapy']['jobListCol']].find({'_id': {'$in': finished_ids}, 'crawling_status': {'$nin': [crawling_statuses.CANCELED, crawling_statuses.FINISHED]}}, fields=['_id'])]
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': res['jobid']}, {'$set': {'webentity_id': webentity_id, 'nb_pages': 0, 'nb_links': 0, 'crawl_arguments': args, 'crawling_status': crawling_statuses.PENDING, 'indexing_status': indexing_statuses.PENDING, 'timestamp': ts}}, upsert=True, safe=True)
# return db[config['mongo-scrapy']['jobLogsCol']].insert([{'_job': _id, 'timestamp': timestamp, 'log': msg} for _id in jobid])


def create_corpus(corpus):
    mongodb[corpus]


def empty_corpus(corpus):
    mongodb[corpus][COL_DOCUMENTS].drop()
    mongodb[corpus][COL_AGENTS].drop()
    mongodb[corpus][COL_TYPES].drop()
    mongodb[corpus][COL_DATAFIELDS].drop()
    mongodb[corpus][COL_UIFIELDS].drop()


def init_corpus_indexes(corpus):
    mongodb[corpus][COL_DOCUMENTS].ensure_index([('_id', pymongo.ASCENDING)], safe=True)
    mongodb[corpus][COL_AGENTS].ensure_index([('_id', pymongo.ASCENDING)], safe=True)
    mongodb[corpus][COL_TYPES].ensure_index([('_id', pymongo.ASCENDING)], safe=True)
    mongodb[corpus][COL_DATAFIELDS].ensure_index([('_id', pymongo.ASCENDING)], safe=True)
    mongodb[corpus][COL_UIFIELDS].ensure_index([('_id', pymongo.ASCENDING)], safe=True)


def get_document_by_mongo_id(corpus, mongo_id):
    if not corpus:
        corpus = default_corpus
    return metajson_service.load_dict(mongodb[corpus][COL_DOCUMENTS].find_one({'_id': ObjectId(mongo_id)}))


def get_documents_by_mongo_ids(corpus, mongo_ids):
    if not corpus:
        corpus = default_corpus
    mongo_object_ids = []
    for mongo_id in mongo_ids:
        mongo_object_ids.append(ObjectId(mongo_id))
    return metajson_service.load_dict_list(mongodb[corpus][COL_DOCUMENTS].find({"_id": {"$in": mongo_object_ids}}))


def get_document_by_rec_id(corpus, rec_id):
    if not corpus:
        corpus = default_corpus
    return metajson_service.load_dict(mongodb[corpus][COL_DOCUMENTS].find_one({"rec_id": rec_id}))


def get_documents_by_rec_ids(corpus, rec_ids):
    if not corpus:
        corpus = default_corpus
    return metajson_service.load_dict_list(mongodb[corpus][COL_DOCUMENTS].find({"rec_id": {"$in": rec_ids}}))


def get_documents(corpus):
    if not corpus:
        corpus = default_corpus
    return metajson_service.load_dict_list(mongodb[corpus][COL_DOCUMENTS].find())


def get_documents_count(corpus):
    if not corpus:
        corpus = default_corpus
    return mongodb[corpus][COL_DOCUMENTS].count()


def search_documents(corpus, query):
    if not corpus:
        corpus = default_corpus
    # {"rec_id": {"$in": rec_ids}}
    return metajson_service.load_dict_list(mongodb[corpus][COL_DOCUMENTS].find(query))


def save_document(corpus, document):
    if not corpus:
        corpus = default_corpus
    if "rec_id" not in document:
        document["rec_id"] = str(uuid.uuid1())
    return mongodb[corpus][COL_DOCUMENTS].insert(document)


def get_datafield(corpus, prop):
    if not corpus:
        corpus = default_corpus
    return metajson_service.load_dict(mongodb[corpus][COL_DATAFIELDS].find_one({"property": prop}))


def save_datafield(corpus, datafield):
    if not corpus:
        corpus = default_corpus
    return mongodb[corpus][COL_DATAFIELDS].insert(datafield)


def get_uifield(corpus, rec_type):
    if not corpus:
        corpus = default_corpus
    return metajson_service.load_dict(mongodb[corpus][COL_UIFIELDS].find_one({"rec_type": rec_type}))


def save_uifield(corpus, uifield):
    if not corpus:
        corpus = default_corpus
    return mongodb[corpus][COL_UIFIELDS].insert(uifield)


def get_type(corpus, type_id):
    if not corpus:
        corpus = default_corpus
    return metajson_service.load_dict(mongodb[corpus][COL_TYPES].find_one({"type_id": type_id}))


def save_type(corpus, metatype):
    if not corpus:
        corpus = default_corpus
    return mongodb[corpus][COL_TYPES].insert(metatype)
