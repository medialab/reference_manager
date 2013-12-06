#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib import metajson
from biblib.services import date_service
from biblib.util import constants

role_to_short_forms = {
    "act": ["perf.", "Perf."],
    "aut": ["", ""],
    "com": ["comp.", "Comp."],
    "cph": ["", ""],
    "ctb": ["", ""],
    "dgg": ["", ""],
    "drt": ["dir.", "Dir."],
    "dst": ["", ""],
    "edt": ["ed.", "Ed."],
    "nrt": ["narr.", "Narr."],
    "pbd": ["ed.", "Ed."],
    "pbl": ["", ""],
    "pro": ["prod.", "Prod."],
    "sce": ["writ.", "Writ."],
    "trl": ["trans.", "Trans."]
}

thesis_rec_type_to_degree = {
    "Dissertation": "Diss.",
    "BachelorThesis": "BA thesis",
    "StudentThesis": "BA thesis",
    "MasterThesis": "MA thesis",
    "DoctoralThesis": "PhD thesis",
    "ProfessoralThesis": "Prof. thesis"
}

# Tape Recording: Cassette, VHS, DVD, Videocassette, Filmstrip

def cite(document, format):
    result = ""

    if "rec_type" in document:
        rec_type = document["rec_type"]
    else:
        rec_type = "Document"

    # Book:
    # Lastname, Firstname. Title of Book. Place of Publication: Publisher, Year of Publication. Medium of Publication.

    # Components for artwork cited from a book: 
    # 1) Name of artist. 2) Underline title of artwork.
    # 3) Date artwork created (if date is uncertain use [c. 1503] meaning [circa 1503] or around the year 1503).
    # 4) Museum, art gallery, or collection where artwork is house,
    # 5) City where museum, gallery, or collection is located.
    # 6) Title of book used. 7) Author or editor of book.
    # 8) Place of publication: 9) Publisher, 10) Date of publication.
    # 11) Other relevant information, e.g. figure, page, plate, or slide number.

    # is_part_of, is_part_of_is_part_of 
    is_part_of = None
    is_part_of_is_part_of = None
    if "is_part_ofs" in document and len(document["is_part_ofs"]) > 0:
        is_part_of = document["is_part_ofs"][0]
        if "is_part_ofs" in is_part_of and len(is_part_of["is_part_ofs"]) > 0:
            is_part_of_is_part_of = is_part_of["is_part_ofs"][0]

    # extract the different kind of creators
    document_creators_dict = get_creators_role_dict(document)

    # creators
    creators = format_creators_dict(document_creators_dict, 0)
    if creators:
        result += creators

    # title
    title = format_title_of_document(document)
    if title:
        result += title

    # is_part_of
    if is_part_of:

        # "Review of"
        if rec_type in [constants.DOC_TYPE_ARTICLEREVIEW, constants.DOC_TYPE_BOOKREVIEW]:
            result += "Rev. of "

        # is_part_of_title
        is_part_of_title = format_title_of_document(is_part_of)
        if is_part_of_title:
            result += is_part_of_title

        # extract the different kind of creators
        is_part_of_creators_dict = get_creators_role_dict(is_part_of)

        # is_part_of_creators
        is_part_of_creators = format_creators_dict(is_part_of_creators_dict, 1)
        if is_part_of_creators:
            result += is_part_of_creators

        # is_part_of_is_part_of
        if is_part_of_is_part_of:

            # extract the different kind of creators
            is_part_of_is_part_of_creators_dict = get_creators_role_dict(is_part_of_is_part_of)

            # is_part_of_is_part_of_title
            is_part_of_is_part_of_title = format_title_of_document(is_part_of_is_part_of)
            if is_part_of_is_part_of_title:
                result += is_part_of_is_part_of_title

            # is_part_of_is_part_of_creators
            is_part_of_is_part_of_creators = format_creators_dict(is_part_of_is_part_of_creators_dict, 2)
            if is_part_of_is_part_of_creators:
                result += is_part_of_is_part_of_creators

    # edition
    edition = document.get_edition()
    if edition:
        result += u"<span class=\"edition\">{0}</span> ".format(edition + " ed.")

    # extent_volumes
    extent_volumes = document.get_extent_volumes()
    if extent_volumes:
        result += u"<span class=\"extent_volumes\">{0}</span>. ".format(extent_volumes)

    # degree
    if rec_type in thesis_rec_type_to_degree:
        degree = thesis_rec_type_to_degree[rec_type]
        result += u"<span class=\"thesis_degree\">{0}.</span> ".format(degree)

    # date_issued_first
    # (example aime : 208)
    if "date_issued_first" in document and document["date_issued_first"]:
        result += u"<span class=\"date\">{}</span>. ".format(date_service.format_date(document["date_issued_first"]))

    # publication_places
    publication_places = document.get_publication_places()
    if publication_places:
        result += u"<span class=\"publication_places\">{0}</span>: ".format(publication_places[0])
    elif rec_type in [constants.DOC_TYPE_BOOK, constants.DOC_TYPE_BOOKLET, constants.DOC_TYPE_BOOKPART, constants.DOC_TYPE_CONFERENCEPAPER, constants.DOC_TYPE_CONFERENCEPROCEEDINGS, constants.DOC_TYPE_DICTIONARY, constants.DOC_TYPE_DICTIONARYENTRY, constants.DOC_TYPE_DISSERTATION, constants.DOC_TYPE_DOCTORALTHESIS, constants.DOC_TYPE_EBOOK, constants.DOC_TYPE_EJOURNAL, constants.DOC_TYPE_EDITEDBOOK, constants.DOC_TYPE_ENCYCLOPEDIA, constants.DOC_TYPE_ENCYCLOPEDIAARTICLE, constants.DOC_TYPE_JOURNAL, constants.DOC_TYPE_MAGAZINE, constants.DOC_TYPE_MAP, constants.DOC_TYPE_MASTERTHESIS, constants.DOC_TYPE_MULTIVOLUMEBOOK, constants.DOC_TYPE_NEWSPAPER, constants.DOC_TYPE_PROFESSORALTHESIS, constants.DOC_TYPE_REPORT, constants.DOC_TYPE_REPORTPART, constants.DOC_TYPE_TECHREPORT]:
        result += u"<span class=\"publication_places\">N.p.</span>: "

    # publishers
    # Shorten the publisher's name; for example, omit articles, business abbreviations (Co., Inc.),
    # and descriptive words (Press, Publisher).
    # When multiple publishers are listed, include all of them, placing a semicolon between each.
    # Example aime : 368
    # publishers
    publishers = document.get_publishers()
    # creators as publishers
    if "publishers" in document_creators_dict:
        creators_publishers = document_creators_dict["publishers"]
        if not publishers:
            publishers = []
        for creator in creators_publishers:
            publishers.append(creator.formatted_name())
    if publishers:
        publishers_count = len(publishers)
        #print "publishers_count:{}".format(publishers_count)
        for position, publisher in enumerate(publishers):
            #print "position:{}".format(position)
            #print "publisher:{}".format(publisher)
            result += u"<span class=\"publishers\">{0}</span>".format(publisher)
            if publishers_count > 1 and position < publishers_count - 1:
                result += u"; "
        result += u", "

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
    date_result = date_service.format_date(date)
    if date_result:
        if rec_type in [constants.DOC_TYPE_JOURNALARTICLE]:
            date_result = u"(" + date_result + u")"

        # todo : deux point au lieu d'un point
        result += u"<span class=\"date\">{0}</span>".format(date_result)
        if not date_result.endswith("."):
            result += u". "
        else:
            result += u" "

    # part_page_begin & part_page_end
    part_page_begin = document.get_part_page_begin()
    if part_page_begin:
        result += u"<span class=\"part_page_begin\">{0}</span>".format(part_page_begin)

    part_page_end = document.get_part_page_end()
    if part_page_end:
        result += u"-<span class=\"part_page_end\">{0}</span>".format(part_page_end)

    if part_page_begin or part_page_end:
        result += ". "

    # medium of publication, date_last_accessed, url
    medium_of_publication = None
    date_last_accessed_formatted = None
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
            date_last_accessed = document["resources"][0]["date_last_accessed"]
            date_last_accessed_formatted = date_service.format_date(date_last_accessed)
    if medium_of_publication:
        result += u"<span class=\"medium_of_publication\">{0}</span>. ".format(medium_of_publication)

    if date_last_accessed_formatted:
        result += u"<span class=\"date_last_accessed\">{0}</span>. ".format(date_last_accessed_formatted)

    if url:
        result += u"<span class=\"url\">{0}</span>".format(format_url(url))

    #print result 
    #this print fires an encoding error when result contains non ascii characters
    #if print is needed :
    #   1- use python log command not print
    #   2- for encoding a result.ecnode("utf8") might solve the prb    
    return result


