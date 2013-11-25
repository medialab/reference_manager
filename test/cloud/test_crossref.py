#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
from biblib.cloud import crossref
from biblib.services import io_service


def test():
    base_dir = os.path.join(os.getcwd(), "data")
    print "base_dir: " + base_dir

    openurl = "url_ver=Z39.88-2004&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rft.atitle=Isolation of a common receptor for coxsackie B&rft.jtitle=Science&rft.aulast=Bergelson&rft.auinit=J&rft.date=1997&rft.volume=275&rft.spage=1320&rft.epage=1323"
    metajson_list = crossref.query_openurl_and_retrieve_metadata(openurl, True)
    if metajson_list:
        output_path = os.path.join(base_dir, "result", "result_crossref_metajon.json")
        print io_service.export_metajson_collection("test_crossref", "Crossref import test", metajson_list, output_path)
    else:
        assert False
