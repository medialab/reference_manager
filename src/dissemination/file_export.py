#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from bson import json_util
from metadatas.metajson import Collection
from citations import citations_manager


def export_html_webpage(document_list, output_file_name, style="mla"):
    with open(output_file_name, "w") as biblio_file:
        header = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n"
        header += "<head>\n"
        header += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>"
        header += "<title>MLA citations test</title>\n"
        header += "</head>\n"
        header += "<body>\n"
        biblio_file.write(header)

        for document in document_list:
            source_info = ""
            if "rec_source" in document:
                source_info += document["rec_source"] + ":"
            if "rec_id" in document:
                source_info += document["rec_id"] + ":"
            citation = citations_manager.cite(document, style, "html")
            biblio_file.write("<div>" + citation + "</div>\n")

        footer = "</body>\n"
        footer += "</html>"
        biblio_file.write(footer)


def export_metajson(document_list, output_file_name):
    with open(output_file_name, "w") as metajson_file:
        collection = Collection()
        collection["col_id"] = "aime"
        collection["title"] = "AIME references"
        collection["records"] = document_list
        metajson_file.write(json_util.dumps(collection, ensure_ascii=False, indent=4, encoding="utf-8", sort_keys=True))
