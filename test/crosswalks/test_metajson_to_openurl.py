#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
from referencemanager.crosswalks import metajson_to_openurl
from referencemanager.services import import_service
from referencemanager.services import export_service


def test():
    base_dir = os.path.join(os.getcwd(), "data")
    print "base_dir: " + base_dir

    input_dir = os.path.join(base_dir, "result")
    openurl_list = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_dir, file_name)
            print file_path

            metajson_list = import_service.load_metajson_file(file_path)
            if metajson_list:
                for metajson in metajson_list:
                    openurl = metajson_to_openurl.convert_metajson_document_to_openurl(metajson)
                    print openurl
                    openurl_list.append(openurl)

    if openurl_list:
        output_path = os.path.join(base_dir, "result", "result_metajon_to_openurl.txt")
        export_service.export_textline(openurl_list, output_path)
    else:
        assert False
