#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from metadatas.metajson import Common, Document, Contributor, Identifier, Resource
import xml.etree.ElementTree as ET
import bson


def convert_crossref_unixref_records_to_metajson_document_list(unixref, source, only_first_result=False):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(unixref, parser=parser)
    records_elements = tree.getroot()
    records = records_elements.findall('doi_record')

    document_list = []
    if records:
        if only_first_result:
            document_list.append(convert_crossref_unixref_record_to_metajson_document(records[0], source))
        else:
            for record in records:
                document_list.append(convert_crossref_unixref_record_to_metajson_document(record, source))
    return document_list


def convert_crossref_unixref_record_to_metajson_document(record, source):
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
        contributors = journal_article.findall("contributors")
        year = journal_article.find("publication_date/year")
        month = journal_article.find("publication_date/month")
        day = journal_article.find("publication_date/day")
        part_page_start = journal_article.find("pages/first_page")
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
        resource["remote_url"] = resource_url.text
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

    if part_page_start is not None:
        document["part_page_start"] = part_page_start.text

    if part_page_end is not None:
        document["part_page_end"] = part_page_end.text

    # todo: contributor

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

    document["is_part_of"] = [is_part_of]

    return document


document_list = convert_crossref_unixref_records_to_metajson_document_list("../test/data/unixref2.xml", "test")
print bson.json_util.dumps(document_list[0], ensure_ascii=False, indent=4, encoding="utf-8", sort_keys=True)
