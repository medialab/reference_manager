#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# mongod --dbpath /Users/jrault/Documents/SciencesPo/Projets/biblib/mongodb

import pymongo
from bson.objectid import ObjectId
from bson.errors import InvalidId
from biblib.metajson import SearchResponse
from biblib.services import config_service
from biblib.services import date_service
from biblib.services import metajson_service
from biblib.util import exceptions
from biblib.util import jsonbson

DOCUMENTS = "documents"
AGENTS = "agents"
TYPES = "types"
FIELDS = "fields"

config = config_service.config["mongodb"]
default_corpus = config_service.config["default_corpus"]

try:
    mongodb = pymongo.MongoClient(config['host'], config['port'])
except pymongo.errors.ConnectionFailure as e:
    print "ERROR: connexion failure to MongoDB : {}".format(e)

# examples:
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': {'$in': update_ids}}, {'$set': {'crawling_status': crawling_statuses.RUNNING}}, multi=True, safe=True)
# update_ids = [job['_id'] for job in mongodb[config['mongo-scrapy']['jobListCol']].find({'_id': {'$in': finished_ids}, 'crawling_status': {'$nin': [crawling_statuses.CANCELED, crawling_statuses.FINISHED]}}, fields=['_id'])]
# resdb = mongodb[config['mongo-scrapy']['jobListCol']].update({'_id': res['jobid']}, {'$set': {'webentity_id': webentity_id, 'nb_pages': 0, 'nb_links': 0, 'crawl_arguments': args, 'crawling_status': crawling_statuses.PENDING, 'indexing_status': indexing_statuses.PENDING, 'timestamp': ts}}, upsert=True, safe=True)
# return db[config['mongo-scrapy']['jobLogsCol']].insert([{'_job': _id, 'timestamp': timestamp, 'log': msg} for _id in jobid])


def list_corpora():
    return [x for x in mongodb.database_names() if x != "local"]


def create_corpus(corpus):
    mongodb[corpus]


def delete_corpus(corpus):
    mongodb.drop_database(corpus)


def empty_corpus(corpus):
    mongodb[corpus][DOCUMENTS].drop()
    mongodb[corpus][AGENTS].drop()
    mongodb[corpus][TYPES].drop()
    mongodb[corpus][FIELDS].drop()


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
    mongodb[corpus][FIELDS].ensure_index([index_id], safe=True)


def get_document_by_mongo_id(corpus, mongo_id):
    if not corpus:
        corpus = default_corpus
    result = mongodb[corpus][DOCUMENTS].find_one({'_id': ObjectId(mongo_id)})
    if result:
        return metajson_service.load_dict(result)
    else:
        raise exceptions.metajsonprc_error(3)


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
        raise exceptions.metajsonprc_error(4)


def set_document_property(corpus, rec_id, key, value, role):
    metajson_document = get_document_by_rec_id(corpus, rec_id)
    metajson_document[key] = value
    save_document(corpus, metajson_document, role)
    return metajson_document


def get_document_by_rec_id(corpus, rec_id):
    if not corpus:
        corpus = default_corpus
    result = mongodb[corpus][DOCUMENTS].find_one({"rec_id": rec_id})
    if result:
        return metajson_service.load_dict(result)
    else:
        raise exceptions.metajsonprc_error(1)


