#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Document
from biblib.metajson import Creator
from biblib.metajson import Identifier
from biblib.metajson import Resource
import xml.etree.ElementTree as ET


def unixref_xmletree_to_metajson_list(unixref_xmletree, source, only_first_record=False):
    if unixref_xmletree is not None:
        records = unixref_xmletree.findall('doi_record')
        if records:
            if only_first_record:
                yield unixref_record_to_metajson(records[0], source)
            else:
                for record in records:
                    yield unixref_record_to_metajson(record, source)


def unixref_record_to_metajson(record, source):
    journal_metadata = record.find("./crossref/journal/journal_metadata")
    if journal_metadata is not None:
        journal_title = journal_metadata.find("full_title")
        journal_title_abbreviated = journal_metadata.find("abbrev_title")
        for issn in journal_metadata.findall("issn"):
            if issn.get("media_type") == "print":
                journal_issn = issn
            elif issn.get("media_type") == "electronic":
                journal_eissn = issn

    journal_issue = record.find("./crossref/journal/journal_issue")
    if journal_issue is not None:
        part_issue = journal_issue.find("issue")
        part_volume = journal_issue.find("journal_volume/volume")

    journal_article = record.find("./crossref/journal/journal_article")
    if journal_article is not None:
        titles = journal_article.findall("titles/title")
        creators = journal_article.findall("creators")
        year = journal_article.find("publication_date/year")
        month = journal_article.find("publication_date/month")
        day = journal_article.find("publication_date/day")
        part_page_begin = journal_article.find("pages/first_page")
        part_page_end = journal_article.find("pages/last_page")
        doi = journal_article.find("doi_data/doi")
        resource_url = journal_article.find("doi_data/resource")

    document = Document()
    # todo: how to find the type ?
    document["rec_type"] = "JournalArticle"

    if doi is not None:
        document.set_key_with_value_type_in_list("identifiers", doi.text, "doi")

    if resource_url is not None:
        resource = Resource()
        resource["url"] = resource_url.text
        document["resources"] = [resource]

    if source is not None:
        document["rec_source"] = source

    if titles is not None and len(titles) > 0:
        document["title"] = titles[0].text

    date_issued = year.text
    if month is not None:
        month = month.text
        if len(month) == 1:
            month = "0" + month
        date_issued += "-" + month
    if day is not None:
        day = day.text
        if len(day) == 1:
            day = "0" + day
        date_issued += "-" + day
    document["date_issued"] = date_issued

    if part_issue is not None:
        document["part_issue"] = part_issue.text

    if part_volume is not None:
        document["part_volume"] = part_volume.text

    if part_page_begin is not None:
        document["part_page_begin"] = part_page_begin.text

    if part_page_end is not None:
        document["part_page_end"] = part_page_end.text

    # todo: creator

    is_part_of = Document()
    # todo: how to find the type ?
    is_part_of["rec_type"] = "Journal"

    if journal_title is not None:
        is_part_of["title"] = journal_title.text
    if journal_title_abbreviated is not None:
        is_part_of["title_abbreviated"] = journal_title_abbreviated.text
    if journal_issn is not None:
        is_part_of.set_key_with_value_type_in_list("identifiers", journal_issn.text, "issn")
    if journal_eissn is not None:
        is_part_of.set_key_with_value_type_in_list("identifiers", journal_eissn.text, "eissn")

    document["is_part_ofs"] = [is_part_of]

    return document
