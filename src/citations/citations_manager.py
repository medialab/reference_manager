#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from crosswalks import metajson_to_openurl
from citations import mla_style

def cite(metajson_document, style, format):
  if format == "html":
    result = metajson_to_openurl.convert_metajson_document_to_openurl_coins(metajson_document)

  if style == "mla":
    result += mla_style.cite(metajson_document, format)
  return result

