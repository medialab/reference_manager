#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Collection
from biblib.citations import citations_manager
from biblib.services import repository_service
from biblib.util import jsonbson


def export_corpus(corpus, output_file_path, output_format, error_file):
    if corpus and output_file_path:
        print "corpus: {}".format(corpus)
        print "output_file_path: {}".format(output_file_path)
        print "output_format: {}".format(output_format)
        # fetch
        metajson_list = repository_service.get_documents(corpus)
        print len(metajson_list)
        # todo
        # export citations
        # export_html_webpage(metajson_list, output_file_path)
        # export json
        export_metajson_collection(corpus, corpus, metajson_list, output_file_path)


def export_html_webpage(metajson_list, output_file_path, style="mla"):
    with open(output_file_path, "w") as output_file:
        header = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n"
        header += "<head>\n"
        header += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>"
        header += "<title>MLA citations test</title>\n"
        header += "</head>\n"
        header += "<body>\n"
        output_file.write(header)

        for document in metajson_list:
            source_info = ""
            if "rec_source" in document:
                source_info += document["rec_source"] + ":"
            if "rec_id" in document:
                source_info += document["rec_id"] + ":"
            citation = citations_manager.cite(document, style, "html")
            output_file.write("<div>" + citation + "</div>\n")

        footer = "</body>\n"
        footer += "</html>"
        output_file.write(footer)


def export_metajson_collection(col_id, col_title, metajson_list, output_file_path):
    if metajson_list:
        with open(output_file_path, "w") as output_file:
            collection = Collection()
            collection["col_id"] = col_id
            collection["title"] = col_title
            collection["records"] = metajson_list
            dump = jsonbson.dumps_bson(collection, True)
            output_file.write(dump)
            return dump


def export_textline(line_list, output_file_path):
    if line_list:
        with open(output_file_path, "w") as output_file:
            for line in line_list:
                if line:
                    output_file.write(line)
