#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from referencemanager import metajson
from referencemanager.metajson import Collection
from referencemanager.metajson import Document
from referencemanager.metajson import Contributor
from referencemanager.metajson import Subject
from referencemanager.services import contributor_service
from referencemanager.services import language_service


summon_document_type_to_metajson_document_type = {
    "Audio Recording": "AudioRecording",
    "Book": "Book",
    "Book Chapter": "BookPart",
    "Book Review": "BookReview",
    "Case": "LegalCase",
    "Computer File": "Software",
    "Conference Proceeding": "Book",
    "Data Set": "Dataset",
    "Dissertation": "Thesis",
    "Image": "Image",
    "Journal": "Journal",
    "Journal Article": "JournalArticle",
    "Magazine": "Magazine",
    "Magazine Article": "MagazineArticle",
    "Manuscript": "UnpublishedDocument",
    "Map": "Map",
    "Music Recording": "MusicRecording",
    "Music Score": "MusicalScore",
    "Newspaper": "Newspaper",
    "Newspaper Article": "NewspaperArticle",
    "Patent": "Patent",
    "Poster": "ConferencePoster",
    "Realia": "PhysicalObject",
    "Reference": "Dictionary",
    "Report": "Report",
    "Thesis": "Thesis",
    "Video Recording": "VideoRecording",
    "Web Resource": "WebEntity"
}


summon_document_type_to_metajson_document_is_part_of_type = {
    "Book Chapter": "Book",
    "Book Review": "Journal",
    "Journal Article": "Journal",
    "Magazine Article": "Magazine",
    "Newspaper Article": "Newspaper"
}


summon_identifier_type_to_metajson_identifier_type = {
    "CODEN": "coden",
    "DOI": "doi",
    "EAN": "ean",
    "EISBN": "eisbn",
    "EISSN": "eissn",
    "ISBN": "isbn",
    "ISMN": "ismn",
    "ISRC": "isrc",
    "ISSN": "issn",
    "LCCallNum": "lccallnum",
    "LCCN": "lccn",
    "OCLC": "oclc",
    "PatentNumber": "patentnumber",
    "PCID": "pmcid",
    "PMID": "pmid",
    "SICI": "sici",
    "ID": "summon",
    "URI": "uri"
}


def convert_summon_json_file_to_metajson_document_list(summon_filename):
    with open(summon_filename, "r") as summon_file:
        summon_result = json.loads(summon_file.read())
        return convert_summon_json_result_to_metajson_document_list(summon_result, summon_filename)


def convert_summon_json_result_to_metajson_document_list(summon_result, source, only_first_result=False):
    if "documents" in summon_result:
        return convert_summon_json_document_list_to_metajson_document_list(summon_result["documents"], source, only_first_result)


def convert_summon_json_document_list_to_metajson_document_list(sum_doc_list, source, only_first_result=False):
    results = []
    for sum_doc in sum_doc_list:
        results.append(convert_summon_json_document_to_metajson_document(sum_doc, source))
    return results


