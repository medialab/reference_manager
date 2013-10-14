#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import QName

from biblib.metajson import Creator
from biblib.metajson import Document
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Resource
from biblib.metajson import Rights
from biblib.services import creator_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import constants

MODS_PART_FIELDS = ["part_chapter_number", "part_chapter_title", "part_chronology", "part_column", "part_issue", "part_month", "part_name", "part_number", "part_page_end", "part_page_start", "part_paragraph", "part_quarter", "part_season", "part_section", "part_session", "part_track", "part_unit", "part_volume", "part_week"]

MODS_DATE_FIELDS = []

MODS_ARTICLE_TYPES = ["Article", "JournalArticle", "MagazineArticle", "NewspaperArticle", "Annotation", "InterviewArticle", "BookReview", "ArticleReview", "PeriodicalIssue"]

MODS_GENRE_EUREPO_TO_METAJSON_DOCUMENT_TYPE = {
    # registered info:eu-repo/semantics types
    "info:eu-repo/semantics/annotation": constants.DOC_TYPE_ANNOTATIONARTICLE,
    "info:eu-repo/semantics/article": constants.DOC_TYPE_JOURNALARTICLE,
    "info:eu-repo/semantics/bachelorThesis": constants.DOC_TYPE_MASTERTHESIS,
    "info:eu-repo/semantics/book": constants.DOC_TYPE_BOOK,
    "info:eu-repo/semantics/bookPart": constants.DOC_TYPE_BOOKPART,
    "info:eu-repo/semantics/bookReview": constants.DOC_TYPE_BOOKREVIEW,
    "info:eu-repo/semantics/conferenceContribution": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "info:eu-repo/semantics/conferenceItem": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "info:eu-repo/semantics/conferenceObject": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "info:eu-repo/semantics/conferencePaper": constants.DOC_TYPE_CONFERENCEPAPER,
    "info:eu-repo/semantics/conferencePoster": constants.DOC_TYPE_CONFERENCEPOSTER,
    "info:eu-repo/semantics/conferenceProceedings": constants.DOC_TYPE_CONFERENCEPROCEEDINGS,
    "info:eu-repo/semantics/contributionToPeriodical": constants.DOC_TYPE_NEWSPAPERARTICLE,  # or DOC_TYPE_MAGAZINEARTICLE
    "info:eu-repo/semantics/doctoralThesis": constants.DOC_TYPE_DOCTORALTHESIS,
    "info:eu-repo/semantics/lecture": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "info:eu-repo/semantics/masterThesis": constants.DOC_TYPE_MASTERTHESIS,
    "info:eu-repo/semantics/other": constants.DOC_TYPE_UNPUBLISHEDDOCUMENT,
    "info:eu-repo/semantics/patent": constants.DOC_TYPE_PATENT,
    "info:eu-repo/semantics/preprint": constants.DOC_TYPE_PREPRINT,
    "info:eu-repo/semantics/report": constants.DOC_TYPE_REPORT,
    "info:eu-repo/semantics/reportPart": constants.DOC_TYPE_REPORTPART,
    "info:eu-repo/semantics/researchProposal": constants.DOC_TYPE_RESEARCHPROPOSAL,
    "info:eu-repo/semantics/review": constants.DOC_TYPE_BOOKREVIEW,
    "info:eu-repo/semantics/studentThesis": constants.DOC_TYPE_MASTERTHESIS,
    "info:eu-repo/semantics/technicalDocumentation": constants.DOC_TYPE_TECHREPORT,
    "info:eu-repo/semantics/workingPaper": constants.DOC_TYPE_WORKINGPAPER,
    # not registered info:eu-repo/semantics types
    "info:eu-repo/semantics/audiovisual": constants.DOC_TYPE_VIDEORECORDING,
    "info:eu-repo/semantics/interview": constants.DOC_TYPE_INTERVIEWARTICLE,
    "info:eu-repo/semantics/map": constants.DOC_TYPE_MAP,
    "info:eu-repo/semantics/periodicalIssue": constants.DOC_TYPE_PERIODICALISSUE,
    "info:eu-repo/semantics/professoralThesis": constants.DOC_TYPE_PROFESSORALTHESIS,
    "info:eu-repo/semantics/series": constants.DOC_TYPE_SERIES,
    "info:eu-repo/semantics/unspecified": constants.DOC_TYPE_UNPUBLISHEDDOCUMENT,
    "info:eu-repo/semantics/website": constants.DOC_TYPE_WEBSITE,
    "info:eu-repo/semantics/websiteContribution": constants.DOC_TYPE_WEBPAGE
}

