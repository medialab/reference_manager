#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import json
from referencemanager.cloud import crossref
from referencemanager.services import export_service


def test():
    base_dir = os.path.join(os.getcwd(), "data")
    print "base_dir: " + base_dir

    openurl = "url_ver=Z39.88-2004&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rft.atitle=Isolation of a common receptor for coxsackie B&rft.jtitle=Science&rft.aulast=Bergelson&rft.auinit=J&rft.date=1997&rft.volume=275&rft.spage=1320&rft.epage=1323"
    metajson_list = crossref.query_openurl_and_retrieve_metadata(openurl, True)
    if metajson_list:
        output_path = os.path.join(base_dir, "result", "result_crossref_metajon.json")
        export_service.export_metajson(metajson_list, output_path)
        print json.dumps(metajson_list, indent=4, ensure_ascii=False, encoding="utf-8", sort_keys=True)
    else:
        assert False
