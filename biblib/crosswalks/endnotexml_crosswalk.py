#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import xml.etree.ElementTree as ET

from biblib.metajson import Document
from biblib.metajson import Resource
from biblib.services import contributor_service
from biblib.services import language_service

endnote_import_note = False
endnote_import_research_note = False
endnote_import_keywords = False

TYPE_ARTWORK = "2"
TYPE_AUDIOVISUAL_MATERIAL = "3"
TYPE_BILL = "4"
TYPE_BOOK_SECTION = "5"
TYPE_BOOK = "6"
TYPE_CASE = "7"
TYPE_SOFTWARE = "9"
TYPE_CONFERENCE_PROCEEDINGS = "10"
TYPE_WEB_PAGE = "12"
TYPE_GENERIC = "13"
TYPE_HEARING = "14"
TYPE_JOURNAL_ARTICLE = "17"
TYPE_MAGAZINE_ARTICLE = "19"
TYPE_MAP = "20"
TYPE_FILM_OR_BROADCAST = "21"
TYPE_NEWSPAPER_ARTICLE = "23"
TYPE_PATENT = "25"
TYPE_PERSONAL_COMMUNICATION = "26"
TYPE_REPORT = "27"
TYPE_EDITED_BOOK = "28"
TYPE_STATUTE = "31"
TYPE_THESIS = "32"
TYPE_UNPUBLISHED_WORK = "34"
TYPE_MANUSCRIPT = "36"
TYPE_FIGURE = "37"
TYPE_CHART_OR_TABLE = "38"
TYPE_EQUATION = "39"
TYPE_ELECTRONIC_ARTICLE = "43"
TYPE_ELECTRONIC_BOOK = "44"
TYPE_ONLINE_DATABASE = "45"
TYPE_GOVERNMENT_DOCUMENT = "46"
TYPE_CONFERENCE_PAPER = "47"
TYPE_ONLINE_MULTIMEDIA = "48"
TYPE_CLASSICAL_WORK = "49"
TYPE_LEGAL_RULE_OR_REGULATION = "50"
TYPE_ENCYCLOPEDIA = "53"
TYPE_GRANT = "54"

endnote_record_type_to_metajson_document_type = {
    "Aggregated Database": "Document",
    "Ancient Text": "UnpublishedDocument",
    TYPE_ARTWORK: "Image",
    TYPE_AUDIOVISUAL_MATERIAL: "AudioRecording",
    TYPE_BILL: "Document",
    "Blog": "WebEntity",
    TYPE_BOOK: "Book",
    TYPE_BOOK_SECTION: "BookPart",
    TYPE_CASE: "Document",
    "Catalog": "Document",
    TYPE_CHART_OR_TABLE: "Image",
    TYPE_CLASSICAL_WORK: "AudioRecording",
    "Computer Program": "Software",
    TYPE_CONFERENCE_PAPER: "BookPart",
    TYPE_CONFERENCE_PROCEEDINGS: "Book",
    "Dataset": "Document",
    "Dictionary": "Dictionary",
    TYPE_EDITED_BOOK: "Book",
    TYPE_ENCYCLOPEDIA: "Book",
    TYPE_ELECTRONIC_ARTICLE: "Article",
    "Electronic Book Section": "BookPart",
    TYPE_EQUATION: "Document",
    TYPE_FIGURE: "Image",
    TYPE_FILM_OR_BROADCAST: "Film",
    TYPE_GRANT: "UnpublishedDocument",
    TYPE_GENERIC: "Document",
    TYPE_GOVERNMENT_DOCUMENT: "Document",
    TYPE_HEARING: "Document",
    TYPE_JOURNAL_ARTICLE: "Article",
    "Legal": "Document",
    TYPE_LEGAL_RULE_OR_REGULATION: "Document",
    TYPE_MAGAZINE_ARTICLE: "Article",
    TYPE_MANUSCRIPT: "UnpublishedDocument",
    TYPE_MAP: "Image",
    TYPE_NEWSPAPER_ARTICLE: "Article",
    TYPE_ONLINE_DATABASE: "Document",
    TYPE_ONLINE_MULTIMEDIA: "WebEntity",
    TYPE_PATENT: "Document",
    TYPE_REPORT: "UnpublishedDocument",
    "Serial": "Document",
    "Standard": "Document",
    TYPE_STATUTE: "Document",
    TYPE_THESIS: "Thesis",
    TYPE_UNPUBLISHED_WORK: "UnpublishedDocument",
    TYPE_WEB_PAGE: "WebEntity"
}

