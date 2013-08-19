#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import QName
from biblib import metajson
from biblib.metajson import Document
from biblib.metajson import Resource
from biblib.metajson import Creator
from biblib.metajson import Person
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Event
from biblib.services import creator_service
from biblib.services import language_service
from biblib.util import constants

part_fields = ["part_chapter_number", "part_chapter_title", "part_chronology", "part_column", "part_issue", "part_month", "part_name", "part_number", "part_page_end", "part_page_start", "part_paragraph", "part_quarter", "part_season", "part_section", "part_session", "part_track", "part_unit", "part_volume", "part_week"]

mods_genre_eurepo_to_metajson_document_type = {
    # info:eu-repo/semantics
    "info:eu-repo/semantics/annotation": "Annotation",
    "info:eu-repo/semantics/article": "JournalArticle",
    "info:eu-repo/semantics/bachelorThesis": "MasterThesis",
    "info:eu-repo/semantics/book": "Book",
    "info:eu-repo/semantics/bookPart": "BookPart",
    "info:eu-repo/semantics/bookReview": "BookReview",
    "info:eu-repo/semantics/conferenceContribution": "ConferenceContribution",
    "info:eu-repo/semantics/conferenceItem": "ConferenceContribution",
    "info:eu-repo/semantics/conferenceObject": "ConferenceContribution",
    "info:eu-repo/semantics/conferencePaper": "ConferencePaper",
    "info:eu-repo/semantics/conferencePoster": "ConferencePoster",
    "info:eu-repo/semantics/conferenceProceedings": "ConferenceProceedings",
    "info:eu-repo/semantics/contributionToPeriodical": "ContributionToPeriodical",
    "info:eu-repo/semantics/doctoralThesis": "DoctoralThesis",
    "info:eu-repo/semantics/lecture": "ConferenceContribution",
    "info:eu-repo/semantics/masterThesis": "MasterThesis",
    "info:eu-repo/semantics/other": "Document",
    "info:eu-repo/semantics/patent": "Patent",
    "info:eu-repo/semantics/preprint": "Preprint",
    "info:eu-repo/semantics/report": "Report",
    "info:eu-repo/semantics/reportPart": "ReportPart",
    "info:eu-repo/semantics/researchProposal": "Document",
    "info:eu-repo/semantics/review": "BookReview",
    "info:eu-repo/semantics/studentThesis": "MasterThesis",
    "info:eu-repo/semantics/technicalDocumentation": "Document",
    "info:eu-repo/semantics/workingPaper": "WorkingPaper",
    # not registered info:eu-repo/semantics types
    "info:eu-repo/semantics/audiovisual": "Audiovisual",
    "info:eu-repo/semantics/interview": "Interview",
    "info:eu-repo/semantics/map": "Map",
    "info:eu-repo/semantics/periodicalIssue": "PeriodicalIssue",
    "info:eu-repo/semantics/professoralThesis": "ProfessoralThesis",
    "info:eu-repo/semantics/series": "Series",
    "info:eu-repo/semantics/unspecified": "Document",
    "info:eu-repo/semantics/website": "Website",
    "info:eu-repo/semantics/websiteContribution": "WebsiteContribution"
}

mods_genre_eprint_to_metajson_document_type = {
    # http://purl.org/eprint/type/
    "http://purl.org/eprint/type/Book": "Book",
    "http://purl.org/eprint/type/BookItem": "BookPart",
    "http://purl.org/eprint/type/BookReview": "BookReview",
    "http://purl.org/eprint/type/ConferenceItem": "ConferenceContribution",
    "http://purl.org/eprint/type/ConferencePaper": "ConferencePaper",
    "http://purl.org/eprint/type/ConferencePoster": "ConferencePoster",
    "http://purl.org/eprint/type/JournalArticle": "JournalArticle",
    "http://purl.org/eprint/type/JournalItem": "PeriodicalIssue",
    "http://purl.org/eprint/type/NewsItem": "ContributionToPeriodical",
    "http://purl.org/eprint/type/Patent": "Patent",
    "http://purl.org/eprint/type/Report": "Report",
    "http://purl.org/eprint/type/SubmittedJournalArticle": "Preprint",
    "http://purl.org/eprint/type/Thesis": "DoctoralThesis",
    "http://purl.org/eprint/type/WorkingPaper": "WorkingPaper"
}

