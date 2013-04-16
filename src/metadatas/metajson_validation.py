#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import re
from util import resource_util

def validate_metajson_document(metajson):
    errors=[]
    # common
    if "rec_type" not in metajson or not metajson["rec_type"]:
        errors.append("Empty type")
    if "title" not in metajson or not metajson["title"]:
        errors.append("Empty title")
    date = metajson.get_date()
    if date :
        errors.extend(validate_metajson_date(date))
    else :
        errors.append("Empty date_issued")
    if "contributors" in metajson and metajson["contributors"]:
        for contributor in metajson["contributors"]:
            errors.extend(validate_metajson_contributor(contributor))
    else :
        errors.append("No contributor")

    # related_items
    if "is_part_of" in metajson :
        for is_part_of in metajson["is_part_of"] :
            errors.extend(validate_metajson_is_part_of(is_part_of))
    if "series" in metajson :
        for series in metajson["series"] :
            errors.extend(validate_metajson_series(series))
    if "original" in metajson :
        for original in metajson["original"] :
            errors.extend(validate_metajson_original(original))
    if "review_of" in metajson :
        for review_of in metajson["review_of"] :
            errors.extend(validate_metajson_review_of(review_of))
    if "archive" in metajson :
        for archive in metajson["archive"] :
            errors.extend(validate_metajson_archive(archive))
    #if "resources" in metajson :
    #    for resource in metajson["resources"] :
    #        errors.extend(validate_metajson_resource(resource))
    
    return errors

def validate_metajson_is_part_of(is_part_of):
    errors=[]
    if not is_part_of :
        errors.append("Empty is_part_of")
    if "rec_type" not in is_part_of or not is_part_of["rec_type"] :
        errors.append("Empty type in is_part_of")
    if "title" not in is_part_of or not is_part_of["title"] :
        errors.append("Empty title in is_part_of")
    if "contributors" in is_part_of and is_part_of["contributors"] :
        for contributor in is_part_of["contributors"] :
            errors.extend(validate_metajson_contributor(contributor))
    if "is_part_of" in is_part_of :
        for is_part_of_is_part_of in is_part_of["is_part_of"] :
            errors.extend(validate_metajson_is_part_of(is_part_of_is_part_of))
    if "series" in is_part_of :
        for is_part_of_series in is_part_of["series"] :
            errors.extend(validate_metajson_series(is_part_of_series))
    return errors

def validate_metajson_original(original):
    errors=[]
    if not original:
        errors.append("Empty original")
    if "rec_type" not in original or not original["rec_type"]:
        errors.append("Empty type in original")
    if "title" not in original or not original["title"]:
        errors.append("Empty title in original")
    if "contributors" in original and original["contributors"]:
        for contributor in original["contributors"]:
            errors.extend(validate_metajson_contributor(contributor))
    return errors

def validate_metajson_archive(archive):
    errors=[]
    if not archive:
        errors.append("Empty archive")
    if "title" not in archive or not archive["title"]:
        errors.append("Empty title in archive")
    if "contributors" in archive and archive["contributors"]:
        for contributor in archive["contributors"]:
            errors.extend(validate_metajson_contributor(contributor))
    return errors

def validate_metajson_series(series):
    errors=[]
    if not series:
        errors.append("Empty series")
    if "title" not in series or not series["title"]:
        errors.append("Empty title in series")
    if "contributors" in series and series["contributors"]:
        for contributor in series["contributors"]:
            errors.extend(validate_metajson_contributor(contributor))
    return errors

def validate_metajson_review_of(review_of):
    errors=[]
    if not review_of:
        review_of.append("Empty review_of")
    if "rec_type" not in review_of or not review_of["rec_type"]:
        errors.append("Empty type in review_of")
    if "title" not in review_of or not review_of["title"]:
        errors.append("Empty title in review_of")
    if "contributors" in review_of and review_of["contributors"]:
        for contributor in review_of["contributors"]:
            errors.extend(validate_metajson_contributor(contributor))
    return errors

def validate_metajson_contributor(contributor):
    errors=[]
    if "role" not in contributor or not contributor["role"]:
        errors.append("No role for contributor")
    if "person" in contributor:
        if "name_family" not in contributor["person"] or not contributor["person"]["name_family"]:
            errors.append("No name_family in contributor person")
    elif "orgunit" in contributor:
        if "name" not in contributor["orgunit"] or not contributor["orgunit"]["name"]:
            errors.append("No name in contributor orgunit")
    elif "event" in contributor:
        if "title" not in contributor["event"] or not contributor["event"]["title"]:
            errors.append("No title in contributor event")
    elif "family" in contributor:
        if "name_family" not in contributor["family"] or not contributor["family"]["name_family"]:
            errors.append("No name_family in contributor family")
    else:
        errors.append("No entity in contributor")
    return errors

def validate_metajson_resource(resource):
    errors=[]
    if "remote_url" in resource:
        url_dict = resource_util.verify_url(resource["remote_url"])
        if url_dict["error"]:
            errors.append("Error {} with URL: {}".format(url_dict["code"], resource["remote_url"]))
        elif "redirect" in url_dict:
            errors.append("Redirected URL: {}".format(url_dict["redirect_url"]))
    return errors

def validate_metajson_date(date):
    errors=[]
    if date :
        date_regex = re.compile('^([\+-]?\d{4}(?!\d{2}\b))((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d|[12]\d{2}|3([0-5]\d|6[1-6])))([T\s]((([01]\d|2[0-3])((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?$')
        if not date_regex.match(date):
            errors.append("Maybe malformed date: "+date)
    else :
        errors.append("Empty date")
    return errors
