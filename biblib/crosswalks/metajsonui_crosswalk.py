#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Document
from biblib.metajson import DocumentUi


def metajsonui_to_metajson_list(metajsonui, source, only_first_record):
    yield metajsonui_to_metajson(metajsonui, source)


def metajsonui_to_metajson(metajsonui, source):
    # todo
    return Document(metajsonui)


def metajson_to_metajsonui(metajson, source):
    # todo
    return DocumentUi(metajson)