mods_genre_marcgt_to_metajson_document_type = {
    # marcgt
    "abstract or summary": "Book",
    "article": "JournalArticle",
    "atlas": "Map",
    "autobiography": "Book",
    "bibliography": "Book",
    "biography": "Book",
    "book": "Book",
    "conference publication": "ConferenceProceedings",
    "catalog": "Book",
    "chart": "Map",
    "comic strip": "Book",
    "database": "Document",
    "dictionary": "Book",
    "directory": "Book",
    "drama": "Book",
    "encyclopedia": "Book",
    "essay": "Book",
    "festschrift": "Book",
    "fiction": "Book",
    "folktale": "Book",
    "globe": "Map",
    "graphic": "Map",
    "handbook": "Book",
    "history": "Book",
    "humor, satire": "Book",
    "index": "Book",
    "instruction": "Book",
    "issue": "PeriodicalIssue",
    "interview": "Interview",
    "journal": "journal",
    "kit": "Book",
    "language instruction": "Audiovisual",
    "law report or digest": "Annotation",
    "legislation": "Annotation",
    "letter": "Preprint",
    "loose-leaf": "Periodical",
    "map": "Map",
    "motion picture": "Audiovisual",
    "memoir": "Book",
    "newspaper": "Newspaper",
    "novel": "Book",
    "numeric data": "Book",
    "online system or service": "Website",
    "patent": "Patent",
    "periodical": "Periodical",
    "picture": "Map",
    "poetry": "Book",
    "programmed text": "Book",
    "rehearsal": "Book",
    "remote sensing image": "Map",
    "report": "Report",
    "reporting": "Report",
    "review": "BookReview",
    "series": "Series",
    "short story": "Book",
    "slide": "Audiovisual",
    "sound": "Audiovisual",
    "speech": "ConferenceContribution",
    "statistics": "Book",
    "survey of literature": "BookReview",
    "technical drawing": "Map",
    "technical report": "Report",
    "thesis": "DoctoralThesis",
    "treaty": "Book",
    "videorecording": "Audiovisual",
    "web site": "Website",
    "websiteContribution": "websiteContribution"
}


def register_namespaces():
    for key in constants.xmlns_map:
        ET.register_namespace(key, constants.xmlns_map[key])


def prefixtag(ns_prefix, tagname):
    if tagname:
        if ns_prefix and ns_prefix in constants.xmlns_map:
            return str(QName(constants.xmlns_map[ns_prefix], tagname))
        else:
            return tagname


def mods_xmletree_to_metajson_list(mods_root, source, only_first_record):
    if mods_root is not None:
        if mods_root.tag.endswith("mods"):
            yield mods_xmletree_to_metajson(mods_root, source)
        elif mods_root.tag.endswith("modsCollection"):
            mods_list = mods_root.findall("mods")
            if mods_list:
                for mods in mods_list:
                    yield mods_xmletree_to_metajson(mods, source)


