#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import locale
import logging
import traceback

from txjsonrpc.web import jsonrpc
from txjsonrpc import jsonrpclib
from twisted.web import server
from twisted.application import service
from twisted.application import internet
from operator import itemgetter

from biblib.citations import citations_manager
from biblib.services import config_service
from biblib.services import crosswalks_service
from biblib.services import metajson_service
from biblib.services import repository_service
from biblib.util import console
from biblib.util import constants
from biblib.util import exceptions
from biblib.util import jsonbson

# usage with log in the console
# twistd -noy jsonrpc_service.tac -l -

# usage with log in a file
# twistd -noy jsonrpc_service.tac -l server.log

# usage with log in a file and release the console
# twistd -noy jsonrpc_service.tac -l server.log &

port = config_service.config["jsonrpc"]["port"]
default_corpus = config_service.config["default_corpus"]

console.setup_console()


class References_repository(jsonrpc.JSONRPC):
    """
    jsonrpc webservices to propose bibliographic services
    """

    addSlash = True

    def __init__(self):
        jsonrpc.JSONRPC.__init__(self)

    def render(self, request):
        request.setHeader("Access-Control-Allow-Origin", "*")
        request.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS') 
        request.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        logging.debug("REQUEST: {}".format(request.content.read()))
        return jsonrpc.JSONRPC.render(self, request)

    def _cbRender(self, result, request, id, version):
        logging.debug("RESULT: {}".format(jsonrpclib.dumps(result, id=id, version=version)))
        return jsonrpc.JSONRPC._cbRender(self, result, request, id, version=2.0)

    def jsonrpc_echo(self, x):
        """ Return all passed args.
            params:
                - corpus: the corpus 
        """
        return x

    def jsonrpc_list_corpora(self):
        """ Return the list of corpora"""
        return repository_service.list_corpora()

    def jsonrpc_default_corpus(self):
        """ Return the default corpus"""
        return default_corpus

    def jsonrpc_save(self, corpus, document, role=None):
        """ insert or update a reference in the repository
            return object id if ok or error
            params:
                - corpus: the corpus
                - document: the document metadata to save 
                - role: the user role

        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        # role correction
        if role == "":
            role = None
        try:
            document["rec_modified_date"] = datetime.now().isoformat()
            doc_bson = jsonbson.json_to_bson(document)
            oid, rec_id = repository_service.save_document(corpus, doc_bson, role)
            return {"rec_id": rec_id}
        except Exception as ex:
            traceback.print_exc()
            return jsonrpclib.Fault(100, str(ex))

    def jsonrpc_delete(self, corpus, rec_id):
        """ delete a reference in the repository
            return object id if ok or error
            params:
                - corpus: the corpus 
                - rec_id: rec_id of a metadata record
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        return jsonbson.bson_to_json(repository_service.delete_document(corpus, rec_id))

    def jsonrpc_set_metadata_property(self, corpus, rec_id, key, value, role=None):
        """ set the value for a property of a metadata
            params:
                - corpus: the corpus 
                - rec_id: rec_id of a metadata record
                - key: property that will be set
                - value: value that will be set
                - role: the user role
            return the asked references in the specified format
            return the modified reference in the specified format
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        # role correction
        if role == "":
            role = None
        try:
            metajson_document = repository_service.set_document_property(corpus, rec_id, key, value, role)
            return jsonbson.bson_to_json(metajson_document)
        except exceptions.metajsonprc_error as ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_metadata_by_rec_ids(self, corpus, rec_ids, output_format=constants.FORMAT_METAJSON):
        """ get metadata of a list of references
            params:
                - corpus: the corpus 
                - rec_ids: list of record ids (rec_id)
                - output_format: the format wanted to describe references
            return the asked references in the specified format
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        try:
            metajson_documents = repository_service.get_documents_by_rec_ids(corpus, rec_ids)
            results = []
            for metajson_document in metajson_documents:
                if output_format == constants.FORMAT_METAJSON:
                    results.append(jsonbson.bson_to_json(metajson_document))
                else:
                    results.append(crosswalks_service.convert_native(metajson_document, constants.FORMAT_METAJSON, output_format, corpus, corpus, False, False))
            return results
        except exceptions.metajsonprc_error as ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_metadata_by_mongo_ids(self, corpus, mongo_ids, output_format=constants.FORMAT_METAJSON):
        """ get metadata of a list of references
            params:
                - corpus: the corpus 
                - mongo_ids: list of mongodb ids (_id)
                - format: the format wanted to describe references
                    (metajson by defaut, metajsonui for user interface)
            return the asked references in the specified format
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        try:
            metajson_documents = repository_service.get_documents_by_mongo_ids(corpus, mongo_ids)
            results = []
            for metajson_document in metajson_documents:
                if output_format == constants.FORMAT_METAJSON:
                    results.append(jsonbson.bson_to_json(metajson_document))
                else:
                    results.append(crosswalks_service.convert_native(metajson_document, constants.FORMAT_METAJSON, output_format, corpus, corpus, False, False))
            if results:
                return results
            else:
                return jsonrpclib.Fault(2, exceptions.metajsonprc_error_code_to_message[2])
        except exceptions.metajsonprc_error as ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_citation_by_rec_ids(self, corpus, rec_ids, style="mla", format="html"):
        """ get citations for a list of metadatas by their rec_ids
            params:
                - corpus: the corpus 
                - rec_ids: list of known ids
                - style: the style in which to format the citations (mla by default)
                - format: the format wanted to describe citations (html by default)
            return the asked citations in the specified format
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        try:
            metajson_documents = repository_service.get_documents_by_rec_ids(corpus, rec_ids)
            results = []
            for metajson_document in metajson_documents:
                result = {}
                result["rec_id"] = metajson_document["rec_id"]
                result[style] = citations_manager.cite(metajson_document, style, format)
                results.append(result)
            if results:
                return jsonbson.bson_to_json(results)
            else:
                return jsonrpclib.Fault(2, exceptions.metajsonprc_error_code_to_message[2])
        except exceptions.metajsonprc_error as ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_preview(self, metadatas, styles, formats):
        """ Add formated citations inside each metadata
            params:
                - metadatas: list of metadatas in the MetaJSON metadata format
                - styles: the list of bibliographic style in which to format citations
                - formats: the list of citation result format wanted to format citations
            return the metadata with citations formated inside
        """
        try:
            if metadatas:
                metadatas = metajson_service.load_dict_list(metadatas)
                results = []
                for metadata in metadatas:
                    if "rec_class" in metadata and metadata["rec_class"] == constants.REC_CLASS_DOCUMENT:
                        results.append(citations_manager.add_citations_to_metadata(metadata, styles, formats))
                return jsonbson.bson_to_json(results)
            else:
                raise exceptions.metajsonprc_error(0)
        except exceptions.metajsonprc_error as ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_search(self, corpus, search_query):
        """ search for one or more data from the repository
            params:
                - corpus: the corpus 
                - search_query: a custom SearchQuery object with the query params
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        try:
            date_begin = datetime.datetime.now()
            search_response = repository_service.search(corpus, search_query)
            date_end = datetime.datetime.now()
            interval = date_end - date_begin
            response_time = "{0:.3f}".format(interval.total_seconds() * 1000)
            search_response["response_time"] = response_time
            return jsonbson.bson_to_json(search_response)
        except exceptions.metajsonprc_error as ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_search_mongo(self, corpus, mongo_query):
        """ search for one or more data from the repository
            params:
                - corpus: the corpus 
                - mongo_query: search query must respect the mongo query syntax
            return the asked data (in JSON)
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        return jsonbson.bson_to_json(repository_service.search_mongo(corpus, mongo_query))

    def jsonrpc_type(self, corpus, type_id, language):
        """ search for one types from the repository
            params:
                - corpus: the corpus 
                - type_id: type identifier
                - language: language for label and description
            return the asked type (in JSON)
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        type_dict = repository_service.get_type(corpus, type_id)
        self.type_adaptation(type_dict, language, True, None)
        return jsonbson.bson_to_json(type_dict)

    def jsonrpc_types(self, corpus, language):
        """ search for all types from the repository
            params:
                - corpus: the corpus 
                - language: language for label and description
            return the asked type (in JSON)
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        type_list = repository_service.get_types(corpus)
        if type_list:
            results = []
            for type_dict in type_list:
                logging.debug("type_id: {}".format(type_dict["type_id"]))
                self.type_adaptation(type_dict, language, True, None)
                results.append(jsonbson.bson_to_json(type_dict))
            return results

    def jsonrpc_field(self, corpus, rec_type, language, role=None):
        """ search for one field for user interface
            from the repository
            params:
                - corpus: the corpus 
                - rec_type: document type
                - language: language for label and description
                - role: the user role
            return the asked field for user interface (in JSON)
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        # role correction$
        if role == "":
            role = None
        field_dict = repository_service.get_field(corpus, rec_type)
        self.type_adaptation(field_dict, language, False, role)
        return jsonbson.bson_to_json(field_dict)

    def jsonrpc_fields(self, corpus, language, role=None):
        """ search for all fields for user interface
            from the repository
            params:
                - corpus: the corpus 
                - language: language for label and description
                - role: the user role
            return the asked fields for user interface (in JSON)
        """
        # default corpus management
        if not corpus:
            corpus = default_corpus
        # role correction
        if role == "":
            role = None
        field_list = repository_service.get_fields(corpus)
        if field_list:
            results = []
            for field_dict in field_list:
                logging.debug("rec_type: {}".format(field_dict["rec_type"]))
                self.type_adaptation(field_dict, language, False, role)
                results.append(jsonbson.bson_to_json(field_dict))
            return results

    def locale_keyfunc(self, keyfunc):
        def locale_wrapper(obj):
            #logging.debug(locale.getlocale(locale.LC_COLLATE))
            #logging.debug(locale.strxfrm(keyfunc(obj)).lower())
            return locale.strxfrm(keyfunc(obj))
        return locale_wrapper

    def type_adaptation(self, type_dict, language, sort, role):
        # language simplification
        if type_dict and language:
            if "sort" in type_dict:
                sort = type_dict["sort"]
            self.key_language_simplification(type_dict, "labels", "label", language)
            self.key_language_simplification(type_dict, "descriptions", "description", language)
            if "children" in type_dict:
                if role is not None:
                    type_dict["children"] = [child for child in type_dict["children"] if "roles" not in child or role in child["roles"]]
                for child in type_dict["children"]:
                    self.type_adaptation(child, language, sort, role)
                if sort:
                    #locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
                    #locale.setlocale(locale.LC_ALL, ("no", None))
                    type_dict["children"] = sorted(type_dict["children"], key=self.locale_keyfunc(itemgetter('label')))

    def key_language_simplification(self, type_dict, key_old, key_new, language):
        if key_old and key_new:
            if key_old in type_dict:
                result = ""
                if language in type_dict[key_old]:
                    result = type_dict[key_old][language]
                else:
                    result = type_dict[key_old]["en"]
                del type_dict[key_old]
                type_dict[key_new] = result

application = service.Application("Biblib JSON-RPC services")
root = References_repository()
site = server.Site(root)
server = internet.TCPServer(port, site)
server.setServiceParent(application)
