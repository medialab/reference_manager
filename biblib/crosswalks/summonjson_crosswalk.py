#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Collection
from biblib.metajson import Document
from biblib.metajson import Creator
from biblib.metajson import Subject
from biblib.services import creator_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import constants
from biblib.util import string


summon_document_type_to_metajson_document_type = {
    "Audio Recording": constants.DOC_TYPE_AUDIORECORDING,
    "Book": constants.DOC_TYPE_BOOK,
    "Book Chapter": constants.DOC_TYPE_BOOKPART,
    "Book Review": constants.DOC_TYPE_BOOKREVIEW,
    "Case": constants.DOC_TYPE_LEGALCASE,
    "Computer File": constants.DOC_TYPE_SOFTWARE,
    "Conference Proceeding": constants.DOC_TYPE_CONFERENCEPROCEEDINGS,
    "Data Set": constants.DOC_TYPE_DATASETQUANTI,
    "Dissertation": constants.DOC_TYPE_DISSERTATION,
    "eBook": constants.DOC_TYPE_EBOOK,
    "Image": constants.DOC_TYPE_IMAGE,
    "Journal": constants.DOC_TYPE_JOURNAL,
    "Journal Article": constants.DOC_TYPE_JOURNALARTICLE,
    "Magazine": constants.DOC_TYPE_MAGAZINE,
    "Magazine Article": constants.DOC_TYPE_MAGAZINEARTICLE,
    "Manuscript": constants.DOC_TYPE_MANUSCRIPT,
    "Map": constants.DOC_TYPE_MAP,
    "Music Recording": constants.DOC_TYPE_MUSICRECORDING,
    "Music Score": constants.DOC_TYPE_MUSICALSCORE,
    "Newspaper": constants.DOC_TYPE_NEWSPAPER,
    "Newspaper Article": constants.DOC_TYPE_NEWSPAPERARTICLE,
    "Patent": constants.DOC_TYPE_PATENT,
    "Poster": constants.DOC_TYPE_CONFERENCEPOSTER,
    "Realia": constants.DOC_TYPE_PHYSICALOBJECT,
    "Reference": constants.DOC_TYPE_DICTIONARY,
    "Report": constants.DOC_TYPE_REPORT,
    "Thesis": constants.DOC_TYPE_DOCTORALTHESIS,
    "Video Recording": constants.DOC_TYPE_VIDEORECORDING,
    "Web Resource": constants.DOC_TYPE_WEBSITE
}


