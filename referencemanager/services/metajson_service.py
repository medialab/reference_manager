#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from referencemanager.metajson import Common
from referencemanager.metajson import Collection
from referencemanager.metajson import Datafield
from referencemanager.metajson import Document
from referencemanager.metajson import DocumentUi
from referencemanager.metajson import Event
from referencemanager.metajson import Family
from referencemanager.metajson import Orgunit
from referencemanager.metajson import Person
from referencemanager.metajson import Resource
from referencemanager.metajson import Target
from referencemanager.metajson import Type


def load_dict(meta_dict):
    if "metajson_class" not in meta_dict:
        return Common(meta_dict)
    elif meta_dict["metajson_class"] == "Document":
        return Document(meta_dict)
    elif meta_dict["metajson_class"] == "DocumentUi":
        return DocumentUi(meta_dict)
    elif meta_dict["metajson_class"] == "Person":
        return Person(meta_dict)
    elif meta_dict["metajson_class"] == "Orgunit":
        return Orgunit(meta_dict)
    elif meta_dict["metajson_class"] == "Event":
        return Event(meta_dict)
    elif meta_dict["metajson_class"] == "Family":
        return Family(meta_dict)
    elif meta_dict["metajson_class"] == "Datafield":
        return Datafield(meta_dict)
    elif meta_dict["metajson_class"] == "Resource":
        return Resource(meta_dict)
    elif meta_dict["metajson_class"] == "Target":
        return Target(meta_dict)
    elif meta_dict["metajson_class"] == "Type":
        return Type(meta_dict)
    elif meta_dict["metajson_class"] == "Collection":
        return Collection(meta_dict)
    else:
        print "Unknown metajson_class: {O}".format(meta_dict["metajson_class"])
        return Common(meta_dict)


def load_dict_list(meta_dict_list):
    metajson_list = []
    for meta_dict in meta_dict_list:
        metajson_list.append(load_dict(meta_dict))
    return metajson_list