endnote_record_type_to_metajson_document_is_part_of_type = {
    TYPE_BOOK_SECTION: "Book",
    TYPE_CONFERENCE_PAPER: "ConferenceProceedings",
    TYPE_ELECTRONIC_ARTICLE: "Journal",
    "Electronic Book Section": "Book",
    TYPE_JOURNAL_ARTICLE: "Journal",
    TYPE_MAGAZINE_ARTICLE: "Magazine",
    TYPE_NEWSPAPER_ARTICLE: "Newspaper"
}


def endnotexml_xmletree_to_metajson_list(endnotexml_root, source, only_first_record):
    records_elements = endnotexml_root.find("records")
    records = records_elements.findall("record")

    if records:
        for record in records:
            yield endnotexml_record_to_metajson(record, source)


def endnotexml_record_to_metajson(record, source):
    document = Document()

    # TODO
    # translated_contributors: /contributors/translated-authors/author/style
    # auth_address: /auth-address/style
    # label: /label/style
    # custom1

    # Extract endnote properties

    rec_id = record.find("rec-number").text
    endnote_type = record.find("ref-type").text
    rec_type = endnote_record_type_to_metajson_document_type[endnote_type]

    primary_contributors = extract_contributors(None, "aut", record, "./contributors/authors/author/style")
    secondary_contributors = extract_contributors(None, "edt", record, "./contributors/secondary-authors/author/style")
    if endnote_type in [TYPE_BOOK, TYPE_BOOK_SECTION]:
        tertiary_contributors = extract_contributors(None, "edt", record, "./contributors/tertiary-authors/author/style")
    elif endnote_type == TYPE_THESIS:
        tertiary_contributors = extract_contributors(None, "ths", record, "./contributors/tertiary-authors/author/style")
    elif endnote_type == TYPE_FILM_OR_BROADCAST:
        tertiary_contributors = extract_contributors(None, "pro", record, "./contributors/tertiary-authors/author/style")
    if endnote_type in [TYPE_BOOK, TYPE_BOOK_SECTION]:
        subsidiary_contributors = extract_contributors(None, "trl", record, "./contributors/subsidiary-authors/author/style")
    elif endnote_type == TYPE_FILM_OR_BROADCAST:
        subsidiary_contributors = extract_contributors(None, "act", record, "./contributors/subsidiary-authors/author/style")
    translated_contributors = extract_contributors(None, "trl", record, "./contributors/translated-authors/author/style")
    auth_address = extract_text(record, "./auth-address/style")

    title = extract_text(record, "./titles/title/style")
    title_secondary = extract_text(record, "./titles/secondary-title/style")
    title_tertiary = extract_text(record, "./titles/tertiary-title/style")
    title_alternative = extract_text(record, "./titles/alt-title/style")
    title_abbreviated = extract_text(record, "./titles/short-title/style")
    title_translated = extract_text(record, "./titles/translated-title/style")

    pages = extract_text(record, "./pages/style")
    part_volume = extract_text(record, "./volume/style")
    part_number = extract_text(record, "./number/style")
    extent_volumes = extract_text(record, "./num-vols/style")
    edition = extract_text(record, "./edition/style")
    part_section = extract_text(record, "./section/style")
    reprint_edition = extract_text(record, "./reprint-edition/style")
    keywords = extract_text(record, "./keywords/keyword/style")
    date_year = extract_text(record, "./dates/year/style")
    date_pub = extract_text(record, "./dates/pub-dates/date/style")
    publisher_place = extract_text(record, "./pub-location/style")
    publisher = extract_text(record, "./publisher/style")
    orig_pub = extract_text(record, "./orig-pub/style")
    isbn_or_issn = extract_text(record, "./isbn/style")
    accessionnumber = extract_text(record, "./accession-num/style")
    callnumber = extract_text(record, "./call-num/style")
    if endnote_type == TYPE_WEB_PAGE:
        abstract = extract_text(record, "./pages/style")
    else:
        abstract = extract_text(record, "./abstract/style")
    label = extract_text(record, "./label/style")
    caption = extract_text(record, "./caption/style")
    note = extract_text(record, "./notes/style")
    reviewed_item = extract_text(record, "./reviewed-item/style")
    rec_type_description = extract_text(record, "./work-type/style")
    remote_url = extract_text(record, "./urls/related-urls/url/style")
    custom1 = extract_text(record, "./custom1/style")
    custom2 = extract_text(record, "./custom2/style")
    custom3 = extract_text(record, "./custom3/style")
    custom4 = extract_text(record, "./custom4/style")
    custom5 = extract_text(record, "./custom5/style")
    custom6 = extract_text(record, "./custom6/style")
    custom7 = extract_text(record, "./custom7/style")
    doi = extract_text(record, "./electronic-resource-num/style")
    remote_database_name = extract_text(record, "./remote-database-name/style")
    remote_database_provider = extract_text(record, "./remote-database-provider/style")
    research_notes = extract_text(record, "./research-notes/style")
    language = extract_text(record, "./language/style")
    access_date = extract_text(record, "./access-date/style")

    # rec_id, rec_source
    document["rec_id"] = rec_id
    document["rec_source"] = source

    # publisher, publisher_place
    if publisher:
        publisher = publisher.replace("\r", "; ")
    if publisher_place:
        publisher_place = publisher_place.replace("\r", "; ")

    # type, is_part_of.type, is_part_of.is_part_of.type
    try:
        is_part_of_type = endnote_record_type_to_metajson_document_is_part_of_type[endnote_type]
    except:
        is_part_of_type = None

    is_part_of_is_part_of_type = None
    if title_secondary is not None:
        if endnote_type == TYPE_FIGURE:
            # how to determine the is_part_of type ?
            # if there is a volume or an issue number, it's a JournalArticle, else it's a Book or BookChapter
            if part_volume is not None or part_number is not None:
                is_part_of_type = "Article"
                is_part_of_is_part_of_type = "Journal"
            else:
                if title_translated is not None:
                    is_part_of_type = "BookPart"
                    is_part_of_is_part_of_type = "Book"
                else:
                    is_part_of_type = "Book"
        elif endnote_type == TYPE_FILM_OR_BROADCAST:
            rec_type = "VideoPart"
            is_part_of_type = "VideoRecording"

    document["rec_type"] = rec_type
    document.set_key_if_not_none("rec_type_description", rec_type_description)

    # issn or isbn ?
    if is_part_of_type in ["Journal", "Newspaper", "Article"]:
        isbn_or_issn_type = "issn"
    else:
        isbn_or_issn_type = "isbn"

    # is_part_of, is_part_of.is_part_of
    if is_part_of_type is not None:
        is_part_of = Document()
        is_part_of.set_key_if_not_none("rec_type", is_part_of_type)
        is_part_of.set_key_if_not_none("title", title_secondary)

        if is_part_of_is_part_of_type is not None:
            # is_part_of in case of is_part_of.is_part_of
            # contributors with role aut
            is_part_of.add_contributors(contributor_service.change_contibutors_role(secondary_contributors, "aut"))

            # is_part_of.is_part_of
            is_part_of_is_part_of = Document()
            is_part_of_is_part_of.set_key_if_not_none("rec_type", is_part_of_is_part_of_type)
            is_part_of_is_part_of.set_key_if_not_none("title", title_translated)
            # contributors with role edt
            is_part_of_is_part_of.add_contributors(contributor_service.change_contibutors_role(translated_contributors, "edt"))
            #is_part_of_is_part_of.set_key_if_not_none("date_issued",date_year)
            is_part_of_is_part_of.set_key_if_not_none("publisher", publisher)
            is_part_of_is_part_of.set_key_if_not_none("publisher_place", publisher_place)
            is_part_of_is_part_of.set_key_with_value_type_in_list("identifiers", isbn_or_issn, isbn_or_issn_type)

            is_part_of.add_items_to_key([is_part_of_is_part_of], "is_part_of")

        else:
            # is_part_of in case of no is_part_of.is_part_of
            # contributors with role edt
            is_part_of.add_contributors(secondary_contributors)
            #is_part_of.set_key_if_not_none("date_issued",date_year)
            is_part_of.set_key_if_not_none("publisher", publisher)
            is_part_of.set_key_if_not_none("publisher_place", publisher_place)
            is_part_of.set_key_with_value_type_in_list("identifiers", isbn_or_issn, isbn_or_issn_type)

        document.add_items_to_key([is_part_of], "is_part_of")

    else:
        document.set_key_with_value_type_in_list("identifiers", isbn_or_issn, isbn_or_issn_type)
        if publisher:
            if endnote_type == TYPE_THESIS:
                document.add_contributors([contributor_service.formatted_name_to_contributor(publisher, "orgunit", "dgg")])
            elif endnote_type == TYPE_FILM_OR_BROADCAST:
                document.add_contributors([contributor_service.formatted_name_to_contributor(publisher, "orgunit", "dst")])
            else:
                document.set_key_if_not_none("publisher", publisher)
        document.set_key_if_not_none("publisher_place", publisher_place)

    # series[]
    if endnote_type in [TYPE_BOOK, TYPE_BOOK_SECTION]:
        series = Document()
        if endnote_type == TYPE_BOOK and title_secondary:
            series.set_key_if_not_none("title", title_secondary)
            series.add_contributors(secondary_contributors)
            series.set_key_if_not_none("part_volume", part_number)
        if endnote_type == TYPE_BOOK_SECTION and title_tertiary:
            series.set_key_if_not_none("title", title_tertiary)
            series.add_contributors(tertiary_contributors)
            series.set_key_if_not_none("part_volume", part_number)
        if "title" in series and len(series) > 2:
            document.add_items_to_key([series], "series")

    # originals[]
    if (reprint_edition or orig_pub) and endnote_type in [TYPE_BOOK, TYPE_BOOK_SECTION, TYPE_JOURNAL_ARTICLE, TYPE_FILM_OR_BROADCAST]:
        original = Document()
        if reprint_edition:
            original_title = reprint_edition
        elif orig_pub:
            original_title = orig_pub
        original.set_key_if_not_none("title", original_title)
        original.set_key_if_not_none("rec_type", rec_type)
        document.add_items_to_key([original], "original")

    # review_of[]
    if reviewed_item and endnote_type in [TYPE_BOOK_SECTION, TYPE_JOURNAL_ARTICLE]:
        review_of = Document()
        review_of.set_key_if_not_none("title", reviewed_item)
        review_of.set_key_if_not_none("rec_type", "Book")
        document.add_items_to_key([review_of], "review_of")

    # abstracts[0].value
    if abstract:
        document["abstracts"] = [{"value": abstract}]

    # archive
    if endnote_type == TYPE_FIGURE and remote_database_provider:
        archive = Document()
        archive["title"] = remote_database_provider
        document.add_items_to_key([archive], "archive")

    # caption
    document.set_key_if_not_none("caption", caption)

    # contributors[]
    document.add_contributors(primary_contributors)
    if endnote_type in [TYPE_BOOK, TYPE_THESIS, TYPE_FILM_OR_BROADCAST]:
        document.add_contributors(tertiary_contributors)
    if endnote_type in [TYPE_BOOK, TYPE_BOOK_SECTION, TYPE_FILM_OR_BROADCAST]:
        document.add_contributors(subsidiary_contributors)
    if custom4:
        document.add_contributors(endnote_authors_to_contributors(custom4, "person", "rev"))
    if endnote_type == TYPE_FIGURE and remote_database_name:
        document.add_contributors(endnote_authors_to_contributors(remote_database_name, None, "cph"))

    # edition
    if endnote_type in [TYPE_BOOK, TYPE_BOOK_SECTION, TYPE_FILM_OR_BROADCAST, TYPE_WEB_PAGE] and edition:
        document["edition"] = edition

    # extent_pages, extent_volumes
    if endnote_type in [TYPE_BOOK, TYPE_THESIS] and pages:
        document["extent_pages"] = pages.replace("p.", "").strip()
    if endnote_type in [TYPE_BOOK, TYPE_BOOK_SECTION] and extent_volumes:
        document["extent_volumes"] = extent_volumes

    # date_issued, date_issued_first
    if date_year:
        date_issued = ""
        date_issued_first = ""
        orig_index_start = date_year.find("[")
        orig_index_end = date_year.find("]")
        if orig_index_start != -1 and orig_index_end != -1:
            date_issued_first = date_year[orig_index_start + 1: orig_index_end]
            date_issued = date_year.replace("[" + date_issued_first + "]", "").strip()
        else:
            date_issued = date_year.strip()

        if "is_part_of" in document:
            if document["is_part_of"][0]["rec_type"] == "Book":
                document["is_part_of"][0].set_key_if_not_none("date_issued", date_issued)
                document["is_part_of"][0].set_key_if_not_none("date_issued_first", date_issued_first)
            elif "is_part_of" in document["is_part_of"][0] and document["is_part_of"][0]["is_part_of"][0]["rec_type"] == "Book":
                document["is_part_of"][0]["is_part_of"][0].set_key_if_not_none("date_issued", date_issued)
                document["is_part_of"][0]["is_part_of"][0].set_key_if_not_none("date_issued_first", date_issued_first)
            else:
                document.set_key_if_not_none("date_issued_first", date_issued_first)
                document.set_key_if_not_none("date_issued", date_issued)
        else:
            document.set_key_if_not_none("date_issued_first", date_issued_first)
            document.set_key_if_not_none("date_issued", date_issued)

    # identifiers[]
    document.set_key_with_value_type_in_list("identifiers", accessionnumber, "accessionnumber")
    document.set_key_with_value_type_in_list("identifiers", callnumber, "callnumber")
    document.set_key_with_value_type_in_list("identifiers", doi, "doi")

    # language
    if language:
        iso639_2 = language_service.convert_unknown_format_to_iso639_2(language)
        if iso639_2:
            document["languages"] = [{"authority": "iso639-2b", "value": iso639_2}]

    # note
    if endnote_import_note and note:
        document.set_key_with_value_type_in_list("notes", note, "general")
    if endnote_import_research_note and research_notes:
        document.set_key_with_value_type_in_list("notes", research_notes, "user")

    # part_page_start & part_page_end
    if endnote_type in [TYPE_BOOK_SECTION, TYPE_FIGURE, TYPE_JOURNAL_ARTICLE] and pages:
        hyphen_index = pages.find("-")
        if hyphen_index == -1:
            document["part_page_start"] = pages.replace("p.", "").strip()
        else:
            document["part_page_start"] = pages[:hyphen_index].replace("p.", "").strip()
            document["part_page_end"] = pages[hyphen_index+1:].replace("p.", "").strip()

    if endnote_type in [TYPE_JOURNAL_ARTICLE]:
        document.set_key_if_not_none("part_issue", part_number)
    elif endnote_type in [TYPE_FIGURE]:
        document.set_key_if_not_none("part_number", part_number)
    document.set_key_if_not_none("part_section", part_section)
    document.set_key_if_not_none("part_volume", part_volume)

    # resources[0]
    if remote_url is not None:
        resource = Resource()
        resource.set_key_if_not_none("remote_url", remote_url)
        if endnote_type == TYPE_WEB_PAGE:
            resource.set_key_if_not_none("date_last_accessed", part_number)
        else:
            resource.set_key_if_not_none("date_last_accessed", access_date)
        document["resources"] = [resource]

    # subjects[]
    if endnote_import_keywords and keywords:
        for keyword in keywords.split():
            document.set_key_with_value_type_in_list("subjects", keyword, "topic")

    # title, title_alternative, title_abbreviated, title_translated
    document["title"] = title
    if title_alternative:
        document["title_alternative"] = [{"title": title_alternative}]
    if title_abbreviated:
        document["title_abbreviated"] = [{"title": title_abbreviated}]
    if not is_part_of_is_part_of_type and title_translated:
        # the title_translated is used for the is_part_of.is_part_of_type.title
        document["title_translated"] = [{"title": title_translated}]

    debug = True
    if debug:
        related_items_msg = ""
        if is_part_of_type:
            related_items_msg = "\tis_part_of: {} ".format(is_part_of_type)
        if is_part_of_is_part_of_type:
            related_items_msg += "\tis_part_of.is_part_of: {} ".format(is_part_of_is_part_of_type)
        print "# {}\t:\t{}\t:\t{}\t->\titem: {} {}".format(source, rec_id, endnote_type, rec_type, related_items_msg, title)

    return document