def remove_last_point(text):
    if text and (isinstance(text, unicode) or isinstance(text, str)):
        if text.endswith("."):
            return text[:-1]
        else:
            return text


def format_url(url):
    if url:
        return u"&lt;<a href=\"{0}\" target=\"_blank\">{0}</a>&gt;".format(url)


def format_title_of_document(document):
    # Capitalize the first word and all other principal words of the titles and subtitles
    # of cited works listed. (Do not capitalize articles, prepositions, coordinating conjunctions, or the "to" in infinitives.)
    if document and "title" in document and document["title"] is not None:
        result = u""
        if "title_non_sort" in document and document["title_non_sort"] is not None:
            result += document["title_non_sort"]
        result += remove_last_point(document["title"])
        if "title_sub" in document and document["title_sub"]:
            result += u": " + remove_last_point(document["title_sub"])
        if "is_part_ofs" in document:
            return u"\"<span class=\"title\">{0}</span>.\" ".format(result)
        else:
            return u"<span class=\"title\">{0}</span>. ".format(result)


def get_creators_role_dict(document):
    result = {}
    if "creators" in document:
        # Sort the creators in 3 types:
        # author
        # publisher
        # contributor
        for creator in document["creators"]:
            if "role" in creator:
                role = creator["role"]
                if role in ["act", "aut", "com", "drt", "edt", "pbd", "pro", "sce", "trl", "nrt"]:
                    add_item_to_key_of_dict(creator, "authors", result)
                elif role in ["dgg", "dst", "pbl"]:
                    add_item_to_key_of_dict(creator, "publishers", result)
                elif role in ["cph"]:
                    add_item_to_key_of_dict(creator, "copyright", result)
                else:
                    add_item_to_key_of_dict(creator, "contributors", result)
            else:
                add_item_to_key_of_dict(creator, "contributors", result)
    return result


