#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import re

from stdnum import ean
from stdnum import isan
from stdnum import isbn
from stdnum import ismn
from stdnum import issn

from biblib.services import resource_service


def validate_metajson_document(document):
    errors = []
    # common
    if "rec_type" not in document or not document["rec_type"]:
        errors.append("Empty type")
    if "title" not in document or not document["title"]:
        errors.append("Empty title")
    date = document.get_date()
    if date:
        errors.extend(validate_metajson_date(date))
    else:
        errors.append("Empty date_issued")
    if "creators" in document and document["creators"]:
        for creator in document["creators"]:
            errors.extend(validate_metajson_creator(creator))
    else:
        errors.append("No creator")
    if "identifiers" in document:
        for identifier in document["identifiers"]:
            errors.extend(validate_identifier(identifier))
    # related_items
    if "is_part_ofs" in document:
        for is_part_of in document["is_part_ofs"]:
            errors.extend(validate_metajson_is_part_of(is_part_of))
    if "series" in document:
        for series in document["series"]:
            errors.extend(validate_metajson_series(series))
    if "originals" in document:
        for original in document["originals"]:
            errors.extend(validate_metajson_original(original))
    if "review_ofs" in document:
        for review_ofs in document["review_ofs"]:
            errors.extend(validate_metajson_review_ofs(review_ofs))
    if "archives" in document:
        for archive in document["archives"]:
            errors.extend(validate_metajson_archive(archive))
    #if "resources" in document:
    #    for resource in document["resources"]:
    #        errors.extend(validate_metajson_resource(resource))

    return errors


def validate_metajson_is_part_of(is_part_of):
    errors = []
    if not is_part_of:
        errors.append("Empty is_part_of")
    if "rec_type" not in is_part_of or not is_part_of["rec_type"]:
        errors.append("Empty type in is_part_ofs")
    if "title" not in is_part_of or not is_part_of["title"]:
        errors.append("Empty title in is_part_of")
    if "creators" in is_part_of and is_part_of["creators"]:
        for creator in is_part_of["creators"]:
            errors.extend(validate_metajson_creator(creator))
    if "identifiers" in is_part_of:
        for identifier in is_part_of["identifiers"]:
            errors.extend(validate_identifier(identifier))
    if "is_part_ofs" in is_part_of:
        for is_part_of_is_part_of in is_part_of["is_part_ofs"]:
            errors.extend(validate_metajson_is_part_of(is_part_of_is_part_of))
    if "series" in is_part_of:
        for is_part_of_series in is_part_of["series"]:
            errors.extend(validate_metajson_series(is_part_of_series))
    return errors


def validate_metajson_original(original):
    errors = []
    if not original:
        errors.append("Empty original")
    if "rec_type" not in original or not original["rec_type"]:
        errors.append("Empty type in original")
    if "title" not in original or not original["title"]:
        errors.append("Empty title in original")
    if "creators" in original and original["creators"]:
        for creator in original["creators"]:
            errors.extend(validate_metajson_creator(creator))
    return errors


def validate_metajson_archive(archive):
    errors = []
    if not archive:
        errors.append("Empty archive")
    if "title" not in archive or not archive["title"]:
        errors.append("Empty title in archive")
    if "creators" in archive and archive["creators"]:
        for creator in archive["creators"]:
            errors.extend(validate_metajson_creator(creator))
    return errors


def validate_metajson_series(series):
    errors = []
    if not series:
        errors.append("Empty series")
    if "title" not in series or not series["title"]:
        errors.append("Empty title in series")
    if "creators" in series and series["creators"]:
        for creator in series["creators"]:
            errors.extend(validate_metajson_creator(creator))
    return errors


def validate_metajson_review_ofs(review_ofs):
    errors = []
    if not review_ofs:
        review_ofs.append("Empty review_ofs")
    if "rec_type" not in review_ofs or not review_ofs["rec_type"]:
        errors.append("Empty type in review_ofs")
    if "title" not in review_ofs or not review_ofs["title"]:
        errors.append("Empty title in review_ofs")
    if "creators" in review_ofs and review_ofs["creators"]:
        for creator in review_ofs["creators"]:
            errors.extend(validate_metajson_creator(creator))
    return errors


def validate_metajson_creator(creator):
    errors = []
    if "roles" not in creator or not creator["roles"]:
        errors.append("No role for creator")
    if "agent" in creator:
        if "rec_class" in creator["agent"]:
            if creator["agent"]["rec_class"] == "Person":
                if "name_family" not in creator["agent"] or not creator["agent"]["name_family"]:
                    errors.append("No name_family in creator Person")
            elif creator["agent"]["rec_class"] == "Orgunit":
                if "name" not in creator["agent"] or not creator["agent"]["name"]:
                    errors.append("No name in creator Orgunit")
            elif creator["agent"]["rec_class"] == "Event":
                if "title" not in creator["agent"] or not creator["agent"]["title"]:
                    errors.append("No title in creator Event")
            elif creator["agent"]["rec_class"] == "Family":
                if "name_family" not in creator["agent"] or not creator["agent"]["name_family"]:
                    errors.append("No name_family in creator Family")
            else:
                errors.append("Not a valid rec_class in creator : {}".format(creator["agent"]["rec_class"]))
        else:
            errors.append("No rec_class in creator")
    else:
        errors.append("No agent in creator")
    return errors


def validate_metajson_resource(resource):
    errors = []
    if "url" in resource:
        url_dict = resource_service.fetch_url(resource["url"])
        if url_dict["error"]:
            errors.append("Error {} with URL: {}".format(url_dict["code"], resource["url"]))
        elif "redirect" in url_dict:
            errors.append("Redirected URL: {}".format(url_dict["redirect_url"]))
    return errors


def validate_metajson_date(date):
    errors = []
    if date:
        date_regex = re.compile('^([\+-]?\d{4}(?!\d{2}\b))((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d|[12]\d{2}|3([0-5]\d|6[1-6])))([T\s]((([01]\d|2[0-3])((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?$')
        if not date_regex.match(date):
            errors.append("Maybe malformed date: {}".format(date))
    else:
        errors.append("Empty date")
    return errors


def validate_identifier(identifier):
    errors = []
    if identifier:
        if identifier["id_type"] == "issn":
            try:
                issn.validate(identifier["value"])
            except:
                errors.append("Invalid ISSN: {}".format(identifier["value"]))
        elif identifier["id_type"] == "isbn":
            try:
                isbn.validate(identifier["value"])
            except:
                errors.append("Invalid ISBN: {}".format(identifier["value"]))
        elif identifier["id_type"] == "isan":
            try:
                isan.validate(identifier["value"])
            except:
                errors.append("Invalid ISAN: {}".format(identifier["value"]))
        elif identifier["id_type"] == "ismn":
            try:
                ismn.validate(identifier["value"])
            except:
                errors.append("Invalid ISMN: {}".format(identifier["value"]))
        elif identifier["id_type"] == "ean":
            try:
                ean.validate(identifier["value"])
            except:
                errors.append("Invalid EAN: {}".format(identifier["value"]))
    return errors