MODS_GENRE_EPRINT_TO_METAJSON_DOCUMENT_TYPE = {
    # registered http://purl.org/eprint/type/ types
    "http://purl.org/eprint/type/Book": constants.DOC_TYPE_BOOK,
    "http://purl.org/eprint/type/BookItem": constants.DOC_TYPE_BOOKPART,
    "http://purl.org/eprint/type/BookReview": constants.DOC_TYPE_BOOKREVIEW,
    "http://purl.org/eprint/type/ConferenceItem": constants.DOC_TYPE_CONFERENCECONTRIBUTION,
    "http://purl.org/eprint/type/ConferencePaper": constants.DOC_TYPE_CONFERENCEPAPER,
    "http://purl.org/eprint/type/ConferencePoster": constants.DOC_TYPE_CONFERENCEPOSTER,
    "http://purl.org/eprint/type/JournalArticle": constants.DOC_TYPE_JOURNALARTICLE,
    "http://purl.org/eprint/type/JournalItem": constants.DOC_TYPE_PERIODICALISSUE,
    "http://purl.org/eprint/type/NewsItem": constants.DOC_TYPE_NEWSPAPERARTICLE,
    "http://purl.org/eprint/type/Patent": constants.DOC_TYPE_PATENT,
    "http://purl.org/eprint/type/Report": constants.DOC_TYPE_REPORT,
    "http://purl.org/eprint/type/SubmittedJournalArticle": constants.DOC_TYPE_PREPRINT,
    "http://purl.org/eprint/type/Thesis": constants.DOC_TYPE_DOCTORALTHESIS,
    "http://purl.org/eprint/type/WorkingPaper": constants.DOC_TYPE_WORKINGPAPER
}

