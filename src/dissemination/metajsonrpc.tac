#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from txjsonrpc.web import jsonrpc
from txjsonrpc import jsonrpclib
from twisted.web import server
from twisted.internet import reactor
from twisted.application import service, internet

import json
import bson
from bson.json_util import dumps
from metadatas.metajson import Common, Document, Contributor, Identifier, Resource
from repository import mongodb_repository
from citations import citations_manager
from crosswalks import crosswalks_manager

port = 8080

class References_repository(jsonrpc.JSONRPC):
    """
    jsonrpc webservice to propose bibliographic services
    """

    addSlash = True

    def __init__(self):
        jsonrpc.JSONRPC.__init__(self)

    def render(self, request):
        request.setHeader("Access-Control-Allow-Origin", "*")
        request.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        # request.setHeader("Access-Control-Request-Headers", "Origin, X-Requested-With, Content-Type, Accept, content-type")
        print "REQUEST: %s" % request.content.read()
        return jsonrpc.JSONRPC.render(self, request)

    def _cbRender(self, result, request, id, version):                      
        print "RESULT: %s" % jsonrpclib.dumps(result, id=id, version=version)
        return jsonrpc.JSONRPC._cbRender(self, result, request, id, version=2.0)

    def format_bson(self, bson_data) :
        return bson.json_util.dumps(bson_data,ensure_ascii=False,indent=4,encoding="utf-8",sort_keys=True)

    def jsonrpc_echo(self, x):
        """Return all passed args."""
        return x

    def jsonrpc_save(self, ref):
        """ insert or update a reference in the repository 
            return object id if ok or error
        """
        json_ref = json.loads(ref)
        print json.dumps(json_ref, indent = 4, ensure_ascii = False, encoding = "utf-8", sort_keys = True)
        return self.format_bson(mongodb_repository.save_metajson(json_ref))

    def jsonrpc_metadata_by_rec_ids(self, rec_ids, format="metajson"):
        """ get metadata of a list of references
            params : 
                - ids : list of record ids (rec_id)
                - format : the format wanted to describe references  
            return the asked references in the specified format
        """
        metajson_document = mongodb_repository.get_by_rec_ids(rec_ids)
        if format == "metajson" :
            return self.format_bson(metajson_document)
        else :
            return crosswalks_manager.convert_document(metajson_document, "metajson", format)

    def jsonrpc_metadata_by_mongo_ids(self, mongo_ids, format="metajson"):
        """ get metadata of a list of references
            params : 
                - ids : list of mongodb ids (_id)
                - format : the format wanted to describe references  
            return the asked references in the specified format
        """
        metajson_document = mongodb_repository.get_by_mongo_ids(mongo_ids)
        if format == "metajson" :
            return self.format_bson(metajson_document)
        else :
            return crosswalks_manager.convert_document(metajson_document, "metajson", format)

    def jsonrpc_citation_by_rec_ids(self, rec_ids, style="mla", format="html"):
        """ get citations of a list of references
            params : 
                - ids : list of known ids
                - style : the style in which to wirte the citations
                - format : the format wanted to describe citations  
            return the asked references in the specified format
        """
        document_list = mongodb_repository.get_by_rec_ids(rec_ids)
        if document_list :
            results = []
            for document in document_list :
                results.append(citations_manager.cite(document, style, format))
            return results

    def jsonrpc_search(self, mongoquery):
        """ search for one or more data from the repository
            params : 
                - mongoquery : search query must respect the mongoquery syntax
            return the asked data (in JSON)
        """
        pass

application = service.Application("References repository web service")
root = References_repository()
site = server.Site(root)
server = internet.TCPServer(port, site)
server.setServiceParent(application)

# usage with log in the console
# twistd -noy metajsonrpc.tac -l -

# usage with log in a file
# twistd -noy metajsonrpc.tac -l server.log

# usage with log in a file and release the console
# twistd -noy metajsonrpc.tac -l server.log $

