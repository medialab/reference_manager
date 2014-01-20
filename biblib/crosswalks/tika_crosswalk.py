#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging

from biblib.metajson import Document
from biblib.metajson import Resource


def tika_to_metajson(tika, source):
    # convert str to dict
    tikadict = {}
    lines = tika.split("\n")
    for line in lines:
        if line:
            linesplit = line.replace("\"","").split(",")
            if linesplit and len(linesplit) > 1:
                key = linesplit[0]
                value = linesplit[1]
                tikadict[key] = value
    return tikadict_to_metajson(tikadict, source)


def tikadict_to_metajson(tikadict, source):
    document = Document()
    resource = Resource()

    if source:
        document["source"] = source

    # document
    # dc:title -> document title
    if "dc:title" in tikadict:
        document["title"] = tikadict["dc:title"]
    # dcterms:created -> document date_issued ou resource rec_created_date ?
    if "dcterms:created" in tikadict:
        document["date_issued"] = tikadict["dcterms:created"]
    # xmpTPg:NPages -> document extent_pages
    if "xmpTPg:NPages" in tikadict:
        document["extent_pages"] = tikadict["xmpTPg:NPages"]

    # resource
    # dcterms:modified -> resource rec_modified_date ?
    if "dcterms:modified" in tikadict:
        resource["rec_modified_date"] = tikadict["dcterms:modified"]
    # producer -> resource processing_software_name
    if "producer" in tikadict:
        resource["processing_software_name"] = tikadict["producer"]
    # Content-Type -> resource format_mimetype
    if "Content-Type" in tikadict:
        resource["format_mimetype"] = tikadict["Content-Type"]
    
    document["resources"] = [resource]

    logging.debug(document)
    return document

