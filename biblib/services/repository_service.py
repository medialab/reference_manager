#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# mongod --dbpath /Users/jrault/Documents/SciencesPo/Projets/biblib/mongodb

import uuid
import pymongo
from bson.objectid import ObjectId
from bson.errors import InvalidId
from biblib.metajson import SearchResponse
from biblib.services import config_service
from biblib.services import metajson_service
from biblib.util import exceptions
from biblib.util import jsonbson

DOCUMENTS = "documents"
AGENTS = "agents"
TYPES = "types"
UIFIELDS = "uifields"

config = config_service.config["mongodb"]
default_corpus = config["default_corpus"]

try:
    mongodb = pymongo.MongoClient(config['host'], config['port'])
except pymongo.errors.ConnectionFailure as e:
    print "ERROR: connexion failure to MongoDB : {}".format(e)

# examples:
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': {'$in': update_ids}}, {'$set': {'crawling_status': crawling_statuses.RUNNING}}, multi=True, safe=True)
# update_ids = [job['_id'] for job in mongodb[config['mongo-scrapy']['jobListCol']].find({'_id': {'$in': finished_ids}, 'crawling_status': {'$nin': [crawling_statuses.CANCELED, crawling_statuses.FINISHED]}}, fields=['_id'])]
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': res['jobid']}, {'$set': {'webentity_id': webentity_id, 'nb_pages': 0, 'nb_links': 0, 'crawl_arguments': args, 'crawling_status': crawling_statuses.PENDING, 'indexing_status': indexing_statuses.PENDING, 'timestamp': ts}}, upsert=True, safe=True)
# return db[config['mongo-scrapy']['jobLogsCol']].insert([{'_job': _id, 'timestamp': timestamp, 'log': msg} for _id in jobid])


def create_corpus(corpus):
    mongodb[corpus]


def empty_corpus(corpus):
    mongodb[corpus][DOCUMENTS].drop()
    mongodb[corpus][AGENTS].drop()
    mongodb[corpus][TYPES].drop()
    mongodb[corpus][UIFIELDS].drop()


def init_corpus_indexes(corpus):
    index_id = ('_id', pymongo.ASCENDING)
    index_rec_id = ('rec_id', pymongo.ASCENDING)
    index_title = ('title', pymongo.ASCENDING)
    index_name = ('name', pymongo.ASCENDING)
    index_name_family = ('name_family', pymongo.ASCENDING)
    index_name_family = ('name_given', pymongo.ASCENDING)

    mongodb[corpus][DOCUMENTS].ensure_index([index_id, index_rec_id, index_title], safe=True)

    mongodb[corpus][DOCUMENTS].ensure_index([index_id, index_rec_id, index_title], safe=True)
    mongodb[corpus][AGENTS].ensure_index([index_id, index_rec_id, index_name, index_name_family], safe=True)
    mongodb[corpus][TYPES].ensure_index([index_id], safe=True)
    mongodb[corpus][UIFIELDS].ensure_index([index_id], safe=True)


def get_document_by_mongo_id(corpus, mongo_id):
    if not corpus:
        corpus = default_corpus
    result = mongodb[corpus][DOCUMENTS].find_one({'_id': ObjectId(mongo_id)})
    if result:
        return metajson_service.load_dict(result)
    else:
        return None


def get_documents_by_mongo_ids(corpus, mongo_ids):
    if not corpus:
        corpus = default_corpus
    mongo_object_ids = []
    for mongo_id in mongo_ids:
        mongo_object_ids.append(ObjectId(mongo_id))
    results = mongodb[corpus][DOCUMENTS].find({"_id": {"$in": mongo_object_ids}})
    if results:
        return metajson_service.load_dict_list(results)
    else:
        return None


def get_document_by_rec_id(corpus, rec_id):
    if not corpus:
        corpus = default_corpus
    result = mongodb[corpus][DOCUMENTS].find_one({"rec_id": rec_id})
    if result:
        return metajson_service.load_dict(result)
    else:
        return None


def get_documents_by_rec_ids(corpus, rec_ids):
    if not corpus:
        corpus = default_corpus
    results = mongodb[corpus][DOCUMENTS].find({"rec_id": {"$in": rec_ids}})
    if results:
        return metajson_service.load_dict_list(results)
    else:
        return None


