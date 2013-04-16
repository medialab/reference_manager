#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from metadatas import metajson
from metadatas import metajson_contrib_util

def cite(document, format):

    is_part_of = None
    is_part_of_is_part_of = None
    if "is_part_of" in document and len(document["is_part_of"]) > 0:
        is_part_of = document["is_part_of"][0]
        if "is_part_of" in is_part_of and len(is_part_of["is_part_of"]) > 0:
            is_part_of_is_part_of = is_part_of["is_part_of"][0]

    result = ""

    # contributors
    contributors = format_contributors_of_document(document, 0)
    if contributors:
        result += contributors

    # title
    title = format_title_of_document(document)
    if title:
        result += title

    # is_part_of
    if is_part_of:
        
        # is_part_of_title
        is_part_of_title = format_title_of_document(is_part_of)
        if is_part_of_title:
            result += is_part_of_title

        # is_part_of_contributors
        is_part_of_contributors = format_contributors_of_document(is_part_of, 1)
        if is_part_of_contributors:
            result += is_part_of_contributors

        # is_part_of_is_part_of
        if is_part_of_is_part_of:

            # is_part_of_is_part_of_title
            is_part_of_is_part_of_title = format_title_of_document(is_part_of_is_part_of)
            if is_part_of_is_part_of_title:
                result += is_part_of_is_part_of_title

            # is_part_of_is_part_of_contributors
            is_part_of_is_part_of_contributors = format_contributors_of_document(is_part_of_is_part_of, 2)
            if is_part_of_is_part_of_contributors:
                result += is_part_of_is_part_of_contributors

    # Others contributors
    # Trans. (translated by) trl
    # Dir. (directed by) drt
    # Writ. (written by). sce
    # Prod. (produced by) pro
    # Narr. (narrated by) nrt
    # Perf. (performers) act
    # Ed. (edited by) edt
    # aut
    # dgg
    # cph
    contrib_dict = get_contributors_dict_of_document(document)

    # edition
    edition = document.get_edition()
    if edition:
        result += edition + " ed. "

    # extent_volumes
    extent_volumes = document.get_extent_volumes()
    if extent_volumes:
        result += extent_volumes + ". "

    # degree
    # todo

    # publisher_place
    publisher_place = document.get_publisher_place()
    if publisher_place:
        result += publisher_place + ": "

    # publisher
    publisher = document.get_publisher()
    if publisher:
        result += publisher + ", "
    else:
        pass
        # todo dgg

    # part_volume, part_issue
    part_volume = document.get_part_volume()
    if part_volume:
        result += part_volume + "."
    
    part_issue = document.get_part_issue()
    if part_issue:
        result += part_issue
    
    if part_volume or part_issue:
        result += " "

    # date
    date = document.get_date()
    if date:
        result += date + ". "

    # part_page_start & part_page_end
    part_page_start = document.get_part_page_start()
    if part_page_start:
        result += part_page_start

    part_page_end = document.get_part_page_end()
    if part_page_end:
        result += "-" + part_page_end

    if part_page_end or part_page_end:
        result += ". "

    # medium of publication, date_last_accessed, remote_url
    medium_of_publication = None
    date_last_accessed = None
    remote_url = None
    if "medium" in document:
        medium_of_publication = document["medium"]

    if not medium_of_publication and "rec_type_description" in document:
        medium_of_publication = document["rec_type_description"]

    if "resources" in document and len(document["resources"]) > 0:
        if "remote_url" in document["resources"][0]:
            remote_url = document["resources"][0]["remote_url"]
        if not medium_of_publication and remote_url:
            medium_of_publication = "Web"
        if "date_last_accessed" in document["resources"][0]:
            date_last_accessed = format_date_last_accessed(document["resources"][0]["date_last_accessed"])
    if medium_of_publication:
        result += medium_of_publication + ". "
    if date_last_accessed:
        result += date_last_accessed + ". "
    if remote_url:
        result += format_url(remote_url)

    print result
    return result


def remove_last_point(text):
    if text:
        if text.endswith("."):
            return text[:-1]
        else:
            return text


def format_date_last_accessed(date):
    if date:
        result = date
        return result


def format_url(url):
    if url:
        return "&lt;<a href=\"" + url + "\" target=\"_blank\">" + url + "</a>&gt;"


def format_title_of_document(document):
    if document and "title" in document:
        result = remove_last_point(document["title"])
        if "title_sub" in document:
            result += ": " + remove_last_point(document["title_sub"])
        if "is_part_of" in document:
            return "\"" + result + ".\" "
        else:
            return "<i>" + result + "</i>. "


def get_contributors_dict_of_document(document):
    if "contributors" in document:
        result = {}
        # "aut", "act", "cph", "dgg", "edt", "pro", "trl"
        for contributor in document["contributors"]:
            if "role" in contributor:
                try :
                    result[contributor["role"]].append(contributor)
                except :
                    result[contributor["role"]] = [contributor]
            else:
                try :
                    result["ctb"].append(contributor)
                except :
                    result["ctb"] = [contributor]
        return result


def format_contributors_of_document(document, level):
    if "contributors" in document:
        result = ""
        contri_count = len(document["contributors"])
        has_edt = False
        for position, contributor in enumerate(document["contributors"]):
            if contributor["role"] in ["aut", "edt"]:
                if contributor["role"] == "edt":
                    has_edt = True
                if 0 < position < contri_count - 1:
                    result += ", "
                elif position == contri_count - 1 and contri_count > 1:
                    result += ", and "
                result += format_contributor(contributor, position)

                if contri_count > 3:
                    result += ", et al"
                    break
        if level == 0:
            if has_edt:
                return result + ", eds. "
            else:
                return result + ". "
        else:
            if has_edt:
                return "Ed. " + result + ". "
            else:
                return result + ". "


def format_contributor(contributor, position):
    style = metajson.STYLE_FAMILY_COMMA_GIVEN
    if position > 0:
        style = metajson.STYLE_GIVEN_FAMILY
    return contributor.formatted_name(style)