def mods_xmletree_to_metajson(mods, source):
    document = Document()
    is_part_of = None
    review_of = None
    series = None

    # source
    if source is not None:
        document["rec_source"] = source

    # rec_type, rec_class, genres
    document.update(extract_class_type_genres(mods))
    rec_type = document["rec_type"]

    # rec_id, identifiers
    identifiers = convert_mods_identifiers(mods.findall(prefixtag("mods", "identifier")))
    if identifiers:
        document["identifiers"] = identifiers
        document["rec_id"] = "{}:{}".format(identifiers[0]["id_type"],identifiers[0]["value"])

    # originInfo issuance

    # relatedItems
    related_items = mods.findall(prefixtag("mods", "relatedItem"))
    related_item_host = None
    related_item_original = None
    related_item_series = None
    if related_items:
        print "0"
        for related_item in related_items:
            # host -> is_part_of
            if related_item.get("type") == "host":
                related_item_host = related_item
            elif related_item.get("type") == "original" or related_item.get("type") == "reviewOf":
                related_item_original = related_item
            elif related_item.get("type") == "series":
                related_item_series = related_item

        if related_item_host is not None:
            print "a"
            is_part_of = mods_xmletree_to_metajson(related_item_host, None)
            print is_part_of
            for key in part_fields:
                print "b " + key
                if key in is_part_of:
                    print "c " + key
                    document[key] = is_part_of[key]
                    del is_part_of[key]

        if related_item_original is not None:
            review_of = Document()

        if related_item_series is not None:
            series = Document()

    # title
    document.update(convert_mods_titleinfos(mods.findall(prefixtag("mods", "titleInfo"))))

    # creators
    creators = extract_creators(mods)
    if creators:
        #print creators
        document["creators"] = creators

    # languages
    mods_languages = mods.findall(prefixtag("mods", "language"))
    if mods_languages is not None:
        languages = []
        for mods_language in mods_languages:
            language = convert_language(mods_language)
            if language is not None:
                languages.append(language)
        if languages:
            document["languages"] = languages

    # abstract
    mods_abstracts = mods.findall(prefixtag("mods", "abstract"))
    if mods_abstracts is not None:
        abstracts = []
        for mods_abstract in mods_abstracts:
            abstracts.append(convert_string_lang(mods_abstract))
        if abstracts:
            document["descriptions"] = abstracts

    # subject
    mods_subjects = mods.findall(prefixtag("mods", "subject"))
    if mods_subjects is not None:
        document.update(convert_subjects(mods_subjects))

    # classification
    mods_classifications = mods.findall(prefixtag("mods", "classification"))
    if mods_classifications is not None:
        document.update(convert_classifications(mods_classifications))

    # part
    mods_parts = mods.findall(prefixtag("mods", "part"))
    if mods_parts is not None:
        parts = convert_parts(mods_parts)
        print parts
        document.update(parts)

    # relatedItem
    if is_part_of is not None:
        document["is_part_ofs"] = [is_part_of]
    if review_of is not None:
        document["review_ofs"] = [review_of]
    if series is not None:
        document["seriess"] = [series]

    # root originInfo dates
    root_dates = extract_dates_from_origininfo(mods.find(prefixtag("mods", "originInfo")))
    if root_dates:
        document.update(root_dates)

    # relatedItem host originInfo dates
    if related_item_host is not None and rec_type in ["Article", "JournalArticle", "MagazineArticle", "NewspaperArticle", "Annotation", "InterviewArticle", "BookReview", "ArticleReview", "PeriodicalIssue"]:
        is_part_of_dates = extract_dates_from_origininfo(related_item_host.find(prefixtag("mods", "originInfo")))
        if is_part_of_dates:
            document.update(is_part_of_dates)

    return document


def extract_class_type_genres(mods):
    genres_dict = {}
    genres_dict["genres"] = []

    mods_genres = mods.findall(prefixtag("mods", "genre"))
    if mods_genres:
        for mods_genre in mods_genres:
            if mods_genre.text.startswith("info:eu-repo/semantics/"):
                genres_dict["eurepo"] = mods_genre.text
            elif mods_genre.text.startswith("http://purl.org/eprint/type/"):
                genres_dict["eprint"] = mods_genre.text
            elif "marcgt" not in genres_dict and mods_genre.text in mods_genre_marcgt_to_metajson_document_type:
                genres_dict["marcgt"] = mods_genre.text
            else:
                genre = {}
                if mods_genre.get("authority"):
                    genre["authority"] = mods_genre.get("authority")
                genre["value"] = mods_genre.text
                genres_dict["genres"].append(genre)

    result = {}
    result["rec_class"] = "Document"
    result["rec_type"] = None
    if "eurepo" in genres_dict and genres_dict["eurepo"] in mods_genre_eurepo_to_metajson_document_type:
        result["rec_type"] = mods_genre_eurepo_to_metajson_document_type[genres_dict["eurepo"]]
    elif "eprint" in genres_dict and genres_dict["eprint"] in mods_genre_eprint_to_metajson_document_type:
        result["rec_type"] = mods_genre_eprint_to_metajson_document_type[genres_dict["eprint"]]
    elif "marcgt" in genres_dict and genres_dict["marcgt"] in mods_genre_marcgt_to_metajson_document_type:
        result["rec_type"] = mods_genre_marcgt_to_metajson_document_type[genres_dict["marcgt"]]
    else:
        result["rec_type"] = "Document"

    if genres_dict["genres"]:
        result["genres"] = genres_dict["genres"]

    #print result
    return result


