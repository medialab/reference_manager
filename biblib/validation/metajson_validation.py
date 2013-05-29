#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import re
from biblib.services import resource_service


def validate_metajson_document(metajson):
    errors = []
    # common
    if "rec_type" not in metajson or not metajson["rec_type"]:
        errors.append("Empty type")
    if "title" not in metajson or not metajson["title"]:
        errors.append("Empty title")
    date = metajson.get_date()
    if date:
        errors.extend(validate_metajson_date(date))
    else:
        errors.append("Empty date_issued")
    if "creators" in metajson and metajson["creators"]:
        for creator in metajson["creators"]:
            errors.extend(validate_metajson_creator(creator))
    else:
        errors.append("No creator")

    # related_items
    if "is_part_of" in metajson:
        for is_part_of in metajson["is_part_of"]:
            errors.extend(validate_metajson_is_part_of(is_part_of))
    if "series" in metajson:
        for series in metajson["series"]:
            errors.extend(validate_metajson_series(series))
    if "original" in metajson:
        for original in metajson["original"]:
            errors.extend(validate_metajson_original(original))
    if "review_of" in metajson:
        for review_of in metajson["review_of"]:
            errors.extend(validate_metajson_review_of(review_of))
    if "archive" in metajson:
        for archive in metajson["archive"]:
            errors.extend(validate_metajson_archive(archive))
    #if "resources" in metajson:
    #    for resource in metajson["resources"]:
    #        errors.extend(validate_metajson_resource(resource))

    return errors


def validate_metajson_is_part_of(is_part_of):
    errors = []
    if not is_part_of:
        errors.append("Empty is_part_of")
    if "rec_type" not in is_part_of or not is_part_of["rec_type"]:
        errors.append("Empty type in is_part_of")
    if "title" not in is_part_of or not is_part_of["title"]:
        errors.append("Empty title in is_part_of")
    if "creators" in is_part_of and is_part_of["creators"]:
        for creator in is_part_of["creators"]:
            errors.extend(validate_metajson_creator(creator))
    if "is_part_of" in is_part_of:
        for is_part_of_is_part_of in is_part_of["is_part_of"]:
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


def validate_metajson_review_of(review_of):
    errors = []
    if not review_of:
        review_of.append("Empty review_of")
    if "rec_type" not in review_of or not review_of["rec_type"]:
        errors.append("Empty type in review_of")
    if "title" not in review_of or not review_of["title"]:
        errors.append("Empty title in review_of")
    if "creators" in review_of and review_of["creators"]:
        for creator in review_of["creators"]:
            errors.extend(validate_metajson_creator(creator))
    return errors


def validate_metajson_creator(creator):
    errors = []
    if "role" not in creator or not creator["role"]:
        errors.append("No role for creator")
    if "person" in creator:
        if "name_family" not in creator["person"] or not creator["person"]["name_family"]:
            errors.append("No name_family in creator person")
    elif "orgunit" in creator:
        if "name" not in creator["orgunit"] or not creator["orgunit"]["name"]:
            errors.append("No name in creator orgunit")
    elif "event" in creator:
        if "title" not in creator["event"] or not creator["event"]["title"]:
            errors.append("No title in creator event")
    elif "family" in creator:
        if "name_family" not in creator["family"] or not creator["family"]["name_family"]:
            errors.append("No name_family in creator family")
    else:
        errors.append("No entity in creator")
    return errors


def validate_metajson_resource(resource):
    errors = []
    if "remote_url" in resource:
        url_dict = resource_service.fetch_url(resource["remote_url"])
        if url_dict["error"]:
            errors.append("Error {} with URL: {}".format(url_dict["code"], resource["remote_url"]))
        elif "redirect" in url_dict:
            errors.append("Redirected URL: {}".format(url_dict["redirect_url"]))
    return errors


def validate_metajson_date(date):
    errors = []
    if date:
        date_regex = re.compile('^([\+-]?\d{4}(?!\d{2}\b))((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d|[12]\d{2}|3([0-5]\d|6[1-6])))([T\s]((([01]\d|2[0-3])((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?$')
        if not date_regex.match(date):
            errors.append("Maybe malformed date: "+date)
    else:
        errors.append("Empty date")
    return errors
