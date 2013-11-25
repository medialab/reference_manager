#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


"Template-Type"
"Series"
"Author-Name"
"Author-Name-First"
"Author-Name-Last"
"Author-Workplace-Name"
"Author-Workplace-Institution"
"Author-Person"
"Title"
"Language"
"Creation-Date"
"Abstract"
"Classification-JEL"
"Keywords"
"X-PublishedAs-Type"
"X-PublishedAs-Book-Title"
"X-PublishedAs-Editor-Name"
"X-PublishedAs-Editor-Workplace-Name"
"X-PublishedAs-Provider-Name"
"X-PublishedAs-Journal"
"X-PublishedAs-Year"
"X-PublishedAs-Volume"
"X-PublishedAs-Issue"
"X-PublishedAs-Pages"
"Publication-Status"
"File-URL"
"File-Format"
"Handle"


def metajson_list_to_repec(documents):
    repec = StringIO()
    for document in documents:
        repec.write(metajson_to_repec(document))
    return repec.getvalue()


def metajson_to_repec(document):
    repec = StringIO()
    write_key_value(repec, "Template-Type", "ReDIF-Paper 1.0")
    write_key_value(repec, "Title", document["title"])
    if "part_volume" in document:
        write_key_value(repec, "X-PublishedAs-Volume", document["part_volume"])
    if "part_issue" in document:
        write_key_value(repec, "X-PublishedAs-Issue", document["part_issue"])
    if "part_page_begin" in document:
        pages = document["part_page_begin"]
        if "part_page_end" in document:
            pages += "-" + document["part_page_end"]
        write_key_value(repec, "X-PublishedAs-Pages", pages)
    if "resources" in document:
        for resource in document["resources"]:
            if "url" in resource and resource["url"]:
                write_key_value(repec, "File-URL", resource["url"])
            if "format_mimetype" in resource and resource["format_mimetype"]:
                write_key_value(repec, "File-Format", resource["format_mimetype"])
    write_key_value(repec, "Handle", document["rec_id"])
    repec.write("\n")
    return repec.getvalue()


def write_key_value(repec, key, value):
    key_format = "".join([key, ": ", value, "\n"])
    repec.write(key_format)