def convert_mods_identifiers(mods_identifiers):
    if mods_identifiers:
        results = []
        for mods_identifier in mods_identifiers:
            identifier = convert_mods_identifier(mods_identifier)
            if identifier:
                results.append(identifier)
        return results


def convert_mods_identifier(mods_identifier):
    if mods_identifier is not None:
        return metajson.create_identifier(mods_identifier.get("type"), mods_identifier.text)


def convert_mods_titleinfos(mods_titleinfos):
    result = {}
    if mods_titleinfos is not None:
        for mods_titleinfo in mods_titleinfos:
            title_dict = convert_mods_titleinfo(mods_titleinfo)
            if title_dict["type"] is None:
                del title_dict["type"]
                result.update(title_dict)
            elif title_dict["type"] == "abbreviated":
                del title_dict["type"]
                result["title_abbreviated"] = title_dict
            elif title_dict["type"] == "alternative":
                del title_dict["type"]
                result["title_alternative"] = title_dict
            elif title_dict["type"] == "translated":
                del title_dict["type"]
                result["title_translated"] = title_dict
            elif title_dict["type"] == "uniform":
                del title_dict["type"]
                result["title_uniform"] = title_dict
            else:
                print "error convert_mods_titleinfos unknown type: {}".format(title_dict["type"])

    return result


def convert_mods_titleinfo(mods_titleinfo):
    if mods_titleinfo is not None:
        title_dict = {}
        title_dict["type"] = mods_titleinfo.get("type")
        if mods_titleinfo.find(prefixtag("mods", "title")) is not None:
            title_dict["title"] = mods_titleinfo.find(prefixtag("mods", "title")).text.strip()
        if mods_titleinfo.find(prefixtag("mods", "nonSort")) is not None:
            title_dict["title_non_sort"] = mods_titleinfo.find(prefixtag("mods", "nonSort")).text.strip()
        if mods_titleinfo.find(prefixtag("mods", "subTitle")) is not None:
            title_dict["title_sub"] = mods_titleinfo.find(prefixtag("mods", "subTitle")).text.strip()
        if mods_titleinfo.find(prefixtag("mods", "partNumber")) is not None:
            title_dict["part_number"] = mods_titleinfo.find(prefixtag("mods", "partNumber")).text.strip()
        if mods_titleinfo.find(prefixtag("mods", "partName")) is not None:
            title_dict["part_name"] = mods_titleinfo.find(prefixtag("mods", "partName")).text.strip()

        #print title_dict
        return title_dict


def extract_creators(mods):
    mods_names = mods.findall(prefixtag("mods", "name"))
    if mods_names:
        extension = mods.find(prefixtag("mods", "extension"))
        dai_dict = None
        if extension is not None:
            dai_dict = convert_mods_dailist_to_dict(extension.find(prefixtag("dai", "daiList")))

        result = []
        for mods_name in mods_names:
            creator = convert_mods_name_to_creator(mods_name, dai_dict)
            if creator is not None:
                result.append(creator)
        return result


