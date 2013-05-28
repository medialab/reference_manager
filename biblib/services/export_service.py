#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from bson import json_util
from biblib.metajson import Collection
from biblib.citations import citations_manager


def export_html_webpage(metajson_list, output_path, style="mla"):
    with open(output_path, "w") as output_file:
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


def export_metajson_collection(col_id, col_title, records, output_path):
    if records:
        with open(output_path, "w") as output_file:
            collection = Collection()
            collection["col_id"] = col_id
            collection["title"] = col_title
            collection["records"] = records
            dump = json_util.dumps(collection, ensure_ascii=False, indent=4, encoding="utf-8", sort_keys=True)
            output_file.write(dump)
            return dump


def export_textline(line_list, output_path):
    if line_list:
        with open(output_path, "w") as output_file:
            for line in line_list:
                if line:
                    output_file.write(line)
