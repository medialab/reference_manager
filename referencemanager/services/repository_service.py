#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# mongod --dbpath /Users/jrault/Documents/SciencesPo/Projets/ReferenceManager/mongodb

import uuid
import pymongo
from bson.objectid import ObjectId
from referencemanager.services import config_service
from referencemanager.services import metajson_service

config = config_service.config["mongodb"]

mongodb = pymongo.Connection(config['host'], config['port'])[config['db']]

# examples:
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': {'$in': update_ids}}, {'$set': {'crawling_status': crawling_statuses.RUNNING}}, multi=True, safe=True)
# update_ids = [job['_id'] for job in mongodb[config['mongo-scrapy']['jobListCol']].find({'_id': {'$in': finished_ids}, 'crawling_status': {'$nin': [crawling_statuses.CANCELED, crawling_statuses.FINISHED]}}, fields=['_id'])]
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': res['jobid']}, {'$set': {'webentity_id': webentity_id, 'nb_pages': 0, 'nb_links': 0, 'crawl_arguments': args, 'crawling_status': crawling_statuses.PENDING, 'indexing_status': indexing_statuses.PENDING, 'timestamp': ts}}, upsert=True, safe=True)
# return db[config['mongo-scrapy']['jobLogsCol']].insert([{'_job': _id, 'timestamp': timestamp, 'log': msg} for _id in jobid])


def empty_db():
    mongodb[config['datafieldsCol']].drop()
    mongodb[config['referencesCol']].drop()
    mongodb[config['typesCol']].drop()
    init_indexes()


def init_indexes():
    mongodb[config['datafieldsCol']].ensure_index([('_id', pymongo.ASCENDING)], safe=True)
    mongodb[config['referencesCol']].ensure_index([('_id', pymongo.ASCENDING)], safe=True)
    mongodb[config['typesCol']].ensure_index([('_id', pymongo.ASCENDING)], safe=True)


def get_datafield(rec_type):
    return metajson_service.load_dict(mongodb[config['datafieldsCol']].find_one({"rec_type": rec_type}))


def save_datafield(datafield):
    return mongodb[config['datafieldsCol']].insert(datafield)


def get_reference_by_mongo_id(mongo_id):
    return metajson_service.load_dict(mongodb[config['referencesCol']].find_one({'_id': ObjectId(mongo_id)}))


def get_references_by_mongo_ids(mongo_ids):
    mongo_object_ids = []
    for mongo_id in mongo_ids:
        mongo_object_ids.append(ObjectId(mongo_id))
    return metajson_service.load_dict_list(mongodb[config['referencesCol']].find({"_id": {"$in": mongo_object_ids}}))


def get_reference_by_rec_id(rec_id):
    return metajson_service.load_dict(mongodb[config['referencesCol']].find_one({"rec_id": rec_id}))


def get_references_by_rec_ids(rec_ids):
    return metajson_service.load_dict_list(mongodb[config['referencesCol']].find({"rec_id": {"$in": rec_ids}}))


def get_references():
    return metajson_service.load_dict_list(mongodb[config['referencesCol']].find())


def get_references_count():
    return mongodb[config['referencesCol']].count()


def search_references(query):
    # {"rec_id": {"$in": rec_ids}}
    return metajson_service.load_dict_list(mongodb[config['referencesCol']].find(query))


def save_reference(document):
    if "rec_id" not in document:
        document["rec_id"] = str(uuid.uuid1())
    return mongodb[config['referencesCol']].insert(document)


def get_type(type_id):
    return metajson_service.load_dict(mongodb[config['typesCol']].find_one({"type_id": type_id}))


def save_type(metatype):
    return mongodb[config['typesCol']].insert(metatype)