def convert_mods_dailist_to_dict(dai_list):
    if dai_list is not None:
        dai_identifiers = dai_list.findall(prefixtag("dai", "identifier"))
        if dai_identifiers:
            result = {}
            for dai_identifier in dai_identifiers:
                result[dai_identifier.get("IDref")] = {"authority": dai_identifier.get("authority"), "value": dai_identifier.text}
            #print result
            return result


def convert_mods_name_to_creator(mods_name, dai_dict):
    if mods_name is not None:
        creator = Creator()
        # extract properties
        name_type = mods_name.get("type")
        name_id = mods_name.get("ID")
        name_parts = mods_name.findall(prefixtag("mods", "namePart"))
        name_affiliations = mods_name.findall(prefixtag("mods", "affiliation"))
        name_roleterm = None
        name_role = mods_name.find(prefixtag("mods", "role"))
        if name_role is not None:
            name_roleterm = name_role.find(prefixtag("mods", "roleTerm"))
        name_descriptions = mods_name.findall(prefixtag("mods", "description"))

        # affiliation
        affiliation = None
        if name_affiliations:
            affiliation = Orgunit()
            affiliation["name"] = name_affiliations[0].text.strip()

        #agent_rec_id, agent_identifiers, affiliation_rec_id
        agent_rec_id = None
        agent_identifiers = None
        if name_id is not None:
            spire_name_ids = name_id.split("_-_")
            if spire_name_ids and len(spire_name_ids) >= 4:
                agent_rec_id = spire_name_ids[2].replace("__", "/")
                affiliation_rec_id = spire_name_ids[4]
                if affiliation_rec_id:
                    if not affiliation:
                        affiliation = Orgunit()
                    affiliation["rec_id"] = affiliation_rec_id.replace("__", "/")
            elif dai_dict is not None and name_id in dai_dict:
                # identifiers
                id_value = dai_dict[name_id]["authority"] + "/" + dai_dict[name_id]["value"]
                agent_identifiers = [metajson.create_identifier("uri", id_value)]
                # rec_id
                agent_rec_id = dai_dict[name_id]["value"]

        if name_type == "personal":
            # print "personal"
            person = Person()

            if agent_rec_id:
                person["rec_id"] = agent_rec_id
            if agent_identifiers:
                person["identifiers"] = agent_identifiers

            if name_parts:
                for name_part in name_parts:
                    if name_part.get("type") == "given":
                        person["name_given"] = name_part.text.strip()
                    elif name_part.get("type") == "family":
                        person["name_family"] = name_part.text.strip()
                    elif name_part.get("type") == "date":
                        date = name_part.text.replace("(", "").replace(")", "").strip()
                        minus_index = date.find("-")
                        if minus_index == -1:
                            person["date_birth"] = date
                        else:
                            person["date_birth"] = date[:minus_index]
                            person["date_death"] = date[minus_index+1:]
                    elif name_part.get("termsOfAddress") == "date":
                        person["name_terms_of_address"] = name_part.text

            creator["agent"] = person

        elif name_type == "corporate":
            # print "corporate"
            orgunit = Orgunit()
            creator["agent"] = orgunit

            if name_parts:
                orgunit["name"] = name_parts[0].text.strip()

        elif name_type == "conference":
            # print "conference"
            event = Event()
            creator["agent"] = event

            if name_parts:
                for name_part in name_parts:
                    if name_part.get("type") is None:
                        event["title"] = name_part.text.strip()
                    elif name_part.get("type") == "termsOfAddress":
                        address = name_part.text.strip()
                        sep_index = address.find(";")
                        if sep_index == -1:
                            event["place"] = address
                        else:
                            event["place"] = address[:sep_index]
                            event["country"] = address[sep_index+1:]
                    elif name_part.get("type") == "date":
                        date = name_part.text.strip()
                        slash_index = date.find("/")
                        if slash_index == -1:
                            event["date_start"] = date
                        else:
                            event["date_start"] = date[:slash_index]
                            event["date_end"] = date[slash_index+1:]

        if affiliation:
            creator["affiliation"] = affiliation

        if name_roleterm is not None:
            creator["role"] = convert_mods_name_roleterm(name_roleterm)

        #print name_type, name_id, name_parts, name_affiliations, name_roleterm, name_descriptions
        return creator


