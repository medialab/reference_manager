#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib import metajson


def cite(document, format):

    is_part_of = None
    is_part_of_is_part_of = None
    if "is_part_ofs" in document and len(document["is_part_ofs"]) > 0:
        is_part_of = document["is_part_ofs"][0]
        if "is_part_ofs" in is_part_of and len(is_part_of["is_part_ofs"]) > 0:
            is_part_of_is_part_of = is_part_of["is_part_ofs"][0]

    result = ""

    # creators
    creators = format_creators_of_document(document, 0)
    if creators:
        result += creators

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

        # is_part_of_creators
        is_part_of_creators = format_creators_of_document(is_part_of, 1)
        if is_part_of_creators:
            result += is_part_of_creators

        # is_part_of_is_part_of
        if is_part_of_is_part_of:

            # is_part_of_is_part_of_title
            is_part_of_is_part_of_title = format_title_of_document(is_part_of_is_part_of)
            if is_part_of_is_part_of_title:
                result += is_part_of_is_part_of_title

            # is_part_of_is_part_of_creators
            is_part_of_is_part_of_creators = format_creators_of_document(is_part_of_is_part_of, 2)
            if is_part_of_is_part_of_creators:
                result += is_part_of_is_part_of_creators


    # Others creators
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
    contrib_dict = get_creators_dict_of_document(document)

    # edition
    edition = document.get_edition()
    if edition:
        result += u"<span class=\"edition\">{0}</span> ".format(edition + " ed.")

    # extent_volumes
    extent_volumes = document.get_extent_volumes()
    if extent_volumes:
        result += u"<span class=\"extent_volumes\">{0}</span>. ".format(extent_volumes)

    # degree
    # todo

    # publication_places
    publication_places = document.get_publication_places()
    if publication_places:
        result += u"<span class=\"publication_places\">{0}</span>: ".format(publication_places[0])

    # publishers
    publishers = document.get_publishers()
    if publishers:
        result += u"<span class=\"publishers\">{0}</span>, ".format(publishers[0])

    else:
        pass
        # todo creator dgg

    # part_volume, part_issue
    part_volume = document.get_part_volume()
    if part_volume:
        result += u"<span class=\"part_volume\">{0}</span>.".format(part_volume)

    part_issue = document.get_part_issue()
    if part_issue:
        result += u"<span class=\"part_issue\">{0}</span>".format(part_issue)

    if part_volume or part_issue:
        result += " "

    # date
    date = document.get_date()
    print date
    if date:
        result += u"<span class=\"date\">{0}</span>. ".format(date)

    # part_page_start & part_page_end
    part_page_start = document.get_part_page_start()
    if part_page_start:
        result += u"<span class=\"part_page_start\">{0}</span>".format(part_page_start)

    part_page_end = document.get_part_page_end()
    if part_page_end:
        result += u"-<span class=\"part_page_end\">{0}</span>".format(part_page_end)

    if part_page_end or part_page_end:
        result += ". "

    # medium of publication, date_last_accessed, url
    medium_of_publication = None
    date_last_accessed = None
    url = None
    if "medium" in document:
        medium_of_publication = document["medium"]

    if not medium_of_publication and "rec_type_description" in document:
        medium_of_publication = document["rec_type_description"]

    if "resources" in document and len(document["resources"]) > 0:
        if "url" in document["resources"][0]:
            url = document["resources"][0]["url"]
        if not medium_of_publication and url:
            medium_of_publication = "Web"
        if "date_last_accessed" in document["resources"][0]:
            date_last_accessed = format_date_last_accessed(document["resources"][0]["date_last_accessed"])
    if medium_of_publication:
        result += u"<span class=\"medium_of_publication\">{0}</span>. ".format(medium_of_publication)

    if date_last_accessed:
        result += u"<span class=\"date_last_accessed\">{0}</span>. ".format(date_last_accessed)

    if url:
        result += u"<span class=\"url\">{0}</span>".format(format_url(url))

    #print result 
    #this print fires an encoding error when result contains non ascii characters
    #if print is needed :
    #   1- use python log command not print
    #   2- for encoding a result.ecnode("utf8") might solve the prb    
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
        return u"&lt;<a href=\"{0}\" target=\"_blank\">{0}</a>&gt;".format(url)


def format_title_of_document(document):
    if document and "title" in document:
        result = u""
        if "title_non_sort" in document:
            result += document["title_non_sort"]
        result += remove_last_point(document["title"])
        if "title_sub" in document:
            result += u": " + remove_last_point(document["title_sub"])
        if "is_part_ofs" in document:
            return u"\"<span class=\"title\">{0}</span>.\" ".format(result)
        else:
            return u"<span class=\"title\">{0}</span>. ".format(result)


def get_creators_dict_of_document(document):
    if "creators" in document:
        result = {}
        # "aut", "act", "cph", "dgg", "edt", "pro", "trl"
        for creator in document["creators"]:
            if "role" in creator:
                try:
                    result[creator["role"]].append(creator)
                except:
                    result[creator["role"]] = [creator]
            else:
                try:
                    result["ctb"].append(creator)
                except:
                    result["ctb"] = [creator]
        return result


def format_creators_of_document(document, level):
    if "creators" in document:
        result = ""
        contri_count = len(document["creators"])
        has_edt = False
        for position, creator in enumerate(document["creators"]):
            if creator["role"] in ["aut", "edt"]:
                if creator["role"] == "edt":
                    has_edt = True
                if 0 < position < contri_count - 1:
                    result += ", "
                elif position == contri_count - 1 and contri_count > 1:
                    result += ", and "
                result += format_creator(creator, position)

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


def format_creator(creator, position):
    style = metajson.STYLE_FAMILY_COMMA_GIVEN
    if position > 0:
        style = metajson.STYLE_GIVEN_FAMILY
    formatted_name = creator.formatted_name(style)
    if formatted_name:
        return u"<span class=\"creator\">{0}</span>".format(formatted_name)
