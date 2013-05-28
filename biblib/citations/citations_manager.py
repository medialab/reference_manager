#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.crosswalks import openurl_crosswalk
from biblib.citations import mla_style


def cite(metajson_document, style, format):
    if format == "html":
        result = openurl_crosswalk.metajson_to_openurlcoins(metajson_document)

    if style == "mla":
        result += mla_style.cite(metajson_document, format)
    return result