def extract_list(element, xpath):
    styles_xml_element = element.findall(xpath)
    if len(styles_xml_element) != 0:
        try:
            return [style.text for style in styles_xml_element if style is not None]
        except:
            return "error extract_list %s" % (ET.tostring(element))


def extract_text(element, xpath):
    styles = extract_list(element, xpath)
    if styles is not None and len(styles) != 0:
        try:
            result = "".join(styles).strip()
            if result == "":
                return None
            else:
                return result
        except:
            return "error extract_text %s" % (ET.tostring(element))


def extract_text_and_set_key(common_dict, key, element, xpath):
    common_dict.set_key_if_not_none(key, extract_text(element, xpath))


def extract_text_and_set_key_with_type_in_list(common_dict, key, my_type, element, xpath):
    common_dict.set_key_with_value_type_in_list(key, extract_text(element, xpath), my_type)


def extract_contributors(contributor_type, role, element, xpath):
    authors_list = extract_list(element, xpath)
    if authors_list is not None and len(authors_list) != 0:
        contributors = []
        for author_item in authors_list:
            contributors.extend(endnote_authors_to_contributors(author_item, contributor_type, role))
        return contributors


def extract_and_set_contributors(common_dict, contributor_type, role, element, xpath):
    common_dict.add_contributors(extract_contributors(contributor_type, role, element, xpath))


def endnote_authors_to_contributors(authors, contributor_type="person", role="aut"):
    contributors = []
    for author in authors.splitlines():
        contributor = contributor_service.formatted_name_to_contributor(author, contributor_type, role)
        if contributor:
            contributors.append(contributor)
    return contributors
