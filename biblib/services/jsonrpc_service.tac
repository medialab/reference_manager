#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
import locale

from txjsonrpc.web import jsonrpc
from txjsonrpc import jsonrpclib
from twisted.web import server
from twisted.application import service
from twisted.application import internet
from operator import itemgetter

from biblib.citations import citations_manager
from biblib.services import config_service
from biblib.services import crosswalks_service
from biblib.services import repository_service
from biblib.util import console
from biblib.util import exceptions
from biblib.util import jsonbson

# usage with log in the console
# twistd -noy jsonrpc_service.tac -l -

# usage with log in a file
# twistd -noy jsonrpc_service.tac -l server.log

# usage with log in a file and release the console
# twistd -noy jsonrpc_service.tac -l server.log &

port = config_service.config["jsonrpc"]["port"]

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
        request.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        print "REQUEST: %s" % request.content.read()
        return jsonrpc.JSONRPC.render(self, request)

    def _cbRender(self, result, request, id, version):
        print "RESULT: %s" % jsonrpclib.dumps(result, id=id, version=version)
        return jsonrpc.JSONRPC._cbRender(self, result, request, id, version=2.0)

    def jsonrpc_echo(self, x):
            """Return all passed args."""
            return x

    def jsonrpc_save(self, document):
        """ insert or update a reference in the repository
            return object id if ok or error
        """
        doc_bson = jsonbson.json_to_bson(document)
        oid, rec_id = repository_service.save_document(None, doc_bson)
        #jsonbson.bson_to_json(repository_service.save_document(None, doc_bson))
        return {"rec_id": rec_id}

    def jsonrpc_delete(self, rec_id):
        """ delete a reference in the repository
            return object id if ok or error
        """
        return jsonbson.bson_to_json(repository_service.delete_document(None, rec_id))

    def jsonrpc_set_metadata_property(self, rec_id, key, value):
        """ set the value for a property of a metadata
            params:
                - rec_id: rec_id of a metadata record
                - key: property that will be set
                - value: value that will be set
                - format: the format wanted to describe references
            return the asked references in the specified format
            return the modified reference in the specified format
        """
        try:
            metajson_document = repository_service.set_document_property(None, rec_id, key, value)
            return jsonbson.bson_to_json(metajson_document)
        except exceptions.metajsonprc_error, ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_metadata_by_rec_ids(self, rec_ids, format="metajson"):
        """ get metadata of a list of references
            params:
                - rec_ids: list of record ids (rec_id)
                - format: the format wanted to describe references
            return the asked references in the specified format
        """
        try:
            metajson_documents = repository_service.get_documents_by_rec_ids(None, rec_ids)
            print len(metajson_documents)
            results = []
            for metajson_document in metajson_documents:
                if format == "metajson":
                    results.append(jsonbson.bson_to_json(metajson_document))
                else:
                    results.append(crosswalks_service.convert_document(metajson_document, "metajson", format))
            return results
        except exceptions.metajsonprc_error, ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_metadata_by_mongo_ids(self, mongo_ids, format="metajson"):
        """ get metadata of a list of references
            params:
                - mongo_ids: list of mongodb ids (_id)
                - format: the format wanted to describe references
                    (metajson by defaut, metajsonui for user interface)
            return the asked references in the specified format
        """
        try:
            metajson_documents = repository_service.get_documents_by_mongo_ids(None, mongo_ids)
            results = []
            for metajson_document in metajson_documents:
                if format == "metajson":
                    results.append(jsonbson.bson_to_json(metajson_document))
                else:
                    results.append(crosswalks_service.convert_document(metajson_document, "metajson", format))
            return results
        except exceptions.metajsonprc_error, ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_citation_by_rec_ids(self, rec_ids, style="mla", format="html"):
        """ get citations of a list of references
            params:
                - rec_ids: list of known ids
                - style: the style in which to wirte the citations
                - format: the format wanted to describe citations
            return the asked references in the specified format
        """
        try:
            metajson_documents = repository_service.get_documents_by_rec_ids(None, rec_ids)
            results = []
            for metajson_document in metajson_documents:
                result = {}
                result["rec_id"] = metajson_document["rec_id"]
                result[style] = citations_manager.cite(metajson_document, style, format)
                results.append(result)
            return jsonbson.bson_to_json(results)
        except exceptions.metajsonprc_error, ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_search(self, search_query):
        """ search for one or more data from the repository
            params:
                - search_query: a custom SearchQuery object with the query params
        """
        try:
            date_start = datetime.datetime.now()
            search_response = repository_service.search(None, search_query)
            date_end = datetime.datetime.now()
            interval = date_end - date_start
            response_time = "{0:.3f}".format(interval.total_seconds() * 1000)
            search_response["response_time"] = response_time
            return jsonbson.bson_to_json(search_response)
        except exceptions.metajsonprc_error, ex:
            return jsonrpclib.Fault(ex.code, str(ex))

    def jsonrpc_search_mongo(self, mongo_query):
        """ search for one or more data from the repository
            params:
                - mongo_query: search query must respect the mongo query syntax
            return the asked data (in JSON)
        """
        return jsonbson.bson_to_json(repository_service.search_mongo(None, mongo_query))

    def locale_keyfunc(self, keyfunc):
        def locale_wrapper(obj):
            return locale.strxfrm(keyfunc(obj))
        return locale_wrapper

    def type_adaptation(self, type_dict, language, sort):
        # language simplification
        if type_dict and language:
            if "sort" in type_dict:
                sort = type_dict["sort"]
            self.key_language_simplification(type_dict, "labels", "label", language)
            self.key_language_simplification(type_dict, "descriptions", "description", language)
            if "children" in type_dict:
                for child in type_dict["children"]:
                    self.type_adaptation(child, language, sort)
                if sort:
                    #locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
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

    def jsonrpc_type(self, type_id, language):
        """ search for one types from the repository
            params:
                - type_id: type identifier
                - language: language for label and description
            return the asked type (in JSON)
        """
        type_dict = repository_service.get_type(None, type_id)
        self.type_adaptation(type_dict, language, True)
        return jsonbson.bson_to_json(type_dict)

    def jsonrpc_types(self, language):
        """ search for all types from the repository
            params:
                - language: language for label and description
            return the asked type (in JSON)
        """
        type_list = repository_service.get_types(None)
        if type_list:
            results = []
            for type_dict in type_list:
                print "type_id: {}".format(type_dict["type_id"])
                self.type_adaptation(type_dict, language, True)
                results.append(jsonbson.bson_to_json(type_dict))
            return results

    def jsonrpc_uifield(self, rec_type, language):
        """ search for one uifield for user interface
            from the repository
            params:
                - rec_type: document type
                - language: language for label and description
            return the asked uifield for user interface (in JSON)
        """
        uifield_dict = repository_service.get_uifield(None, rec_type)
        self.type_adaptation(uifield_dict, language, False)
        return jsonbson.bson_to_json(uifield_dict)

    def jsonrpc_uifields(self, language):
        """ search for all uifields for user interface
            from the repository
            params:
                - language: language for label and description
            return the asked uifields for user interface (in JSON)
        """
        uifield_list = repository_service.get_uifields(None)
        if uifield_list:
            results = []
            for uifield_dict in uifield_list:
                print "rec_type: {}".format(uifield_dict["rec_type"])
                self.type_adaptation(uifield_dict, language, False)
                results.append(jsonbson.bson_to_json(uifield_dict))
            return results

application = service.Application("References repository web service")
root = References_repository()
site = server.Site(root)
server = internet.TCPServer(port, site)
server.setServiceParent(application)
