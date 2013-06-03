#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json

from bson import json_util
from txjsonrpc.web import jsonrpc
from txjsonrpc import jsonrpclib
from twisted.web import server
from twisted.application import service, internet

from biblib.citations import citations_manager
from biblib.crosswalks import metajsonui_crosswalk
from biblib.services import config_service
from biblib.services import crosswalks_service
from biblib.services import repository_service

# usage with log in the console
# twistd -noy jsonrpc_service.tac -l -

# usage with log in a file
# twistd -noy jsonrpc_service.tac -l server.log

# usage with log in a file and release the console
# twistd -noy jsonrpc_service.tac -l server.log &

port = config_service.config["jsonrpc"]["port"]


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

    def format_bson(self, bson_data):
        return json_util.dumps(bson_data, ensure_ascii=False, indent=4, encoding="utf-8", sort_keys=True)

    def jsonrpc_echo(self, x):
        """Return all passed args."""
        return x

    def jsonrpc_save(self, document):
        """ insert or update a reference in the repository
            return object id if ok or error
        """
        json_doc = json.loads(document)
        print json.dumps(json_doc, indent=4, ensure_ascii=False, encoding="utf-8", sort_keys=True)
        return self.format_bson(repository_service.save_document(None, json_doc))

    def jsonrpc_save_ui(self, document_ui):
        """ insert or update a reference in the repository
            return object id if ok or error
        """
        json_doc_ui = json.loads(document_ui)
        print json.dumps(json_doc_ui, indent=4, ensure_ascii=False, encoding="utf-8", sort_keys=True)
        document = metajsonui_crosswalk.metajsonui_to_metajson(json_doc_ui)
        print json.dumps(document, indent=4, ensure_ascii=False, encoding="utf-8", sort_keys=True)
        return self.format_bson(repository_service.save_document(None, document))

    def jsonrpc_metadata_by_rec_ids(self, rec_ids, format="metajson"):
        """ get metadata of a list of references
            params:
                - ids: list of record ids (rec_id)
                - format: the format wanted to describe references
            return the asked references in the specified format
        """
        metajson_document = repository_service.get_documents_by_rec_ids(None, rec_ids)
        if format == "metajson":
            return self.format_bson(metajson_document)
        else:
            return crosswalks_service.convert_document(metajson_document, "metajson", format)

    def jsonrpc_metadata_by_mongo_ids(self, mongo_ids, format="metajson"):
        """ get metadata of a list of references
            params:
                - ids: list of mongodb ids (_id)
                - format: the format wanted to describe references
                    (metajson by defaut, metajsonui for user interface)
            return the asked references in the specified format
        """
        metajson_document = repository_service.get_documents_by_mongo_ids(None, mongo_ids)
        if format == "metajson":
            return self.format_bson(metajson_document)
        elif format == "metajsonui":
            return self.format_bson(metajsonui_crosswalk.metajson_to_metajsonui(metajson_document))
        else:
            return crosswalks_service.convert_document(metajson_document, "metajson", format)

    def jsonrpc_citation_by_rec_ids(self, rec_ids, style="mla", format="html"):
        """ get citations of a list of references
            params:
                - ids: list of known ids
                - style: the style in which to wirte the citations
                - format: the format wanted to describe citations
            return the asked references in the specified format
        """
        document_list = repository_service.get_documents_by_rec_ids(None, rec_ids)
        if document_list:
            results = []
            for document in document_list:
                result = {}
                result["rec_id"] = document["rec_id"]
                result[style] = citations_manager.cite(document, style, format)
                results.append(result)
            return self.format_bson(results)

    def jsonrpc_search(self, query):
        """ search for one or more data from the repository
            params:
                - mongoquery: search query must respect the mongoquery syntax
            return the asked data (in JSON)
        """
        return self.format_bson(repository_service.search_documents(None, query))

    def jsonrpc_types(self, type_id, language):
        """ search for one or more types from the repository
            params:
                - type_id: types list identifier
                - language: language for label and description
            return the asked types (in JSON)
        """
        # todo filter LangString by language, send only children
        return self.format_bson(repository_service.get_type(None, type_id))

    def jsonrpc_uifields(self, rec_type, language):
        """ search for one or more uifields for user interface
            from the repository
            params:
                - rec_type: document type
                - language: language for label and description
            return the asked uifields for user interface (in JSON)
        """
        # todo filter LangString by language
        return self.format_bson(repository_service.get_uifield(None, rec_type))


application = service.Application("References repository web service")
root = References_repository()
site = server.Site(root)
server = internet.TCPServer(port, site)
server.setServiceParent(application)
