#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.crosswalks import openurl_crosswalk
from biblib.citations import mla_style
from biblib.services import config_service
from biblib.util import constants


default_citations_formats = config_service.config["citations"]["formats"]
default_citations_styles = config_service.config["citations"]["styles"]


def cite(metajson_document, style, format):
    if format == "html":
        result = openurl_crosswalk.metajson_to_openurlcoins(metajson_document)
    else:
        result=["",""]

    if style == constants.STYLE_MLA:
        result = result[1] + mla_style.cite(metajson_document, format)
    return result


def add_citations_to_metadata(metajson_document, styles, formats):
    if not styles:
        styles = default_citations_styles
    if not formats:
        formats = default_citations_formats
    if metajson_document:
        citations = {}
        for format in formats:
            if format:
                citations[format] = {}
                for style in styles:
                    if style:
                        citations[format][style] = cite(metajson_document, style, format)
        if citations:
            metajson_document["citations"] = citations
    return metajson_document
