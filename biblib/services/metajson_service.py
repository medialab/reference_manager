#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import types

from biblib import metajson
from biblib.metajson import Common
from biblib.metajson import Collection
from biblib.metajson import Field
from biblib.metajson import Document
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Identifier
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Resource
from biblib.metajson import Target
from biblib.metajson import Type


def load_dict(meta_dict):
    if "rec_class" not in meta_dict:
        return Common(meta_dict)
    elif meta_dict["rec_class"] == "Document":
        return Document(meta_dict)
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


def move_keys_between_dicts(keys, dict_a, dict_b):
    if dict_a and dict_b:
        for key in keys:
            if key in dict_a:
                dict_b[key] = dict_a[key]
                del dict_a[key]


def copy_keys_between_dicts(keys, dict_a, dict_b):
    if dict_a and dict_b:
        for key in keys:
            if key in dict_a:
                dict_b[key] = dict_a[key]


def pretty_print_document(document):
    print "# rec_source: {}".format(document.get_rec_source())
    print "# rec_type: {}\trec_id: {}\ttitle: {}".format(document.get_rec_type(), document.get_rec_id(), document.get_title())
    is_part_of = document.get_is_part_of()
    if is_part_of:
        print "# is_part_ofs[0].rec_type: {}\tis_part_ofs[0].rec_id: {}\tis_part_ofs[0].title: {}".format(is_part_of.get_rec_type(), is_part_of.get_rec_id(), is_part_of.get_title())
        is_part_of_is_part_of = is_part_of.get_is_part_of()
        if is_part_of_is_part_of:
            print "# is_part_ofs[0].is_part_ofs[0].rec_type: {}\tis_part_ofs[0].is_part_ofs[0].rec_id: {}\tis_part_ofs[0].is_part_ofs[0].title: {}".format(is_part_of_is_part_of.get_rec_type(), is_part_of_is_part_of.get_rec_id(), is_part_of_is_part_of.get_title())
            is_part_of_is_part_of_is_part_of = is_part_of_is_part_of.get_is_part_of()
            if is_part_of_is_part_of_is_part_of:
                print "# is_part_ofs[0].is_part_ofs[0].is_part_ofs[0].rec_type: {}\tis_part_ofs[0].is_part_ofs[0].is_part_ofs[0].rec_id: {}\tis_part_ofs[0].is_part_ofs[0].is_part_ofs[0].title: {}".format(is_part_of_is_part_of_is_part_of.get_rec_type(), is_part_of_is_part_of_is_part_of.get_rec_id(), is_part_of_is_part_of_is_part_of.get_title())


def enhance_metajson(metajson):
    # title_non_sort
    manage_title_non_sort(metajson)
    return metajson


def manage_title_non_sort(metajson):
    #print("manage_title_non_sort")
    if metajson and "title_non_sort" not in metajson and "title" in metajson:
        title = metajson["title"]
        language = None
        if "languages" in metajson:
            language = metajson["languages"][0]
            print("language: {}".format(language))
            if language and language in metajson.TITLE_NON_SORT:
                non_sorts = metajson.TITLE_NON_SORT[language]
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


def create_collection(col_id, col_title, metajson_list):
    if metajson_list:
        collection = Collection()
        if col_id:
            collection["col_id"] = col_id
        if col_title:
            collection["title"] = col_title
        if isinstance(metajson_list, types.GeneratorType):
            collection["records"] = list(metajson_list)
        else:
            collection["records"] = metajson_list
        return collection


def create_identifier(id_type, id_value):
    if id_value:
        identifier = Identifier()
        identifier["value"] = id_value
        if id_type:
            identifier["id_type"] = id_type
        return identifier
