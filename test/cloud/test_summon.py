#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
from biblib.cloud import summon
from biblib.services import crosswalks_service
from biblib.services import metajson_service
from biblib.util import console
from biblib.util import constants
from biblib.util import jsonbson


def test():
    base_dir = os.path.join(os.getcwd(), "data")
    print "base_dir: " + base_dir

    #query_string = "s.q=europe&s.cmd%5B%5D=addFacetValueFilters%28IsFullText%2Ctrue%29&s.fq%5B%5D=SourceType%3A%28%22Library+Catalog%22%29&s.fvf%5B%5D=ContentType%2CNewspaper+Article%2Ct&s.fvf%5B%5D=ContentType%2CBook+Review%2Ct&s.fvf%5B%5D=ContentType%2CDissertation%2Ct"
    #query_string = "s.cmd=addFacetValueFilters(ContentType,Book+Review)&s.fvf%5B%5D=ContentType,Journal+Article,f&s.fvf%5B%5D=ContentType,Dissertation,t&s.fvf%5B%5D=IsFullText,true,f&s.fvf%5B%5D=ContentType,Newspaper+Article,t&s.q=europe"
    #query_string = "s.cmd=addFacetValueFilters(ContentType,Journal+Article)&s.fvf=IsFullText,true,f&s.q=europe+federal"
    #query_string = "s.fvf%5B%5D=ContentType%2CJournal+Article%2Cf&s.fvf%5B%5D=IsFullText%2Ctrue%2Cf&s.q=europe+federal&s.cmd=addFacetValueFilters(ContentType,Dissertation)%20removeFacetValueFilter(ContentType,Journal%20Article)"
    #query_string = "s.fvf%5B%5D=ContentType%2CConference+Proceeding%2Cf&s.fvf%5B%5D=ContentType%2CData+Set%2Cf&s.fvf%5B%5D=IsFullText%2Ctrue%2Cf&s.fvf%5B%5D=ContentType%2CNewspaper+Article%2Cf&s.fvf%5B%5D=ContentType%2CTrade+Publication+Article%2Cf&s.ps=50&s.q=europe+federal&s.cmd=removeFacetValueFilter(ContentType,Newspaper%20Article)%20removeFacetValueFilter(ContentType,Trade%20Publication%20Article)%20removeFacetValueFilter(ContentType,Data%20Set)"
    #query_string = "s.fvf%5B%5D=ContentType%2CConference+Proceeding%2Cf&s.fvf%5B%5D=IsFullText%2Ctrue%2Cf&s.ps=50&s.q=europe+federal&s.cmd=addFacetValueFilters(ContentType,Data+Set)"
    #query_string = "s.q=Organized+Crime+and+States"
    # Thesis:
    #query_string = "s.cmd=addFacetValueFilters(ContentType,Dissertation)&s.q=social"
    # Video:
    #query_string = "s.q=social&s.fvf%5B%5D=ContentType%2CVideo+Recording%2Cf"
    # EditedBook
    #query_string = "s.q=ouvrage+collectif&s.cmd=addFacetValueFilters(ContentType,Book+%2F+eBook)"
    query_string = "s.fvf%5B%5D=ContentType%2CConference+Proceeding%2Cf"
    summon_response = summon.summon_query(query_string)
    metajson_list = crosswalks_service.convert_json(summon_response, constants.FORMAT_SUMMONJSON, constants.FORMAT_METAJSON, "summon", False)
    collection = metajson_service.create_collection("summon_test", "Summon Test", metajson_list)
    print jsonbson.dumps_json(collection, True)

#console.setup_console()
#test()
