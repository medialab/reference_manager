#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from bson import json_util

from biblib.metajson import Common
from biblib.metajson import Collection
from biblib.metajson import Field
from biblib.metajson import Document
from biblib.metajson import DocumentUi
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Resource
from biblib.metajson import Target
from biblib.metajson import Type
from biblib.services import config_service

metajson_title_non_sort = config_service.metajson_title_non_sort


def load_dict(meta_dict):
    if "rec_class" not in meta_dict:
        return Common(meta_dict)
    elif meta_dict["rec_class"] == "Document":
        return Document(meta_dict)
    elif meta_dict["rec_class"] == "DocumentUi":
        return DocumentUi(meta_dict)
    elif meta_dict["rec_class"] == "Person":
        return Person(meta_dict)
    elif meta_dict["rec_class"] == "Orgunit":
        return Orgunit(meta_dict)
    elif meta_dict["rec_class"] == "Event":
        return Event(meta_dict)
    elif meta_dict["rec_class"] == "Family":
        return Family(meta_dict)
    elif meta_dict["rec_class"] == "Field":
        return Field(meta_dict)
    elif meta_dict["rec_class"] == "Resource":
        return Resource(meta_dict)
    elif meta_dict["rec_class"] == "Target":
        return Target(meta_dict)
    elif meta_dict["rec_class"] == "Type":
        return Type(meta_dict)
    elif meta_dict["rec_class"] == "Collection":
        return Collection(meta_dict)
    else:
        print "Unknown rec_class: {O}".format(meta_dict["rec_class"])
        return Common(meta_dict)


def load_dict_list(meta_dict_list):
    metajson_list = []
    for meta_dict in meta_dict_list:
        metajson_list.append(load_dict(meta_dict))
    return metajson_list


def print_metajson(metajson):
    # todo
    source, rec_id, rec_type, title, is_part_of_type, is_part_of_is_part_of_type = None
    print "# {}\t:\t{}\t:\t{}\t->\titem: {} {}".format(source, rec_id, rec_type, is_part_of_type, is_part_of_is_part_of_type, title)


def dump_metajson(metajson):
    if metajson:
        return json_util.dumps(metajson, ensure_ascii=False, indent=4, encoding="utf-8", sort_keys=True)


def enhance_metajson(metajson):
    # title_non_sort
    manage_title_non_sort(metajson)


def manage_title_non_sort(metajson):
    #print("manage_title_non_sort")
    if metajson and "title_non_sort" not in metajson and "title" in metajson:
        title = metajson["title"]
        language = None
        if "languages" in metajson:
            language = metajson["languages"][0]
            print("language: {}".format(language))
            if language and language in metajson_title_non_sort:
                non_sorts = metajson_title_non_sort[language]
                title_words = title.split()
                if len(title_words) > 1:
                    first_title_word = title_words[0]
                    if first_title_word in non_sorts:
                        title_non_sort = first_title_word
                        title = " ".join(title_words[1:])
                        print("title_non_sort: '{}'".format(title_non_sort))
                        print("title: '{}'".format(title))
                        metajson["title_non_sort"] = title_non_sort
                        metajson["title"] = title
