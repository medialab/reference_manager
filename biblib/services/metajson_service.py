#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import types
import uuid
from datetime import datetime, date, time

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
from biblib.util import constants


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


def enhance_metajson(document):
    # rec_id
    if "rec_id" not in document or document["rec_id"] is None:
        document["rec_id"] = str(uuid.uuid1())
    # title_non_sort
    manage_title_non_sort(document)
    # rec_status
    if "rec_status" not in document or document["rec_status"] is None:
        document["rec_status"] = constants.REC_STATUS_PRIVATE
    # rec_created_date
    if "rec_created_date" not in document or document["rec_created_date"] is None:
        document["rec_created_date"] = datetime.now().isoformat()
    # rec_modified_date
        document["rec_modified_date"] = datetime.now().isoformat()
    # rec_deleted_date
        if document["rec_status"] == constants.REC_STATUS_DELETED and "rec_deleted_date" not in metajson:
            document["rec_deleted_date"] = datetime.now().isoformat()
    return document


def manage_title_non_sort(document):
    #print("manage_title_non_sort")
    if document and "title_non_sort" not in document and "title" in document:
        title = document["title"]
        language = None
        if "languages" in document:
            language = document["languages"][0]
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
                        document["title_non_sort"] = title_non_sort
                        document["title"] = title


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


def create_address(street, post_code, locality_city_town, country, preferred, relation_type, visible):
    address = {}
    if street is not None:    
        address["street"] = street
    if post_code is not None:
        address["post_code"] = post_code
    if locality_city_town is not None:
        address["locality_city_town"] = locality_city_town
    if country is not None:
        address["country"] = country
    if preferred is not None:
        address["preferred"] = preferred
    if relation_type is not None:
        address["relation_type"] = relation_type
    if visible is not None:
        address["visible"] = visible
    return address


def create_email(value, preferred, relation_type, visible):
    if value is not None:
        email = {}
        email["value"] = value
        if preferred is not None:
            email["preferred"] = preferred
        if relation_type is not None:
            email["relation_type"] = relation_type
        if visible is not None:
            email["visible"] = visible
        return email


def create_identifier(id_type, id_value):
    if id_value:
        identifier = Identifier()
        identifier["value"] = id_value
        if id_type:
            identifier["id_type"] = id_type
        return identifier


def create_image_url(url):
    if url:
        image_url = {}
        image_url["value"] = url
        return image_url


def create_instant_message(value, service, preferred, relation_type, visible):
    if value is not None:
        im = {}
        im["value"] = value
        if service is not None:
            im["service"] = service
        if preferred is not None:
            im["preferred"] = preferred
        if relation_type is not None:
            im["relation_type"] = relation_type
        if visible is not None:
            im["visible"] = visible
        return im


def create_language_capability(language, mother_tong, oral_input, oral_output, text_input, text_output):
    if language is not None:
        lc = {}
        lc["language"] = language
        if mother_tong is not None:
            lc["mother_tong"] = mother_tong
        if oral_input is not None:
            lc["oral_input"] = oral_input
        if oral_output is not None:
            lc["oral_output"] = oral_output
        if text_input is not None:
            lc["text_input"] = text_input
        if text_output is not None:
            lc["text_output"] = text_output
        return lc


def create_phone(formatted, phone_type, preferred, relation_type, visible):
    if formatted is not None:
        phone = {}
        phone["formatted"] = formatted
        if phone_type is not None:
            phone["phone_type"] = phone_type
        if preferred is not None:
            phone["preferred"] = preferred
        if relation_type is not None:
            phone["relation_type"] = relation_type
        if visible is not None:
            phone["visible"] = visible
        return phone


def create_uri(value, preferred, relation_type, visible):
    if value is not None:
        uri = {}
        uri["value"] = value
        if preferred is not None:
            uri["preferred"] = preferred
        if relation_type is not None:
            uri["relation_type"] = relation_type
        if visible is not None:
            uri["visible"] = visible
        return uri
