#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.citations import citations_manager


def metajson_to_html_string(document, output_style):
    source_info = ""
    if "rec_source" in document and document["rec_source"]:
        source_info += document["rec_source"] + ":"
    if "rec_id" in document and document["rec_id"]:
        source_info += document["rec_id"] + ":"
    citation = citations_manager.cite(document, output_style, "html")
    return "<div>" + citation + "</div>\n"


def metajson_list_to_html_string(document_list, col_title, output_style):
    result = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n"
    result += "<head>\n"
    result += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>"
    if col_title:
        result += "<title>" + col_title + "</title>\n"
    else:
        result += "<title>BibLib HTML export</title>\n"
    result += "</head>\n"
    result += "<body>\n"
    for document in document_list:
        result += metajson_to_html_string(document, output_style)
    result = "</body>\n"
    result += "</html>"
    return result