def convert_mods_name_roleterm(mods_roleterm):
    if mods_roleterm is not None:
        authority = mods_roleterm.get("authority")
        term_type = mods_roleterm.get("type")
        value = mods_roleterm.text.strip()
        # print authority, term_type, value
        if not value:
            # default creator role
            return "cre"
        else:
            if authority == "marcrelator":
                if term_type == "code":
                    return value
                elif value in creator_service.role_text_to_role_code:
                    return creator_service.role_text_to_role_code[value]
                else:
                    return "cre"
            elif authority == "unimarc" and value in creator_service.role_unimarc_to_role_code:
                return creator_service.role_unimarc_to_role_code[value]
            else:
                return "cre"
    else:
        return "cre"


def extract_dates_from_origininfo(origininfo):
    if origininfo is not None:
        result = {}
        date_issued = convert_date(origininfo.find(prefixtag("mods", "dateIssued")))
        if date_issued:
            result["date_issued"] = date_issued
        date_created = convert_date(origininfo.find(prefixtag("mods", "dateCreated")))
        if date_created:
            result["date_created"] = date_created
        date_captured = convert_date(origininfo.find(prefixtag("mods", "dateCaptured")))
        if date_captured:
            result["date_captured"] = date_captured
        date_valid = convert_date(origininfo.find(prefixtag("mods", "dateValid")))
        if date_valid:
            result["date_valid"] = date_valid
        date_modified = convert_date(origininfo.find(prefixtag("mods", "dateModified")))
        if date_modified:
            result["date_modified"] = date_modified
        date_copyrighted = convert_date(origininfo.find(prefixtag("mods", "copyrightDate")))
        if date_copyrighted:
            result["date_copyrighted"] = date_copyrighted
        date_other = convert_date(origininfo.find(prefixtag("mods", "dateOther")))
        if date_other:
            result["date_other"] = date_other
        return result


def convert_date(mods_date):
    if mods_date is not None:
        encoding = mods_date.get("encoding")
        #point = mods_date.get("point")
        #key_date = mods_date.get("keyDate")
        #qualifier = mods_date.get("qualifier")
        value = mods_date.text.strip()
        if encoding == "iso8601":
            return value
        else:
            # todo
            return value


def convert_language(mods_language):
    if mods_language is not None:
        mods_terms = mods_language.findall(prefixtag("mods", "languageTerm"))
        if mods_terms is not None:
            for mods_term in mods_terms:
                if mods_term.get("type") == "code":
                    if mods_term.get("authority") == "rfc3066":
                        return mods_term.text
                    else:
                        # todo for iso639-2b and other authority
                        pass
                else:
                    # todo for natural language like "French"
                    pass


def convert_string_lang(mods_string_lang):
    if mods_string_lang is not None:
        lang = mods_string_lang.get("lang")
        value = mods_string_lang.text.strip()
        if value is not None:
            result = {"value": value}
            if lang is not None:
                result["language"] = lang
            return result


def convert_subjects(mods_subjects):
    if mods_subjects is not None:
        subjects = []
        keywords_dict = {}
        for mods_subject in mods_subjects:
            if mods_subject is not None:
                mods_subject_authority = mods_subject.get("authority")
                mods_subject_lang = mods_subject.get("lang")
                if mods_subject_lang is not None and mods_subject_lang not in keywords_dict:
                    keywords_dict[mods_subject_lang] = []
                elif mods_subject_lang is None:
                    keywords_dict[constants.LANGUAGE_UNDETERMINED] = []
                if mods_subject_authority is None:
                    # it's a keyword
                    mods_topics = mods_subject.findall(prefixtag("mods", "topic"))
                    if mods_topics is not None:
                        for mods_topic in mods_topics:
                            if mods_topic.text is not None:
                                terms = None
                                if mods_topic.text.find(";") != -1:
                                    terms = mods_topic.text.split(";")
                                elif mods_topic.text.find(",") != -1:
                                    terms = mods_topic.text.split(",")
                                else:
                                    terms = [mods_topic.text]
                            if terms is not None:
                                for term in terms:
                                    if mods_subject_lang is not None:
                                        keywords_dict[mods_subject_lang].append(term.strip())
                                    else:
                                        keywords_dict[constants.LANGUAGE_UNDETERMINED].append(term.strip())
        result = {}
        if subjects:
            result["subjects"] = subjects
        if keywords_dict:
            result["keywords"] = keywords_dict
        return result