def convert_summon_json_document_to_metajson_document(sum_doc, source):
    document = Document()

    # Extract Summon properties
    rec_id = sum_doc["ID"][0].replace("FETCH-", "")
    sum_type = sum_doc["ContentType"][0]
    rec_type = summon_document_type_to_metajson_document_type[sum_type]

    # rec_id, rec_source, rec_type
    document["rec_id"] = rec_id
    document["rec_source"] = source
    document["rec_type"] = rec_type

    # languages
    main_language = None
    if "Language" in sum_doc:
        languages = []
        for sum_lang in sum_doc["Language"]:
            lang = language_service.convert_english_to_rfc5646(sum_lang)
            if lang:
                languages.append(lang)
        if languages:
            main_language = languages[0]
            document["languages"] = languages

    # extract summon properties
    contributors = extract_contributors(sum_doc)
    copyright_statement = extract_value(sum_doc, "Copyright")
    date_issued = extract_date_issued(sum_doc)
    degree = extract_value(sum_doc, "DissertationDegree")
    descriptions = extract_convert_langstrings(sum_doc, "Abstract", main_language)
    edition = extract_value(sum_doc, "Edition")
    extent_pages = extract_value(sum_doc, "PageCount")
    genre = extract_value(sum_doc, "Genre")
    is_part_of_edition = extract_value(sum_doc, "PublicationEdition")
    is_part_of_title = extract_value(sum_doc, "PublicationTitle")
    is_part_of_title_sub = extract_value(sum_doc, "PublicationSubtitle")
    notes = extract_convert_langstrings(sum_doc, "Notes", main_language)
    part_issue = extract_value(sum_doc, "Issue")
    part_page_end = extract_value(sum_doc, "EndPage")
    part_page_start = extract_value(sum_doc, "StartPage")
    part_volume = extract_value(sum_doc, "Volume")
    peer_reviewed = extract_boolean_value(sum_doc, "IsPeerReviewed")
    publisher = extract_value(sum_doc, "Publisher")
    publisher_place = extract_value(sum_doc, "PublicationPlace")
    scholarly = extract_boolean_value(sum_doc, "IsScholarly")
    series_title = extract_value(sum_doc, "PublicationSeriesTitle")
    subject_keywords = extract_value(sum_doc, "Keywords", True)
    subject_names = convert_contributors(sum_doc, "RelatedPersons", None, "person", None)
    subject_terms = extract_value(sum_doc, "SubjectTerms", True)
    table_of_contents = extract_convert_langstrings(sum_doc, "TableOfContents", main_language)
    title = extract_value(sum_doc, "Title")
    title_sub = extract_value(sum_doc, "Subtitle")

    # identifiers
    has_isbn = False
    has_eissn = False
    identifiers_item = []
    identifiers_is_part_of = []
    for sum_key in summon_identifier_type_to_metajson_identifier_type:
        if sum_key in sum_doc:
            for id_value in sum_doc[sum_key]:
                id_type = summon_identifier_type_to_metajson_identifier_type[sum_key]
                if id_type == "issn":
                    identifiers_is_part_of.append(metajson.create_identifier(id_type, id_value))
                elif id_type == "eissn":
                    has_eissn = True
                    identifiers_is_part_of.append(metajson.create_identifier(id_type, id_value))
                elif id_type == "isbn":
                    has_isbn = True
                    identifiers_is_part_of.append(metajson.create_identifier(id_type, id_value))
                else:
                    identifiers_item.append(metajson.create_identifier(id_type, id_value))

    # is_part_of_type determination
    is_part_of_type = None
    if sum_type in summon_document_type_to_metajson_document_is_part_of_type:
        is_part_of_type = summon_document_type_to_metajson_document_is_part_of_type[sum_type]

    elif is_part_of_title and is_part_of_title != title and rec_type not in ["Book", "Journal", "Magazine", "Newspaper", "Periodical"]:
        if has_isbn:
            is_part_of_type = "Book"
        elif has_eissn:
            is_part_of_type = "Journal"
        elif is_part_of_title.lower().find("conference") != -1:
            is_part_of_type = "Book"
        elif is_part_of_title.lower().find("review") or is_part_of_title.lower().find("journal"):
            is_part_of_type = "Journal"
        elif rec_type == "Dataset":
            is_part_of_type = "Periodical"
        else:
            print "unknown is_part_of_type for rec_type: %s" % rec_type

    # is_part_of
    if is_part_of_type:
        is_part_of = Document()
        is_part_of.set_key_if_not_none("rec_type", is_part_of_type)
        is_part_of.set_key_if_not_none("edition", is_part_of_edition)
        is_part_of.add_items_to_key(identifiers_is_part_of, "identifiers")
        is_part_of.set_key_if_not_none("peer_reviewed", peer_reviewed)
        is_part_of.set_key_if_not_none("publisher", publisher)
        is_part_of.set_key_if_not_none("publisher_place", publisher_place)
        is_part_of.set_key_if_not_none("title", is_part_of_title)
        is_part_of.set_key_if_not_none("title_sub", is_part_of_title_sub)

        document.add_items_to_key(identifiers_item, "identifiers")

        document.add_items_to_key([is_part_of], "is_part_of")
    else:
        document.set_key_if_not_none("peer_reviewed", peer_reviewed)
        document.set_key_if_not_none("publisher", publisher)
        document.set_key_if_not_none("publisher_place", publisher_place)
        document.add_items_to_key(identifiers_is_part_of, "identifiers")
        document.add_items_to_key(identifiers_item, "identifiers")

    # series
    if series_title:
        series = Document()
        series.set_key_if_not_none("title", series_title)

        document.add_items_to_key([series], "series")

    # classificiations
    extract_convert_add_classifications(sum_doc, document, "DEWEY", "ddc")
    extract_convert_add_classifications(sum_doc, document, "Discipline", "discipline")
    extract_convert_add_classifications(sum_doc, document, "NAICS", "NAICS")

    # set properties
    document.set_key_if_not_none("contributors", contributors)
    document.set_key_if_not_none("copyright_statement", copyright_statement)
    document.set_key_if_not_none("date_issued", date_issued)
    document.set_key_if_not_none("degree", degree)
    document.set_key_if_not_none("descriptions", descriptions)
    document.set_key_if_not_none("edition", edition)
    document.set_key_if_not_none("extent_pages", extent_pages)
    document.set_key_if_not_none("genre", genre)
    document.set_key_if_not_none("notes", notes)
    document.set_key_if_not_none("part_issue", part_issue)
    document.set_key_if_not_none("part_page_end", part_page_end)
    document.set_key_if_not_none("part_page_start", part_page_start)
    document.set_key_if_not_none("part_volume", part_volume)
    document.set_key_if_not_none("scholarly", scholarly)
    document.set_key_if_not_none("table_of_contents", table_of_contents)
    document.set_key_if_not_none("title", title)
    document.set_key_if_not_none("title_sub", title_sub)

    # subject
    subject = Subject()
    if subject_keywords:
        subject["keywords"] = subject_keywords
    if subject_names:
        subject["names"] = subject_names
    if subject_terms:
        subject["terms"] = subject_terms
    if subject:
        document["subjects"] = subject

    debug = True
    if debug:
        related_items_msg = "\t\t\t\t\t\t"
        if is_part_of_type:
            related_items_msg = "\tis_part_of: {} ".format(is_part_of_type)
        print "{}\t->\titem: {} {}\t:\t{}\t:\t{}".format(sum_type, rec_type, related_items_msg, rec_id, title)

    return document