def get_documents_by_rec_ids(corpus, rec_ids):
    if not corpus:
        corpus = default_corpus
    results = mongodb[corpus][DOCUMENTS].find({"rec_id": {"$in": rec_ids}})
    # results is a pymongo.cursor.Cursor
    if results:
        return metajson_service.load_dict_list(results)
    else:
        raise exceptions.metajsonprc_error(2)


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
        raise exceptions.metajsonprc_error(40)

    # filter_class -> collection
    collection = None
    if "filter_class" not in search_query or search_query["filter_class"] not in ["Document", "Agent", "Person", "OrgUnit", "Event", "Family"]:
        raise exceptions.metajsonprc_error(40)
    elif search_query["filter_class"] == "Document":
        collection = DOCUMENTS
    elif search_query["filter_class"] in ["Agent", "Person", "OrgUnit", "Event", "Family"]:
        collection = AGENTS

    # other filters
    # todo: filter_peer_review, filter_with_full_text, filter_favorite

    filter_query = []
    if "filter_date_end" in search_query:
        filter_date_end = date_service.parse_date(search_query["filter_date_end"])
        filter_query.append({"date_sort": {"$lte": filter_date_end}})
    if "filter_date_begin" in search_query:
        filter_date_begin = date_service.parse_date(search_query["filter_date_begin"])
        filter_query.append({"date_sort": {"$gte": filter_date_begin}})
    if "filter_languages" in search_query:
        filter_query.append({"languages": {"$in": search_query["filter_languages"]}})
    if "filter_types" in search_query:
        filter_query.append({"rec_type": {"$in": search_query["filter_types"]}})
    if "filter_status" in search_query:
        # "private", "pending", "rejected", "published", "deleted"
        filter_query.append({"rec_status": {"$in": search_query["filter_status"]}})

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

            # split value
            values = search_term["value"].replace(",", " ").split()
            
            # index
            if "index" not in search_term:
                # useless
                raise exceptions.metajsonprc_error(40)
            elif search_term["index"] == "all":
                all_terms = []
                if values:
                    for value in values:
                        all_terms.append({"rec_id": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"identifiers.value": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"title": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"title_sub": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"publishers": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"is_part_ofs.title": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"is_part_ofs.is_part_ofs.title": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"creators.agent.name_family": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"creators.agent.name_given": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"creators.agent.name": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"creators.agent.title": {"$regex": value, "$options": 'i'}})
                        all_terms.append({"rec_type": {"$regex": value, "$options": 'i'}})
                    search_indexes.append({"$or": all_terms})

            elif search_term["index"] == "identifier":
                try:
                    obid = ObjectId(search_term["index"])
                    search_indexes.append({"_id": obid})
                except (InvalidId, TypeError):
                    search_indexes.append({"$or": [{"rec_id": {"$regex": search_term["value"], "$options": 'i'}}, {"identifiers.value": {"$regex": search_term["value"], "$options": 'i'}}]})

            elif search_term["index"] == "title":
                title_terms = []
                for value in values:
                    title_terms.append({"title": {"$regex": value, "$options": 'i'}})
                search_indexes.append({"$and": title_terms})

            elif search_term["index"] == "is_part_of":
                is_part_of_terms = []
                for value in values:
                    is_part_of_terms.append({"is_part_ofs.title": {"$regex": value, "$options": 'i'}})
                    is_part_of_terms.append({"is_part_ofs.is_part_ofs.title": {"$regex": value, "$options": 'i'}})
                search_indexes.append({"$or": is_part_of_terms})

            elif search_term["index"] == "creator":
                creator_terms = []
                for value in values:
                    creator_terms.append({"creators.agent.name_family": {"$regex": value, "$options": 'i'}})
                    creator_terms.append({"creators.agent.name_given": {"$regex": value, "$options": 'i'}})
                    creator_terms.append({"creators.agent.name": {"$regex": value, "$options": 'i'}})
                    creator_terms.append({"creators.agent.title": {"$regex": value, "$options": 'i'}})
                search_indexes.append({"$or": creator_terms})

            elif search_term["index"] == "creator_id":
                search_indexes.append({"creators.agent.rec_id": search_term["value"]})

            elif search_term["index"] == "affiliation":
                search_indexes.append({"creators.affiliation.name": {"$regex": search_term["value"], "$options": 'i'}})

            elif search_term["index"] == "affiliation_id":
                search_indexes.append({"creators.affiliation.rec_id": search_term["value"]})

            elif search_term["index"] == "publisher":
                publisher_terms = []
                for value in values:
                    publisher_terms.append({"publishers": {"$regex": value, "$options": 'i'}})
                    publisher_terms.append({"is_part_ofs.publishers": {"$regex": value, "$options": 'i'}})
                    publisher_terms.append({"is_part_ofs.is_part_ofs.publishers": {"$regex": value, "$options": 'i'}})
                search_indexes.append({"$or": publisher_terms})

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

    # combine filter_query and search_indexes
    mongo_args = filter_query
    mongo_args.extend(search_indexes)

    # Generate the mongo query
    if mongo_args:
        mongo_query = {"$and": mongo_args}
    else:
        # search all
        mongo_query = {}
    print "mongo_query:"
    print jsonbson.dumps_bson(mongo_query, True)

    mongo_response = mongodb[corpus][collection].find(mongo_query)
    print mongo_response
    if mongo_response:
        records = metajson_service.load_dict_list(mongo_response)
        records_total_count = len(records)
    else:
        records = []
        records_total_count = 0

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


def save_document(corpus, document, role):
    if not corpus:
        corpus = default_corpus
    # Recover already saved fields that this role can't view or edit
    if "rec_id" in document and role is not None:
        rec_type = document["rec_type"]
        field = get_field(corpus, rec_type)
        recovered_fields = []
        for child in field["children"]:
            if "roles" in child:
                roles = child["roles"]
                if role not in roles:
                    recovered_fields.append(child["property"])
        if recovered_fields:
            try:
                saved_doc = get_document_by_rec_id(corpus, document["rec_id"])
                if saved_doc is not None:
                    for field in recovered_fields:
                        if field in saved_doc:
                            document[field] = saved_doc[field]
            except:
                pass
    # Enhance MetaJSON
    document = metajson_service.enhance_metajson(document)
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


def get_field(corpus, rec_type):
    if not corpus:
        corpus = default_corpus
    result = mongodb[corpus][FIELDS].find_one({"rec_type": rec_type})
    if result:
        return metajson_service.load_dict(result)
    else:
        return None


def get_fields(corpus):
    if not corpus:
        corpus = default_corpus
    results = mongodb[corpus][FIELDS].find()
    if results:
        return metajson_service.load_dict_list(results)
    else:
        return None


def save_field(corpus, field):
    if not corpus:
        corpus = default_corpus
    # insert or update ?
    rec_type = field["rec_type"]
    existing_field = get_field(corpus, rec_type)
    if existing_field:
        field["_id"] = existing_field["_id"]
    return {"rec_type": rec_type, "_id": str(mongodb[corpus][FIELDS].save(field))}


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