MODS_GENRE_MARCGT_TO_METAJSON_DOCUMENT_TYPE = {
    # registered marcgt genre
    "abstract or summary": constants.DOC_TYPE_BOOKREVIEW,
    "article": constants.DOC_TYPE_JOURNALARTICLE,
    "atlas": constants.DOC_TYPE_MAP,
    "autobiography": constants.DOC_TYPE_BOOK,
    "bibliography": constants.DOC_TYPE_BIBLIOGRAPHY,
    "biography": constants.DOC_TYPE_BOOK,
    "book": constants.DOC_TYPE_BOOK,
    "conference publication": constants.DOC_TYPE_CONFERENCEPROCEEDINGS,
    "catalog": constants.DOC_TYPE_BOOK,
    "chart": constants.DOC_TYPE_CHART,
    "comic strip": constants.DOC_TYPE_BOOK,
    "database": constants.DOC_TYPE_DATABASE,
    "dictionary": constants.DOC_TYPE_DICTIONARY,
    "directory": constants.DOC_TYPE_BOOK,
    "drama": constants.DOC_TYPE_BOOK,
    "encyclopedia": constants.DOC_TYPE_ENCYCLOPEDIA,
    "essay": constants.DOC_TYPE_BOOK,
    "festschrift": constants.DOC_TYPE_BOOK,
    "fiction": constants.DOC_TYPE_BOOK,
    "folktale": constants.DOC_TYPE_BOOK,
    "globe": constants.DOC_TYPE_MAP,
    "graphic": constants.DOC_TYPE_CHART,
    "handbook": constants.DOC_TYPE_BOOK,
    "history": constants.DOC_TYPE_BOOK,
    "humor, satire": constants.DOC_TYPE_BOOK,
    "index": constants.DOC_TYPE_BOOK,
    "instruction": constants.DOC_TYPE_MANUEL,
    "issue": constants.DOC_TYPE_PERIODICALISSUE,
    "interview": constants.DOC_TYPE_INTERVIEWARTICLE,
    "journal": constants.DOC_TYPE_JOURNAL,
    "kit": constants.DOC_TYPE_BOOK,
    "language instruction": constants.DOC_TYPE_AUDIORECORDING,
    "law report or digest": constants.DOC_TYPE_ANNOTATIONARTICLE,
    "legislation": constants.DOC_TYPE_STATUTE,
    "letter": constants.DOC_TYPE_LETTER,
    "loose-leaf": constants.DOC_TYPE_PERIODICALISSUE,
    "map": constants.DOC_TYPE_MAP,
    "motion picture": constants.DOC_TYPE_FILM,
    "memoir": constants.DOC_TYPE_BOOK,
    "newspaper": constants.DOC_TYPE_NEWSPAPER,
    "novel": constants.DOC_TYPE_BOOK,
    "numeric data": constants.DOC_TYPE_DATASETQUANTI,
    "online system or service": constants.DOC_TYPE_WEBSITE,
    "patent": constants.DOC_TYPE_PATENT,
    "periodical": constants.DOC_TYPE_JOURNAL,
    "picture": constants.DOC_TYPE_IMAGE,
    "poetry": constants.DOC_TYPE_BOOK,
    "programmed text": constants.DOC_TYPE_SOFTWARE,
    "rehearsal": constants.DOC_TYPE_BOOK,
    "remote sensing image": constants.DOC_TYPE_MAP,
    "report": constants.DOC_TYPE_REPORT,
    "reporting": constants.DOC_TYPE_REPORT,
    "review": constants.DOC_TYPE_BOOKREVIEW,
    "series": constants.DOC_TYPE_SERIES,
    "short story": constants.DOC_TYPE_BOOK,
    "slide": constants.DOC_TYPE_SLIDE,
    "sound": constants.DOC_TYPE_AUDIORECORDING,
    "speech": constants.DOC_TYPE_SPEECH,
    "statistics": constants.DOC_TYPE_DATASETQUANTI,
    "survey of literature": constants.DOC_TYPE_BOOKREVIEW,
    "technical drawing": constants.DOC_TYPE_DRAWING,
    "technical report": constants.DOC_TYPE_TECHREPORT,
    "thesis": constants.DOC_TYPE_DOCTORALTHESIS,
    "treaty": constants.DOC_TYPE_TREATY,
    "videorecording": constants.DOC_TYPE_VIDEORECORDING,
    "web site": constants.DOC_TYPE_WEBSITE,
    "websiteContribution": constants.DOC_TYPE_WEBPAGE
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
    if mods is None:
        return None

    # mods version
    mods_version = mods.get("version")
    print "# mods_version: {}".format(mods_version)

    document = mods_root_or_related_item_to_metajson(mods, None)

    # source
    if source is not None:
        document["rec_source"] = source

    debug = True
    if debug:
        #print "mods genres: {}".format()
        metajson_service.pretty_print_document(document)
    return document


def mods_root_or_related_item_to_metajson(mods, root_rec_type):
    if mods is None:
        return None

    document = Document()

    # typeOfResource, genre -> rec_type, genres
    document.update(extract_mods_genres_type_of_resources(mods))
    if root_rec_type is not None and root_rec_type in constants.root_rec_type_to_is_part_of_rec_type:
        document["rec_type"] = constants.root_rec_type_to_is_part_of_rec_type[root_rec_type]
    rec_type = document["rec_type"]

    # ID, identifiers -> rec_id, identifiers
    document.update(extract_mods_identifiers_and_rec_id(mods))

    # titleInfo
    document.update(extract_mods_title_infos(mods))

    # name
    document.update(extract_mods_names(mods))

    # originInfo
    document.update(extract_mods_origin_info(mods))

    # languages
    document.update(extract_mods_languages(mods))

    # physicalDescription
    document.update(extract_mods_physical_description(mods, rec_type))

    # abstract
    document.update(extract_mods_abstracts(mods))

    # tableOfContents
    document.update(extract_mods_table_of_contentss(mods))

    # targetAudience
    document.update(extract_mods_target_audiences(mods))

    # note
    document.update(extract_mods_notes(mods))

    # subject
    document.update(extract_mods_subjects(mods))

    # classification
    document.update(extract_mods_classifications(mods))

    # relatedItem
    document.update(extract_mods_related_items(mods, rec_type))

    # location
    document.update(extract_mods_locations(mods))

    # accessCondition
    document.update(extract_mods_access_conditions(mods))

    # part
    document.update(extract_mods_parts(mods))

    # extension
    # dailist is managed by the function extract_mods_names

    # recordInfo
    document.update(extract_mods_record_info(mods))

    return document


def extract_mods_related_items(mods_root, root_rec_type):
    mods_related_items = mods_root.findall(prefixtag("mods", "relatedItem"))
    result = Document()
    if mods_related_items:
        # mods related_items

        for mods_related_item in mods_related_items:
            if mods_related_item is not None:
                # extract the relatedItem type attribute
                mods_related_item_type = mods_related_item.get("type")
                # mods_related_item_type in : preceding, succeeding, original, host, constituent, series, otherVersion, otherFormat, isReferencedBy, references, reviewOf)

                # convert like a mods record
                related_item = mods_root_or_related_item_to_metajson(mods_related_item, root_rec_type)

                if related_item is not None:
                    # extract related_item rec_type
                    related_item_rec_type = related_item["rec_type"]

                    #print "root_rec_type: {} related_item_rec_type: {} mods_related_item_type: {} ".format(root_rec_type, related_item_rec_type, mods_related_item_type)

                    if mods_related_item_type == "host":
                        # move the part fields from the related item to the root document
                        metajson_service.move_keys_between_dicts(MODS_PART_FIELDS, related_item, result)

                        # copy the date fields from the related item to the root document
                        if root_rec_type in MODS_ARTICLE_TYPES:
                            metajson_service.copy_keys_between_dicts(MODS_DATE_FIELDS, related_item, result)

                        # host -> is_part_ofs
                        result.add_item_to_key(related_item, "is_part_ofs")

                    elif mods_related_item_type == "original":

                        if root_rec_type in ["BookReview", "ArticleReview"]:
                            # original -> review_ofs
                            result.add_item_to_key(related_item, "review_ofs")
                        else:
                            # original -> originals
                            result.add_item_to_key(related_item, "originals")

                    elif mods_related_item_type == "reviewOf":

                        # reviewOf -> review_ofs
                        result.add_item_to_key(related_item, "review_ofs")

                    elif mods_related_item_type == "series":

                        # series -> seriess
                        result.add_item_to_key(related_item, "seriess")

                    elif mods_related_item_type == "constituent":

                        # constituent -> has_parts
                        result.add_item_to_key(related_item, "has_parts")

                    elif mods_related_item_type == "isReferencedBy":

                        # isReferencedBy -> is_referenced_bys
                        result.add_item_to_key(related_item, "is_referenced_bys")

                    elif mods_related_item_type == "references":

                        # references -> references
                        result.add_item_to_key(related_item, "references")

                    elif mods_related_item_type == "otherFormat":

                        # otherFormat -> other_formats
                        result.add_item_to_key(related_item, "other_formats")

                    elif mods_related_item_type == "otherVersion":

                        # otherVersion -> other_versions
                        result.add_item_to_key(related_item, "other_versions")

                    elif mods_related_item_type == "preceding":

                        # preceding -> precedings
                        result.add_item_to_key(related_item, "precedings")

                    elif mods_related_item_type == "succeedings":

                        # succeeding -> succeedings
                        result.add_item_to_key(related_item, "succeedings")

    return result


def extract_mods_genres_type_of_resources(mods):
    result = {}
    # genre
    mods_genres = mods.findall(prefixtag("mods", "genre"))
    if mods_genres:
        genre_eurepo = None
        genre_eprint = None
        genre_marcgt = None
        other_genres = []
        for mods_genre in mods_genres:
            genre_value = mods_genre.text.strip()
            genre_authority = mods_genre.get("authority")
            genre_type = mods_genre.get("type")
            # text
            if genre_value:
                if genre_value.startswith("info:eu-repo/semantics/"):
                    # last occurrence of eu-repo
                    genre_eurepo = genre_value
                elif genre_value.startswith("http://purl.org/eprint/type/"):
                    # last occurrence of eprint
                    genre_eprint = genre_value
                elif genre_marcgt is None and genre_value in MODS_GENRE_MARCGT_TO_METAJSON_DOCUMENT_TYPE:
                    # first occurrence of marcgt
                    genre_marcgt = genre_value
                else:
                    genre = {}
                    genre["value"] = genre_value
                    if genre_authority:
                        # authority
                        genre["authority"] = genre_authority
                    if genre_type:
                        # type (examples: class, work type, or style)
                        genre["type"] = genre_type
                    other_genres.append(genre)
        # rec_type is based on authorities: eu-repo, eprint, marcgt
        rec_type = None
        if genre_eurepo:
            rec_type = MODS_GENRE_EUREPO_TO_METAJSON_DOCUMENT_TYPE[genre_eurepo]
        elif rec_type is None and genre_eprint:
            rec_type = MODS_GENRE_EPRINT_TO_METAJSON_DOCUMENT_TYPE[genre_eprint]
        elif rec_type is None and genre_marcgt:
            rec_type = MODS_GENRE_MARCGT_TO_METAJSON_DOCUMENT_TYPE[genre_marcgt]
        else:
            rec_type = "Document"
        result["rec_type"] = rec_type

        if other_genres:
            result["genres"] = other_genres

    # typeOfResource
    mods_type_of_resources = mods.findall(prefixtag("mods", "typeOfResource"))
    if mods_type_of_resources:
        for mods_type_of_resource in mods_type_of_resources:
            # todo

            # text values:
            # text, cartographic, notated music, sound recording-musical, sound recording-nonmusical, sound recording,
            # still image, moving image, three dimensional object, software, multimedia, mixed material

            # collection
            # value: yes

            # manuscript
            # value: yes
            pass

    return result


def extract_mods_identifiers_and_rec_id(mods):
    result = {}

    # rec_id
    rec_id = None
    mods_id = mods.get("ID")
    if mods_id is not None:
        rec_id = mods_id

    # identifiers
    mods_identifiers = mods.findall(prefixtag("mods", "identifier"))
    if mods_identifiers:
        identifiers = []
        for mods_identifier in mods_identifiers:
            if mods_identifier is not None:
                identifier = metajson_service.create_identifier(mods_identifier.get("type"), mods_identifier.text.strip())
                if identifier:
                    identifiers.append(identifier)
        if identifiers:
            result["identifiers"] = identifiers
            if rec_id is None:
                rec_id = "{}:{}".format(identifiers[0]["id_type"], identifiers[0]["value"])

    if rec_id:
        result["rec_id"] = rec_id
    return result


def extract_mods_title_infos(mods):
    result = {}
    mods_titleinfos = mods.findall(prefixtag("mods", "titleInfo"))
    if mods_titleinfos is not None:
        for mods_titleinfo in mods_titleinfos:
            if mods_titleinfo is not None:
                title_dict = {}
                # type
                title_type = mods_titleinfo.get("type")
                # title
                if mods_titleinfo.find(prefixtag("mods", "title")) is not None:
                    title_dict["title"] = mods_titleinfo.find(prefixtag("mods", "title")).text.strip()
                # nonSort
                if mods_titleinfo.find(prefixtag("mods", "nonSort")) is not None:
                    title_dict["title_non_sort"] = mods_titleinfo.find(prefixtag("mods", "nonSort")).text
                # subTitle
                if mods_titleinfo.find(prefixtag("mods", "subTitle")) is not None:
                    title_dict["title_sub"] = mods_titleinfo.find(prefixtag("mods", "subTitle")).text.strip()
                # partNumber
                if mods_titleinfo.find(prefixtag("mods", "partNumber")) is not None:
                    title_dict["part_number"] = mods_titleinfo.find(prefixtag("mods", "partNumber")).text.strip()
                # partName
                if mods_titleinfo.find(prefixtag("mods", "partName")) is not None:
                    title_dict["part_name"] = mods_titleinfo.find(prefixtag("mods", "partName")).text.strip()

                if title_type is None and "title" not in result:
                    result.update(title_dict)
                elif title_type == "abbreviated":
                    result["title_abbreviated"] = title_dict
                elif title_type == "alternative":
                    result["title_alternative"] = title_dict
                elif title_type == "translated":
                    result["title_translated"] = title_dict
                elif title_type == "uniform":
                    result["title_uniform"] = title_dict
                else:
                    print "error convert_mods_titleinfos unknown type: {}".format(title_type)
    return result


def extract_mods_names(mods):
    result = {}
    mods_names = mods.findall(prefixtag("mods", "name"))
    if mods_names:
        dai_dict = extract_mods_dailist_to_dict(mods)
        creators = []
        for mods_name in mods_names:
            creator = convert_mods_name_dai_dict_to_creator(mods_name, dai_dict)
            if creator is not None:
                creators.append(creator)
        if creators:
            result["creators"] = creators
    return result


def extract_mods_dailist_to_dict(mods):
    mods_extension = mods.find(prefixtag("mods", "extension"))
    if mods_extension is not None:
        mods_dai_list = mods_extension.find(prefixtag("dai", "daiList"))
        if mods_dai_list is not None:
            mods_dai_identifiers = mods_dai_list.findall(prefixtag("dai", "identifier"))
            if mods_dai_identifiers:
                result = {}
                for mods_dai_identifier in mods_dai_identifiers:
                    authority = mods_dai_identifier.get("authority")
                    dai = mods_dai_identifier.text.strip()
                    result[mods_dai_identifier.get("IDref")] = {"authority": authority, "value": dai}
                return result


def convert_mods_name_dai_dict_to_creator(mods_name, dai_dict):
    if mods_name is not None:
        creator = Creator()
        # extract mods properties
        # type
        mods_name_type = mods_name.get("type")
        # ID
        mods_name_id = mods_name.get("ID")
        # namePart
        mods_name_parts = mods_name.findall(prefixtag("mods", "namePart"))
        # affiliation
        mods_name_affiliations = mods_name.findall(prefixtag("mods", "affiliation"))
        # role
        mods_name_role = mods_name.find(prefixtag("mods", "role"))
        mods_name_roleterm = None
        if mods_name_role is not None:
            mods_name_roleterm = mods_name_role.find(prefixtag("mods", "roleTerm"))
        # description
        mods_name_descriptions = mods_name.findall(prefixtag("mods", "description"))

        #agent_rec_id, agent_identifiers, affiliation_name, affiliation_rec_id
        agent_rec_id = None
        agent_identifiers = None
        affiliation_name = None
        affiliation_rec_id = None
        affiliation = None
        if mods_name_id is not None:
            if "spire" in mods_name_id:
                # In case of Spire name.ID
                # name.ID format : _-_spire_-_creator_id_-_creator_dai_-_affiliation_id_-_random_id
                spire_name_ids = mods_name_id.split("_-_")
                if spire_name_ids and len(spire_name_ids) >= 4:
                    agent_rec_id = spire_name_ids[2].replace("__", "/")
                    affiliation_rec_id = spire_name_ids[4]
                    if affiliation_rec_id:
                        affiliation_rec_id = affiliation_rec_id.replace("__", "/")
            elif dai_dict is not None and mods_name_id in dai_dict:
                # agent_rec_id
                agent_rec_id = dai_dict[mods_name_id]["value"]
                # agent_identifiers
                id_value = dai_dict[mods_name_id]["authority"] + "/" + dai_dict[mods_name_id]["value"]
                agent_identifiers = [metajson_service.create_identifier("uri", id_value)]

        if mods_name_affiliations:
            affiliation_name = mods_name_affiliations[0].text.strip()

        if affiliation_name or affiliation_rec_id:
            affiliation = metajson_service.create_affiliation(affiliation_rec_id, affiliation_name, None, None, None, False)

        if mods_name_type == "personal":
            # print "personal"
            person = Person()

            if agent_rec_id:
                person["rec_id"] = agent_rec_id
            if agent_identifiers:
                person["identifiers"] = agent_identifiers

            if mods_name_parts:
                for mods_name_part in mods_name_parts:
                    if mods_name_part.get("type") == "given":
                        person["name_given"] = mods_name_part.text.strip()
                    elif mods_name_part.get("type") == "family":
                        person["name_family"] = mods_name_part.text.strip()
                    elif mods_name_part.get("type") == "date":
                        date = mods_name_part.text.replace("(", "").replace(")", "").strip()
                        minus_index = date.find("-")
                        if minus_index == -1:
                            person["date_birth"] = date
                        else:
                            person["date_birth"] = date[:minus_index]
                            person["date_death"] = date[minus_index+1:]
                    elif mods_name_part.get("termsOfAddress") == "date":
                        person["name_terms_of_address"] = mods_name_part.text

            creator["agent"] = person

        elif mods_name_type == "corporate":
            # print "corporate"
            orgunit = Orgunit()
            creator["agent"] = orgunit

            if mods_name_parts:
                orgunit["name"] = mods_name_parts[0].text.strip()

        elif mods_name_type == "conference":
            # print "conference"
            event = Event()
            creator["agent"] = event

            if mods_name_parts:
                for mods_name_part in mods_name_parts:
                    if mods_name_part.get("type") is None:
                        event["title"] = mods_name_part.text.strip()
                    elif mods_name_part.get("type") == "termsOfAddress":
                        address = mods_name_part.text.strip()
                        sep_index = address.find(";")
                        if sep_index == -1:
                            event["place"] = address
                        else:
                            event["place"] = address[:sep_index]
                            event["country"] = address[sep_index+1:]
                    elif mods_name_part.get("type") == "date":
                        date = mods_name_part.text.strip()
                        slash_index = date.find("/")
                        if slash_index == -1:
                            event["date_start"] = date
                        else:
                            event["date_start"] = date[:slash_index]
                            event["date_end"] = date[slash_index+1:]

        elif mods_name_type == "family":
            # print "family"
            family = Family()
            creator["agent"] = family

        if affiliation:
            creator["affiliation"] = affiliation

        if mods_name_roleterm is not None:
            creator["role"] = convert_mods_name_roleterm(mods_name_roleterm)

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


def extract_mods_origin_info(mods):
    mods_origin_info = mods.find(prefixtag("mods", "originInfo"))
    result = {}
    if mods_origin_info is not None:
        # dateIssued
        date_issued = convert_mods_date(mods_origin_info.find(prefixtag("mods", "dateIssued")))
        if date_issued:
            result["date_issued"] = date_issued
        # dateCreated
        date_created = convert_mods_date(mods_origin_info.find(prefixtag("mods", "dateCreated")))
        if date_created:
            result["date_created"] = date_created
        # dateCaptured
        date_captured = convert_mods_date(mods_origin_info.find(prefixtag("mods", "dateCaptured")))
        if date_captured:
            result["date_captured"] = date_captured
        # dateValid
        date_valid = convert_mods_date(mods_origin_info.find(prefixtag("mods", "dateValid")))
        if date_valid:
            result["date_valid"] = date_valid
        # dateModified
        date_modified = convert_mods_date(mods_origin_info.find(prefixtag("mods", "dateModified")))
        if date_modified:
            result["date_modified"] = date_modified
        # copyrightDate
        date_copyrighted = convert_mods_date(mods_origin_info.find(prefixtag("mods", "copyrightDate")))
        if date_copyrighted:
            result["date_copyrighted"] = date_copyrighted
        # dateOther
        date_other = convert_mods_date(mods_origin_info.find(prefixtag("mods", "dateOther")))
        if date_other:
            result["date_other"] = date_other

        # edition
        mods_edition = mods_origin_info.find(prefixtag("mods", "edition"))
        if mods_edition is not None:
            result["edition"] = mods_edition.text.strip()

        # frequency
        mods_frequency = mods_origin_info.find(prefixtag("mods", "frequency"))
        if mods_frequency is not None:
            result["frequency"] = mods_frequency.text.strip()

        # issuance
        mods_issuance = mods_origin_info.find(prefixtag("mods", "issuance"))
        if mods_issuance is not None:
            result["issuance"] = mods_issuance.text.strip()

        # place
        mods_places = mods_origin_info.findall(prefixtag("mods", "place"))
        if mods_places is not None:
            publication_countries = []
            publication_places = []
            for mods_place in mods_places:
                if mods_place is not None:
                    mods_place_term = mods_place.find(prefixtag("mods", "placeTerm"))
                    if mods_place_term is not None:
                        place_value = mods_place_term.text.strip()
                        place_type = mods_place_term.get("type")
                        place_authority = mods_place_term.get("authority")
                        if place_value:
                            if place_authority == "iso3166":
                                pass
                            # todo metajson: type : country, city
                            # add type (code, text) and authority (marcgac, marccountry, iso3166)
                            publication_places.append(place_value)
            if publication_places:
                result["publication_places"] = publication_places

        # publisher
        mods_publishers = mods_origin_info.findall(prefixtag("mods", "publisher"))
        if mods_publishers is not None:
            publishers = []
            for mods_publisher in mods_publishers:
                if mods_publisher is not None:
                    # todo metajson: based on agent
                    publishers.append(mods_publisher.text.strip())
            if publishers:
                result["publishers"] = publishers

    return result


def convert_mods_date(mods_date):
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


def extract_mods_physical_description(mods, rec_type):
    result = {}
    mods_physical_description = mods.find(prefixtag("mods", "physicalDescription"))
    if mods_physical_description is not None:
        # digitalOrigin
        mods_digital_origin = mods_physical_description.find(prefixtag("mods", "digitalOrigin"))
        if mods_digital_origin is not None:
            result["digital_origin"] = mods_digital_origin
        # extent
        mods_extent = mods_physical_description.find(prefixtag("mods", "extent"))
        if mods_extent is not None:
            extent_value = mods_extent.text.strip()
            if extent_value:
                if rec_type in ["AudioBook", "AudioBroadcast", "AudioRecording", "MusicRecording", "VideoBroadcast", "VideoRecording", "VideoPart"]:
                    result["extent_duration"] = extent_value
                elif rec_type in ["PhysicalObject"]:
                    result["extent_dimension"] = extent_value
                else:
                    result["extent_pages"] = extent_value
        # internetMediaType
        mods_internet_media_type = mods_physical_description.find(prefixtag("mods", "internetMediaType"))
        # form
        mods_form = mods_physical_description.find(prefixtag("mods", "form"))
        # note
        mods_notes = mods_physical_description.findall(prefixtag("mods", "note"))
        # reformattingQuality
        mods_reformatting_quality = mods_physical_description.find(prefixtag("mods", "reformattingQuality"))
    return result


def extract_mods_languages(mods):
    result = {}
    mods_languages = mods.findall(prefixtag("mods", "language"))
    if mods_languages is not None:
        languages = []
        for mods_language in mods_languages:
            if mods_language is not None:
                mods_terms = mods_language.findall(prefixtag("mods", "languageTerm"))
                if mods_terms is not None:
                    for mods_term in mods_terms:
                        # todo use language_service
                        if mods_term.get("type") == "code":
                            if mods_term.get("authority") == "rfc3066":
                                language = mods_term.text.strip()
                                if language is not None:
                                    languages.append(mods_term.text)
                            else:
                                # todo for iso639-2b and other authority
                                pass
                        else:
                            # todo for natural language like "French"
                            pass
        if languages:
            result["languages"] = languages
    return result


def extract_mods_abstracts(mods):
    result = {}
    mods_abstracts = mods.findall(prefixtag("mods", "abstract"))
    if mods_abstracts is not None:
        descriptions = convert_mods_string_langs(mods_abstracts)
        if descriptions:
            result["descriptions"] = descriptions
    return result


def extract_mods_table_of_contentss(mods):
    result = {}
    mods_table_of_contentss = mods.findall(prefixtag("mods", "tableOfContents"))
    if mods_table_of_contentss is not None:
        table_of_contentss = convert_mods_string_langs(mods_table_of_contentss)
        if table_of_contentss:
            result["table_of_contentss"] = table_of_contentss
    return result


def convert_mods_string_langs(mods_string_langs):
    if mods_string_langs is not None:
        results = []
        for mods_string_lang in mods_string_langs:
            if mods_string_lang is not None:
                language = mods_string_lang.get("lang")
                value = mods_string_lang.text.strip()
                if value is not None:
                    result = {"value": value}
                    if language is not None:
                        result["language"] = language.strip()
                    results.append(result)
        return results


def extract_mods_target_audiences(mods):
    result = {}
    mods_target_audiences = mods.findall(prefixtag("mods", "targetAudience"))
    if mods_target_audiences is not None:
        target_audiences = convert_mods_string_authorities(mods_target_audiences)
        if target_audiences:
            result["target_audiences"] = target_audiences
    return result


def convert_mods_string_authorities(mods_string_authorities):
    if mods_string_authorities is not None:
        results = []
        for mods_string_authority in mods_string_authorities:
            if mods_string_authority is not None:
                authority = mods_string_authority.get("authority")
                value = mods_string_authority.text.strip()
                if value is not None:
                    result = {"value": value}
                    if authority is not None:
                        result["authority"] = authority.strip()
                    results.append(result)
        return results


def extract_mods_notes(mods):
    result = {}
    mods_notes = mods.findall(prefixtag("mods", "note"))
    if mods_notes is not None:
        notes = convert_mods_string_lang_types(mods_notes, "note_type")
        if notes:
            result["notes"] = notes
    return result


def extract_mods_access_conditions(mods):
    result = {}
    mods_access_conditions = mods.findall(prefixtag("mods", "accessCondition"))
    if mods_access_conditions is not None:
        access_conditions = convert_mods_string_lang_types(mods_access_conditions, "rights_type")
        if access_conditions:
            rights = Rights()
            for access_condition in access_conditions:
                if "rights_type" in access_condition:
                    if access_condition["rights_type"] == "restriction on access":
                        del access_condition["rights_type"]
                        if "restriction_on_access" not in rights:
                            rights["restriction_on_access"] = []
                        rights["restriction_on_access"].append(access_condition)
                    elif access_condition["rights_type"] == "use and reproduction":
                        del access_condition["rights_type"]
                        if "use_and_reproduction" not in rights:
                            rights["use_and_reproduction"] = []
                        rights["use_and_reproduction"].append(access_condition)
            if rights:
                result["rights"] = rights
    return result


def convert_mods_string_lang_types(mods_string_lang_types, type_field):
    if mods_string_lang_types is not None:
        results = []
        for mods_string_lang_type in mods_string_lang_types:
            if mods_string_lang_type is not None:
                language = mods_string_lang_type.get("lang")
                type_value = mods_string_lang_type.get("type")
                value = mods_string_lang_type.text.strip()
                if value is not None:
                    result = {"value": value}
                    if language is not None:
                        result["language"] = language.strip()
                    if type_value is not None:
                        result[type_field] = type_value.strip()
                    results.append(result)
        return results


def extract_mods_subjects(mods):
    result = {}
    mods_subjects = mods.findall(prefixtag("mods", "subject"))
    if mods_subjects is not None:
        result_subjects = []
        result_keywords_dict = {}
        for mods_subject in mods_subjects:
            if mods_subject is not None:
                mods_subject_authority = mods_subject.get("authority")
                mods_subject_lang = mods_subject.get("lang")
                if mods_subject_lang is not None and mods_subject_lang not in result_keywords_dict:
                    result_keywords_dict[mods_subject_lang] = []
                elif mods_subject_lang is None:
                    result_keywords_dict[constants.LANGUAGE_UNDETERMINED] = []
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
                                        result_keywords_dict[mods_subject_lang].append(term.strip())
                                    else:
                                        result_keywords_dict[constants.LANGUAGE_UNDETERMINED].append(term.strip())
        if result_subjects:
            result["subjects"] = result_subjects
        if result_keywords_dict:
            result["keywords"] = result_keywords_dict
    return result


def extract_mods_classifications(mods):
    result = {}
    mods_classifications = mods.findall(prefixtag("mods", "classification"))
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

        if classifications_dict:
            result["classifications"] = classifications_dict
        if peer_review:
            result["peer_review"] = peer_review
        if peer_review_geo:
            result["peer_review_geo"] = peer_review_geo
    return result


def extract_mods_parts(mods):
    result = {}
    mods_parts = mods.findall(prefixtag("mods", "part"))
    if mods_parts is not None:
        result = {}
        for mods_part in mods_parts:
            if mods_part is not None:
                # detail
                mods_part_details = mods_part.findall(prefixtag("mods", "detail"))
                if mods_part_details is not None:
                    for mods_part_detail in mods_part_details:
                        mods_part_detail_type = mods_part_detail.get("type")
                        mods_part_detail_number = mods_part_detail.find(prefixtag("mods", "number"))
                        if mods_part_detail_type is not None and mods_part_detail_number is not None and mods_part_detail_number.text is not None:
                            if mods_part_detail_type == "volume":
                                result["part_volume"] = mods_part_detail_number.text
                            elif mods_part_detail_type == "issue":
                                result["part_issue"] = mods_part_detail_number.text

                # extent
                mods_part_extents = mods_part.findall(prefixtag("mods", "extent"))
                if mods_part_extents is not None:
                    for mods_part_extent in mods_part_extents:
                        mods_part_extent_unit = mods_part_extent.get("unit")
                        mods_part_extent_start = mods_part_extent.find(prefixtag("mods", "start"))
                        mods_part_extent_end = mods_part_extent.find(prefixtag("mods", "end"))
                        if mods_part_extent_unit is not None and (mods_part_extent_start is not None or mods_part_extent_end is not None):
                            if mods_part_extent_unit == "page" or mods_part_extent_unit == "pages":
                                if mods_part_extent_start is not None and mods_part_extent_start.text is not None:
                                    result["part_page_start"] = mods_part_extent_start.text
                                if mods_part_extent_end is not None and mods_part_extent_end.text is not None:
                                    result["part_page_end"] = mods_part_extent_end.text
    return result


def extract_mods_locations(mods):
    result = {}
    locations = mods.findall(prefixtag("mods", "location"))
    if locations is not None:
        resources = []
        for location in locations:
            if location is not None:
                resource = Resource()
                # url -> remote
                mods_url = location.find(prefixtag("mods", "url"))
                if mods_url is not None:
                    url = mods_url.text.strip()
                    date_last_accessed = mods_url.get("dateLastAccessed")
                    if url:
                        resource["rec_type"] = "remote"
                        resource["url"] = url
                        if date_last_accessed is not None:
                            resource["dateLastAccessed"] = date_last_accessed.strip()

                # physicalLocation
                # shelfLocator
                # holdingSimple
                # holdingExternal

                resources.append(resource)
        if resources:
            result["resources"] = resources
    return result


def extract_mods_record_info(mods):
    result = {}
    mods_record_info = mods.find(prefixtag("mods", "recordInfo"))
    if mods_record_info is not None:
        # todo
        # recordContentSource
        # recordCreationDate
        # recordChangeDate
        # recordIdentifier
        # recordOrigin
        # languageOfCataloging
        # descriptionStandard
        pass
    return result
