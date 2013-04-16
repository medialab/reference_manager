#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# mongod --dbpath /Users/jrault/Documents/SciencesPo/Projets/ReferenceManager/mongodb

import uuid
import pymongo
import bson
from bson.objectid import ObjectId
from metadatas.metajson import Common, Document, Contributor, Identifier, Resource

config={
    "host": "localhost",
    "port": 27017,
    "db": "refmanager",
    "refCol": "references"
}

mongo_db=pymongo.Connection(config['host'],config['port'])[config['db']]

def init_indexes():
    mongo_db[config['refCol']].ensure_index([('_id', pymongo.ASCENDING)], safe=True)

def empty_db():
    mongo_db[config['refCol']].drop()
    init_indexes()

# resdb = mongo_db[config['mongo-scrapy']['jobListCol']].update({'_id': {'$in': update_ids}}, {'$set': {'crawling_status': crawling_statuses.RUNNING}}, multi=True, safe=True)
# update_ids = [job['_id'] for job in mongo_db[config['mongo-scrapy']['jobListCol']].find({'_id': {'$in': finished_ids}, 'crawling_status': {'$nin': [crawling_statuses.CANCELED, crawling_statuses.FINISHED]}}, fields=['_id'])]
# resdb = mongo_db[config['mongo-scrapy']['jobListCol']].update({'_id': res['jobid']}, {'$set': {'webentity_id': webentity_id, 'nb_pages': 0, 'nb_links': 0, 'crawl_arguments': args, 'crawling_status': crawling_statuses.PENDING, 'indexing_status': indexing_statuses.PENDING, 'timestamp': ts}}, upsert=True, safe=True)
# return db[config['mongo-scrapy']['jobLogsCol']].insert([{'_job': _id, 'timestamp': timestamp, 'log': msg} for _id in jobid])

def convert_to_metajson(mongoitems):
    metajson_list=[]
    for mongoitem in mongoitems :
        metajson_list.append(Document(mongoitem))
    return metajson_list

def save_metajson(metajson):
    if "rec_id" not in metajson:
        rec_id = str(uuid.uuid1())
        print rec_id
        metajson["rec_id"] = rec_id
    return mongo_db[config['refCol']].insert(metajson)

def get_by_mongo_id(mongo_id):
    print mongo_id
    return Document(mongo_db[config['refCol']].find_one({'_id': ObjectId(mongo_id)}))

def get_by_mongo_ids(mongo_ids):
    print mongo_ids
    mongo_object_ids = []
    for mongo_id in mongo_ids :
        mongo_object_ids.append(ObjectId(mongo_id))
    #return convert_to_metajson(mongo_db[config['refCol']].for_ids(mongo_ids))
    return convert_to_metajson(mongo_db[config['refCol']].find({"_id": {"$in": mongo_object_ids}}))

def get_by_rec_id(rec_id):
    print rec_id
    return Document(mongo_db[config['refCol']].find_one({"rec_id": rec_id}))

def get_by_rec_ids(rec_ids):
    print rec_ids
    return convert_to_metajson(mongo_db[config['refCol']].find({"rec_id": {"$in": rec_ids}}))

def get_all():
    return convert_to_metajson(mongo_db[config['refCol']].find())

def get_count():
    return mongo_db[config['refCol']].count()