def add_item_to_key_of_dict(item, key, dic):
    if item:
        try:
            dic[key].append(item)
        except:
            dic[key] = [item]


def format_creators_dict(creators_dict, level):
    if "authors" in creators_dict:
        result = ""

        contri_count = len(creators_dict["authors"])

        #print "level: {}".format(level)
        #print "contri_count: {}".format(contri_count)

        for position, creator in enumerate(creators_dict["authors"]):
            #print "position: {}".format(position)
            # prefix
            formatted_name = format_creator(creator, position, level)
            if formatted_name:
                prefix = u""
                suffix = u""

                if contri_count > 1:
                    if 0 < position < contri_count - 1:
                        prefix = u", "
                    elif position == contri_count - 1:
                        prefix = u", and "

                if not (formatted_name.endswith(".") or formatted_name.endswith(".</span>")) and position == contri_count - 1:
                    suffix = u"."

                # formatted_name
                result += u"{}<span class=\"creator\">{}</span>{}".format(prefix, formatted_name, suffix)
                
                # et al
                # deactivated
                #if contri_count > 3:
                #    result += u", <span class=\"creator\">et al.</span>"
                #    print result
                #    break


        #print result
        return result + " "


def format_creator(creator, position, level):
    style = metajson.STYLE_FAMILY_COMMA_GIVEN
    if level > 0 or position > 0:
        style = metajson.STYLE_GIVEN_FAMILY
    formatted_name = creator.formatted_name(style)
    if formatted_name:
        if level == 0:
            if creator["role"] in role_to_short_forms:
                short_form = role_to_short_forms[creator["role"]][0]
                if short_form:
                    formatted_name = formatted_name + ", <span class=\"creator_role\">" + short_form + "</span>"
        else:
            if creator["role"] in role_to_short_forms:
                short_form = role_to_short_forms[creator["role"]][1]
                if short_form:
                    formatted_name = "<span class=\"creator_role\">" + short_form + "</span> " + formatted_name
        if formatted_name:
            return formatted_name