def get_documents(corpus):
    if not corpus:
        corpus = default_corpus
    results = mongodb[corpus][DOCUMENTS].find()
    if results:
        return metajson_service.load_dict_list(results)
    else:
        return None


def get_documents_count(corpus):
    if not corpus:
        corpus = default_corpus
    return mongodb[corpus][DOCUMENTS].count()


def search(corpus, search_query):
    if not corpus:
        corpus = default_corpus
    search_response = SearchResponse()

    # empty search_query
    if search_query is None:
        raise exceptions.search_error("0")

    # filter_class -> collection
    collection = None
    if "filter_class" not in search_query or search_query["filter_class"] not in ["Document", "Agent", "Person", "OrgUnit", "Event", "Family"]:
        raise exceptions.search_error("100")
    elif search_query["filter_class"] == "Document":
        collection = DOCUMENTS
    elif search_query["filter_class"] in ["Agent", "Person", "OrgUnit", "Event", "Family"]:
        collection = AGENTS

    # other filters
    filter_query = []
    if "filter_date_end" in search_query:
        pass
        #filter_query.append({"date_sort": {"$lte": search_query["filter_date_end"]}})
    if "filter_date_start" in search_query:
        pass
        #filter_query.append({"date_sort": {"$gte": search_query["filter_date_start"]}})
    if "filter_languages" in search_query:
        filter_query.append({"languages": {"$in": search_query["filter_languages"]}})
    if "filter_types" in search_query:
        filter_query.append({"rec_type": {"$in": search_query["filter_types"]}})

    # search_terms
    # a
    # and b
    # or c
    # -> or(and(a,b),c)
    # a
    # or b
    # and c
    # -> and(or(a,b),c)

    search_indexes = []
    if "search_terms" in search_query:
        for idx, search_term in enumerate(search_query["search_terms"]):
            # value
            if "value" not in search_term or search_term["value"] is None:
                # useless
                break
            # index
            if "index" not in search_term:
                raise exceptions.search_error("100")
            elif search_term["index"] == "all":
                # todo
                search_indexes.append({"title": {"$regex": search_term["value"], "$options": 'i'}})

            elif search_term["index"] == "identifier":
                try:
                    obid = ObjectId(search_term["index"])
                    search_indexes.append({"_id": obid})
                except (InvalidId, TypeError):
                    search_indexes.append({"or": [{"rec_id": search_term["value"]}, {"identifiers.value": search_term["value"]}]})
            elif search_term["index"] == "title":
                search_indexes.append({"title": {"$regex": search_term["value"], "$options": 'i'}})
            elif search_term["index"] == "is_part_of":
                search_indexes.append({"is_part_ofs.title": {"$regex": search_term["value"], "$options": 'i'}})
            elif search_term["index"] == "creator":
                creator_terms = []
                for value in search_term["value"].replace(",", "").split():
                    creator_terms.append({"creators.agent.name_family": {"$regex": value, "$options": 'i'}})
                    creator_terms.append({"creators.agent.name_given": {"$regex": value, "$options": 'i'}})
                    creator_terms.append({"creators.agent.name": {"$regex": value, "$options": 'i'}})
                    creator_terms.append({"creators.agent.title": {"$regex": value, "$options": 'i'}})
                search_indexes.append({"$or": creator_terms})
            elif search_term["index"] == "creator_id":
                search_indexes.append({"creators.agent.rec_id": search_term["value"]})
            elif search_term["index"] == "affiliation":
                search_indexes.append({"creators.agent.affiliation.name": {"$regex": search_term["value"], "$options": 'i'}})
            elif search_term["index"] == "affiliation_id":
                search_indexes.append({"creators.agent.affiliation.rec_id": search_term["value"]})
            elif search_term["index"] == "publisher":
                search_indexes.append({"publishers": {"$regex": search_term["value"], "$options": 'i'}})
            elif search_term["index"] == "keyword":
                search_indexes.append({"keywords.value": {"$regex": search_term["value"], "$options": 'i'}})
            elif search_term["index"] == "classification":
                search_indexes.append({"classifications.value": {"$regex": search_term["value"], "$options": 'i'}})
            elif search_term["index"] == "research_area":
                search_indexes.append({"research_areas.value": {"$regex": search_term["value"], "$options": 'i'}})
            elif search_term["index"] == "subject":
                search_indexes.append({"subjects.value": {"$regex": search_term["value"], "$options": 'i'}})
            elif search_term["index"] == "set":
                search_indexes.append({"sets.value": {"$regex": search_term["value"], "$options": 'i'}})
            # operator
            if "operator" in search_term:
                if search_term["operator"] == "or":
                    pass
                elif search_term["operator"] == "and":
                    pass
                elif search_term["operator"] == "not":
                    pass

    # result_sorts : how to with this index ? ...

    if filter_query or search_indexes:
        mongo_query = {"$and": search_indexes}
    else:
        mongo_query = {}
    print "mongo_query:"
    print jsonbson.dumps_bson(mongo_query, True)

    records = metajson_service.load_dict_list(mongodb[corpus][collection].find(mongo_query))
    records_total_count = len(records)

    search_response["records"] = records
    search_response["records_total_count"] = records_total_count
    search_response["result_batch_size"] = records_total_count
    search_response["result_offset"] = 0
    search_response["search_query"] = search_query
    return search_response