def convert_classifications(mods_classifications):
    if mods_classifications is not None:
        classifications_dict = {}
        peer_review = False
        peer_review_geo = []
        for mods_classification in mods_classifications:
            if mods_classification is not None:
                mods_classification_authority = mods_classification.get("authority")
                #mods_classification_lang = mods_classification.get("lang")
                if mods_classification.text is not None:
                    if mods_classification_authority is not None:
                        if mods_classification_authority == "peer-review":
                            if mods_classification.text == "yes":
                                peer_review = True
                        else:
                            if mods_classification_authority not in classifications_dict:
                                classifications_dict[mods_classification_authority] = []
                            classifications_dict[mods_classification_authority].append(mods_classification.text.strip())
                    elif mods_classification_authority is None:
                        if constants.CLASSIFICATION_UNDETERMINED not in classifications_dict:
                            classifications_dict[constants.CLASSIFICATION_UNDETERMINED] = []
                        classifications_dict[constants.CLASSIFICATION_UNDETERMINED].append(mods_classification.text.strip())
        result = {}
        if classifications_dict:
            result["classifications"] = classifications_dict
        if peer_review:
            result["peer_review"] = peer_review
        if peer_review_geo:
            result["peer_review_geo"] = peer_review_geo
        return result


def convert_parts(mods_parts):
    print "convert_parts"
    if mods_parts is not None:
        print "convert_parts 0"
        parts_dict = {}
        for mods_part in mods_parts:
            print "convert_parts 1"
            if mods_part is not None:
                # detail
                print "convert_parts 2"
                mods_part_details = mods_part.findall(prefixtag("mods", "detail"))
                if mods_part_details is not None:
                    print "convert_parts 3"
                    for mods_part_detail in mods_part_details:
                        print "convert_parts 4"
                        mods_part_detail_type = mods_part_detail.get("type")
                        mods_part_detail_number = mods_part_detail.find(prefixtag("mods", "number"))
                        if mods_part_detail_type is not None and mods_part_detail_number is not None and mods_part_detail_number.text is not None:
                            if mods_part_detail_type == "volume":
                                print "volume"
                                parts_dict["part_volume"] = mods_part_detail_number.text
                            elif mods_part_detail_type == "issue":
                                print "issue"
                                parts_dict["part_issue"] = mods_part_detail_number.text

                # extent
                mods_part_extents = mods_part.findall(prefixtag("mods", "extent"))
                if mods_part_extents is not None:
                    print "convert_parts 10"
                    for mods_part_extent in mods_part_extents:
                        mods_part_extent_unit = mods_part_extent.get("unit")
                        mods_part_extent_start = mods_part_extent.find(prefixtag("mods", "start"))
                        mods_part_extent_end = mods_part_extent.find(prefixtag("mods", "end"))
                        if mods_part_extent_unit is not None and (mods_part_extent_start is not None or mods_part_extent_end is not None):
                            if mods_part_extent_unit == "page" or mods_part_extent_unit == "pages":
                                if mods_part_extent_start is not None and mods_part_extent_start.text is not None:
                                    parts_dict["part_page_start"] = mods_part_extent_start.text
                                if mods_part_extent_end is not None and mods_part_extent_end.text is not None:
                                    parts_dict["part_page_end"] = mods_part_extent_end.text

        return parts_dict