def extract_convert_langstrings(sum_doc, sum_key, main_language):
    if sum_key in sum_doc:
        langstrings = []
        for value in sum_doc[sum_key]:
            langstrings.append({"language": main_language, "value": value})
        return langstrings


def extract_convert_add_classifications(sum_doc, document, sum_key, authority_id):
    classificiations = extract_value(sum_doc, sum_key, True)
    if classificiations:
        results = []
        for classification in classificiations:
            if classification:
                collection = Collection()
                collection["autority"] = {"id": authority_id}
                collection["id"] = classification
                results.append(collection)
        if results:
            document.add_items_to_key(results, "classificiations")


def extract_convert_identifiers(sum_doc):
    has_isbn = False
    has_eissn = False
    identifiers_item = []
    identifiers_is_part_of = []
    for sum_key in summon_identifier_type_to_metajson_identifier_type:
        if sum_key in sum_doc:
            for id_value in sum_doc[sum_key]:
                id_type = summon_identifier_type_to_metajson_identifier_type[sum_key]
                if id_type == "issn":
                    identifiers_is_part_of.append(metajson.create_identifier(id_type, id_value))
                elif id_type == "eissn":
                    has_eissn = True
                    identifiers_is_part_of.append(metajson.create_identifier(id_type, id_value))
                elif id_type == "isbn":
                    has_isbn = True
                    identifiers_is_part_of.append(metajson.create_identifier(id_type, id_value))
                else:
                    identifiers_item.append(metajson.create_identifier(id_type, id_value))
    return identifiers


def extract_contributors(sum_doc):
    contributors = []
    contributors.extend(convert_contributors(sum_doc, "Author_xml", "AuthorAffiliation_xml", "person", "aut"))
    contributors.extend(convert_contributors(sum_doc, "CorporateAuthor_xml", None, "orgunit", "aut"))
    contributors.extend(convert_contributors(sum_doc, "DissertationAdvisor_xml", None, "person", "ths"))
    contributors.extend(convert_contributors(sum_doc, "DissertationSchool_xml", None, "orgunit", "dgg"))
    contributors.extend(convert_contributors(sum_doc, "Distribution", None, None, "dst"))
    contributors.extend(convert_contributors(sum_doc, "Editor_xml", None, "person", "edt"))
    contributors.extend(convert_contributors(sum_doc, "MeetingName", None, "event", "aut"))
    return contributors


def convert_contributors(sum_doc, sum_authors_key, sum_affiliations_key, contributor_type, role):
    contributors = []
    if sum_authors_key in sum_doc:
        sum_authors = sum_doc[sum_authors_key]
        if sum_authors:
            affiliations_dict = {}
            if sum_affiliations_key in sum_doc:
                sum_affiliations = sum_doc[sum_affiliations_key]
                if sum_affiliations:
                    for index, affiliation in enumerate(sum_affiliations):
                        affiliations_dict[index + 1] = affiliation

            for author in sum_authors:
                contributor = Contributor()
                if "surname" in author and "givenname" in author:
                    contributor.set_key_if_not_none("name_family", author["surname"])
                    contributor.set_key_if_not_none("name_given", author["givenname"])
                    contributor["type"] = "person"
                    if role:
                        contributor["role"] = role
                else:
                    formatted_name = ""
                    if "fullname" in author:
                        formatted_name = author["fullname"]
                    elif "name" in author:
                        formatted_name = author["name"]

                    contributor = contributor_service.convert_formatted_name_to_contributor(formatted_name, contributor_type, role)
                if "sequence" in author and author["sequence"] in affiliations_dict:
                    contributor["affiliation"] = affiliations_dict[author["sequence"]]

                if contributor:
                    contributors.append(contributor)

    return contributors


def extract_date_issued(sum_doc):
    publication_date_xml = extract_value(sum_doc, "PublicationDate_xml", True)
    if publication_date_xml:
        date_dict = {}
        for item in publication_date_xml:
            if "year" in item:
                date_dict["year"] = item["year"]
            if "month" in item:
                date_dict["month"] = item["month"]
            if "day" in item:
                date_dict["day"] = item["day"]

        date = ""
        if "year" in date_dict:
            date += date_dict["year"]
        if "month" in date_dict:
            date += "-" + date_dict["month"]
        if "day" in date_dict:
            date += "-" + date_dict["day"]

        return date


def extract_value(sum_doc, key, as_list=False):
    if key in sum_doc:
        if as_list:
            return sum_doc[key]
        else:
            return sum_doc[key][0]


def extract_boolean_value(sum_doc, key):
    if key in sum_doc:
        return sum_doc[key][0] == "true"