summon_document_type_to_metajson_document_is_part_of_type = {
    "Book Chapter": constants.DOC_TYPE_BOOK,
    "Book Review": constants.DOC_TYPE_JOURNAL,
    "Journal Article": constants.DOC_TYPE_JOURNAL,
    "Magazine Article": constants.DOC_TYPE_MAGAZINE,
    "Newspaper Article": constants.DOC_TYPE_NEWSPAPER
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


def summonjson_to_metajson_list(summon_result, source, only_first_record=False):
    if "documents" in summon_result:
        return summonjson_document_list_to_metajson_list(summon_result["documents"], source, only_first_record)


def summonjson_document_list_to_metajson_list(sum_doc_list, source, only_first_record=False):
    for sum_doc in sum_doc_list:
        yield summonjson_document_to_metajson(sum_doc, source)


def summonjson_document_to_metajson(sum_doc, source):
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
    creators = extract_creators(sum_doc)
    copyright_statement = extract_value(sum_doc, "Copyright")
    database_id = extract_value(sum_doc, "DBID")
    print "DBID: {}".format(database_id)
    database_xml = extract_dict_value(sum_doc, "Database_xml")
    print "database_xml: {}".format(database_xml)
    date_issued = extract_date_issued(sum_doc)
    degree = extract_value(sum_doc, "DissertationDegree")
    descriptions = extract_convert_languageValues(sum_doc, "Abstract", main_language)
    edition = extract_value(sum_doc, "Edition")
    extent_pages = extract_value(sum_doc, "PageCount")
    genre = extract_value(sum_doc, "Genre")
    is_part_of_edition = extract_value(sum_doc, "PublicationEdition")
    is_part_of_title = extract_value(sum_doc, "PublicationTitle")
    is_part_of_title_sub = extract_value(sum_doc, "PublicationSubtitle")
    notes = extract_convert_languageValues(sum_doc, "Notes", main_language)
    part_issue = extract_value(sum_doc, "Issue")
    part_page_end = extract_value(sum_doc, "EndPage")
    part_page_start = extract_value(sum_doc, "StartPage")
    part_volume = extract_value(sum_doc, "Volume")
    peer_reviewed = extract_boolean_value(sum_doc, "IsPeerReviewed")
    publisher = extract_value(sum_doc, "Publisher")
    publication_place = extract_value(sum_doc, "PublicationPlace")
    scholarly = extract_boolean_value(sum_doc, "IsScholarly")
    series_title = extract_value(sum_doc, "PublicationSeriesTitle")
    subject_keywords = extract_value(sum_doc, "Keywords", True)
    subject_agents = convert_creators(sum_doc, "RelatedPersons", None, "person", None)
    subject_topics = extract_value(sum_doc, "SubjectTerms", True)
    table_of_contents = extract_convert_languageValues(sum_doc, "TableOfContents", main_language)
    title = string.strip_html_tags(extract_value(sum_doc, "Title"))
    title_sub = string.strip_html_tags(extract_value(sum_doc, "Subtitle"))

    # identifiers
    has_isbn = False
    has_eissn = False
    identifiers_item = []
    is_part_of_identifiers = []
    for sum_key in summon_identifier_type_to_metajson_identifier_type:
        if sum_key in sum_doc:
            for id_value in sum_doc[sum_key]:
                id_type = summon_identifier_type_to_metajson_identifier_type[sum_key]
                if id_type == "issn":
                    is_part_of_identifiers.append(metajson_service.create_identifier(id_type, id_value))
                elif id_type == "eissn":
                    has_eissn = True
                    is_part_of_identifiers.append(metajson_service.create_identifier(id_type, id_value))
                elif id_type == "isbn":
                    has_isbn = True
                    is_part_of_identifiers.append(metajson_service.create_identifier(id_type, id_value))
                else:
                    identifiers_item.append(metajson_service.create_identifier(id_type, id_value))

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
        is_part_of.add_items_to_key(is_part_of_identifiers, "identifiers")
        is_part_of.set_key_if_not_none("peer_reviewed", peer_reviewed)
        is_part_of.set_key_if_not_none("publishers", [publisher])
        is_part_of.set_key_if_not_none("publication_places", [publication_place])
        is_part_of.set_key_if_not_none("title", is_part_of_title)
        is_part_of.set_key_if_not_none("title_sub", is_part_of_title_sub)

        document.add_items_to_key(identifiers_item, "identifiers")

        document.add_items_to_key([is_part_of], "is_part_ofs")
    else:
        document.set_key_if_not_none("peer_reviewed", peer_reviewed)
        document.set_key_if_not_none("publishers", [publisher])
        document.set_key_if_not_none("publication_places", [publication_place])
        document.add_items_to_key(is_part_of_identifiers, "identifiers")
        document.add_items_to_key(identifiers_item, "identifiers")

    # series
    if series_title:
        series = Document()
        series["rec_type"] = constants.DOC_TYPE_SERIES
        series.set_key_if_not_none("title", series_title)

        document.add_items_to_key([series], "seriess")

    # classificiations
    extract_convert_add_classifications(sum_doc, document, "DEWEY", "ddc")
    extract_convert_add_classifications(sum_doc, document, "Discipline", "discipline")
    extract_convert_add_classifications(sum_doc, document, "NAICS", "NAICS")

    # set properties
    document.set_key_if_not_none("creators", creators)
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

    # keywords, subjects
    subjects = []
    keywords = {main_language: []}
    if subject_keywords:
        keywords[main_language].extend(subject_keywords)
    if subject_topics:
        keywords[main_language].extend(subject_topics)
    if subject_agents:
        subject = Subject()
        subject["agents"] = subject_agents
        subjects.append(subject)
    if subjects:
        document["subjects"] = subjects
    if keywords[main_language]:
        document["keywords"] = keywords

    debug = True
    if debug:
        print "# Summon ContentType: {}".format(sum_type)
        metajson_service.pretty_print_document(document)
    return document


def extract_convert_languageValues(sum_doc, sum_key, main_language):
    if sum_key in sum_doc:
        languageValues = []
        for value in sum_doc[sum_key]:
            languageValues.append({"language": main_language, "value": value})
        return languageValues


def extract_convert_add_classifications(sum_doc, document, sum_key, authority_id):
    classificiations = extract_value(sum_doc, sum_key, True)
    if classificiations:
        if "classificiations" not in document:
            document["classificiations"] = {}
        if authority_id not in document["classificiations"]:
            document["classificiations"][authority_id] = []
        for classification in classificiations:
            if classification:
                document["classificiations"][authority_id].append(classification)


def extract_convert_identifiers(sum_doc):
    has_isbn = False
    has_eissn = False
    identifiers_item = []
    is_part_of_identifiers = []
    for sum_key in summon_identifier_type_to_metajson_identifier_type:
        if sum_key in sum_doc:
            for id_value in sum_doc[sum_key]:
                id_type = summon_identifier_type_to_metajson_identifier_type[sum_key]
                if id_type == "issn":
                    is_part_of_identifiers.append(metajson_service.create_identifier(id_type, id_value))
                elif id_type == "eissn":
                    has_eissn = True
                    is_part_of_identifiers.append(metajson_service.create_identifier(id_type, id_value))
                elif id_type == "isbn":
                    has_isbn = True
                    is_part_of_identifiers.append(metajson_service.create_identifier(id_type, id_value))
                else:
                    identifiers_item.append(metajson_service.create_identifier(id_type, id_value))
    return identifiers_item, is_part_of_identifiers


def extract_creators(sum_doc):
    creators = []
    creators.extend(convert_creators(sum_doc, "Author_xml", "AuthorAffiliation_xml", "person", "aut"))
    creators.extend(convert_creators(sum_doc, "CorporateAuthor_xml", None, "orgunit", "aut"))
    creators.extend(convert_creators(sum_doc, "DissertationAdvisor_xml", None, "person", "ths"))
    creators.extend(convert_creators(sum_doc, "DissertationSchool_xml", None, "orgunit", "dgg"))
    creators.extend(convert_creators(sum_doc, "Distribution", None, None, "dst"))
    creators.extend(convert_creators(sum_doc, "Editor_xml", None, "person", "pbd"))
    creators.extend(convert_creators(sum_doc, "MeetingName", None, "event", "aut"))
    return creators


def convert_creators(sum_doc, sum_authors_key, sum_affiliations_key, creator_type, role):
    creators = []
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
                creator = Creator()
                if "surname" in author and "givenname" in author:
                    creator.set_key_if_not_none("name_family", author["surname"])
                    creator.set_key_if_not_none("name_given", author["givenname"])
                    creator["type"] = "person"
                    if role:
                        creator["role"] = role
                else:
                    formatted_name = ""
                    if "fullname" in author:
                        formatted_name = author["fullname"]
                    elif "name" in author:
                        formatted_name = author["name"]

                    creator = creator_service.formatted_name_to_creator(formatted_name, creator_type, role)
                if "sequence" in author and author["sequence"] in affiliations_dict:
                    creator["affiliation"] = affiliations_dict[author["sequence"]]

                # todo : location dans le cas des DissertationSchool_xml
                if creator:
                    creators.append(creator)

    return creators


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
            return sum_doc[key][0].strip()


def extract_dict_value(sum_doc, key):
    if key in sum_doc:
        return sum_doc[key]


def extract_boolean_value(sum_doc, key):
    if key in sum_doc:
        return sum_doc[key][0] == "true"