def search_mongo(corpus, mongo_query):
    if not corpus:
        corpus = default_corpus
    # {"_id": {"$in": mongo_object_ids}}
    # {"rec_id": {"$in": rec_ids}}
    # {"rec_type": "Book"}
    # {"is_part_ofs.rec_type":"Book"}
    # {"is_part_ofs.rec_type":"Journal"}
    # {"is_part_ofs.rec_type":"VideoRecording"}
    # {"is_part_ofs.is_part_ofs.rec_type":"Book"}
    # {"creators.agent.name_family":"Latour"}
    # {"is_part_ofs.creators.agent.name_family":"Latour"}
    # {"is_part_ofs.creators.agent.name_family":"Latour", "is_part_of.creators.agent.name_given":"Bruno"}
    results = mongodb[corpus][DOCUMENTS].find(mongo_query)
    if results:
        return metajson_service.load_dict_list(results)
    else:
        return None


def save_document(corpus, document):
    if not corpus:
        corpus = default_corpus
    if "rec_id" not in document or document["rec_id"] is not None:
        document["rec_id"] = str(uuid.uuid1())
    rec_id = document["rec_id"]
    return mongodb[corpus][DOCUMENTS].save(document), rec_id


def delete_document(corpus, rec_id):
    if not corpus:
        corpus = default_corpus
    result = mongodb[corpus][DOCUMENTS].remove({"rec_id": rec_id})
    # todo clarify the response
    # result example :
    #{
    #   "connectionId": 20,
    #   "err": null,
    #   "n": 1,
    #   "ok": 1.0
    #}
    return result


def get_uifield(corpus, rec_type):
    if not corpus:
        corpus = default_corpus
    result = mongodb[corpus][UIFIELDS].find_one({"rec_type": rec_type})
    if result:
        return metajson_service.load_dict(result)
    else:
        return None


def get_uifields(corpus):
    if not corpus:
        corpus = default_corpus
    results = mongodb[corpus][UIFIELDS].find()
    if results:
        return metajson_service.load_dict_list(results)
    else:
        return None


def save_uifield(corpus, uifield):
    if not corpus:
        corpus = default_corpus
    # insert or update ?
    rec_type = uifield["rec_type"]
    existing_uifield = get_uifield(corpus, rec_type)
    if existing_uifield:
        uifield["_id"] = existing_uifield["_id"]
    return {"rec_type": rec_type, "_id": str(mongodb[corpus][UIFIELDS].save(uifield))}


def get_type(corpus, type_id):
    if not corpus:
        corpus = default_corpus
    result = mongodb[corpus][TYPES].find_one({"type_id": type_id})
    if result:
        return metajson_service.load_dict(result)
    else:
        return None


def get_types(corpus):
    if not corpus:
        corpus = default_corpus
    results = mongodb[corpus][TYPES].find()
    if results:
        return metajson_service.load_dict_list(results)
    else:
        return None


def save_type(corpus, metatype):
    if not corpus:
        corpus = default_corpus
    # insert or update ?
    type_id = metatype["type_id"]
    existing_type = get_type(corpus, type_id)
    if existing_type:
        metatype["_id"] = existing_type["_id"]
    return {"type_id": type_id, "_id": str(mongodb[corpus][TYPES].save(metatype))}
