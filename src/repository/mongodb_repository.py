#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# mongod --dbpath /Users/jrault/Documents/SciencesPo/Projets/ReferenceManager/mongodb

import os
import uuid
import pymongo
import json
from bson.objectid import ObjectId
from metadatas.metajson import Document
from util import config_loader

config = config_loader.config["mongodb"]

mongodb = pymongo.Connection(config['host'], config['port'])[config['db']]

# examples:
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': {'$in': update_ids}}, {'$set': {'crawling_status': crawling_statuses.RUNNING}}, multi=True, safe=True)
# update_ids = [job['_id'] for job in mongodb[config['mongo-scrapy']['jobListCol']].find({'_id': {'$in': finished_ids}, 'crawling_status': {'$nin': [crawling_statuses.CANCELED, crawling_statuses.FINISHED]}}, fields=['_id'])]
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': res['jobid']}, {'$set': {'webentity_id': webentity_id, 'nb_pages': 0, 'nb_links': 0, 'crawl_arguments': args, 'crawling_status': crawling_statuses.PENDING, 'indexing_status': indexing_statuses.PENDING, 'timestamp': ts}}, upsert=True, safe=True)
# return db[config['mongo-scrapy']['jobLogsCol']].insert([{'_job': _id, 'timestamp': timestamp, 'log': msg} for _id in jobid])


def empty_db():
    mongodb[config['referencesCol']].drop()
    mongodb[config['typesCol']].drop()
    mongodb[config['datafieldsCol']].drop()
    init_indexes()
    #init_types()


def init_indexes():
    mongodb[config['referencesCol']].ensure_index([('_id', pymongo.ASCENDING)], safe=True)
    mongodb[config['typesCol']].ensure_index([('_id', pymongo.ASCENDING)], safe=True)
    mongodb[config['datafieldsCol']].ensure_index([('_id', pymongo.ASCENDING)], safe=True)


def init_types():
    print("mongodb_repository.init_types")
    types_dir = os.path.abspath(os.path.join(os.getcwd(), "types"))
    print(types_dir)
    for file_name in os.listdir(types_dir):
        if file_name.endswith(".json"):
            with open(file_name, 'r') as type_file:
                json_type = json.load(type_file)
                save_type(json_type)


def save_type(metatype):
    return mongodb[config['typesCol']].insert(metatype)


def convert_to_metajson(mongoitems):
    metajson_list = []
    for mongoitem in mongoitems:
        metajson_list.append(Document(mongoitem))
    return metajson_list


def save_metajson(metajson):
    if "rec_id" not in metajson:
        rec_id = str(uuid.uuid1())
        print rec_id
        metajson["rec_id"] = rec_id
    return mongodb[config['referencesCol']].insert(metajson)


def get_by_mongo_id(mongo_id):
    print mongo_id
    return Document(mongodb[config['referencesCol']].find_one({'_id': ObjectId(mongo_id)}))


def get_by_mongo_ids(mongo_ids):
    print mongo_ids
    mongo_object_ids = []
    for mongo_id in mongo_ids:
        mongo_object_ids.append(ObjectId(mongo_id))
    #return convert_to_metajson(mongodb[config['referencesCol']].for_ids(mongo_ids))
    return convert_to_metajson(mongodb[config['referencesCol']].find({"_id": {"$in": mongo_object_ids}}))


def get_by_rec_id(rec_id):
    print rec_id
    return Document(mongodb[config['referencesCol']].find_one({"rec_id": rec_id}))


def get_by_rec_ids(rec_ids):
    print rec_ids
    return convert_to_metajson(mongodb[config['referencesCol']].find({"rec_id": {"$in": rec_ids}}))


def get_all():
    return convert_to_metajson(mongodb[config['referencesCol']].find())


def get_count():
    return mongodb[config['referencesCol']].count()
