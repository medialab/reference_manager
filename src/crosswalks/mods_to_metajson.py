#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from metajson import metajson
from metajson.metajson import Common
from metajson.metajson import Document
from metajson.metajson import Resource
from metajson.metajson import Contributor
from metajson.metajson import Identifier
from metajson.metajson import Person
from metajson.metajson import Family
from metajson.metajson import Orgunit
from metajson.metajson import Event
from metajson import metajson_contrib_util
from util import language_util
from util import other_util
from dissemination import file_export
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import QName

xmlns_map = {
    "mods": "http://www.loc.gov/mods/v3",
    "dai": "info:eu-repo/dai",
    "researcherml": "http://bibliotheque.sciences-po.fr/standards/researcherml/v1"
}

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
    for key in xmlns_map:
        ET.register_namespace(key, xmlns_map[key])


def prefixtag(ns_prefix, tagname):
    if tagname:
        if ns_prefix and ns_prefix in xmlns_map:
            return str(QName(xmlns_map[ns_prefix], tagname))
        else:
            return tagname


def convert_mods_file_to_metajson_document_list(mods_filename):
    register_namespaces()

    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(mods_filename, parser=parser)

    document_list = []

    root = tree.getroot()
    if root is not None:
        if root.tag.endswith("mods"):
            document = convert_mods_to_metajson_document(root, mods_filename)
            document_list.append(document)
        elif root.tag.endswith("modsCollection"):
            mods_list = root.findall("mods")
            if mods_list:
                for mods in mods_list:
                    document_list.append(convert_mods_to_metajson_document(mods, mods_filename))

    return document_list


def convert_mods_to_metajson_document(mods, source):
    document = Document()

    # source
    document["rec_source"] = source

    # rec_type, metajson_class, genres
    document.update(extract_class_type_genres(mods))
    rec_type = document["rec_type"]

    # rec_id, identifiers
    identifiers = convert_mods_identifiers(mods.findall(prefixtag("mods", "identifier")))
    rec_id = ""
    if identifiers:
        if identifiers[0]["type"]:
            rec_id = identifiers[0]["type"] + "_"
        rec_id += identifiers[0]["value"]
    document["rec_id"] = rec_id
    document["identifiers"] = identifiers

    # title
    document.update(convert_mods_titleinfos(mods.findall(prefixtag("mods", "titleInfo"))))

    # contributors
    contributors = extract_contributors(mods)
    if contributors:
        print contributors
        document["contributors"] = contributors

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
    result["metajson_class"] = "Document"
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
            title_dict["title"] = mods_titleinfo.find(prefixtag("mods", "title")).text
        if mods_titleinfo.find(prefixtag("mods", "nonSort")) is not None:
            title_dict["title_non_sort"] = mods_titleinfo.find(prefixtag("mods", "nonSort")).text
        if mods_titleinfo.find(prefixtag("mods", "subTitle")) is not None:
            title_dict["title_sub"] = mods_titleinfo.find(prefixtag("mods", "subTitle")).text
        if mods_titleinfo.find(prefixtag("mods", "partNumber")) is not None:
            title_dict["part_number"] = mods_titleinfo.find(prefixtag("mods", "partNumber")).text
        if mods_titleinfo.find(prefixtag("mods", "partName")) is not None:
            title_dict["part_name"] = mods_titleinfo.find(prefixtag("mods", "partName")).text

        #print title_dict
        return title_dict


def extract_contributors(mods):
    mods_names = mods.findall(prefixtag("mods", "name"))
    if mods_names:
        extension = mods.find(prefixtag("mods", "extension"))
        dai_dict = None
        if extension is not None:
            dai_dict = convert_mods_dailist_to_dict(extension.find(prefixtag("dai", "daiList")))

        result = []
        for mods_name in mods_names:
            contributor = convert_mods_name_to_contributor(mods_name, dai_dict)
            if contributor is not None:
                result.append(contributor)
        return result


def convert_mods_dailist_to_dict(dai_list):
    if dai_list is not None:
        dai_identifiers = dai_list.findall(prefixtag("dai", "identifier"))
        if dai_identifiers:
            result = {}
            for dai_identifier in dai_identifiers:
                result[dai_identifier.get("IDref")] = {"authority": dai_identifier.get("authority"), "value": dai_identifier.text}
            print result
            return result


def convert_mods_name_to_contributor(mods_name, dai_dict):
    if mods_name is not None:
        contributor = Contributor()
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

        if name_type == "personal":
            person = Person()

            if name_id is not None and dai_dict is not None and name_id in dai_dict:
                id_value = dai_dict[name_id]["authority"] + "/" + dai_dict[name_id]["value"]
                identifier = metajson.create_identifier("uri", id_value)
                person.add_item_to_key(identifier, "identifiers")

            if name_parts:
                for name_part in name_parts:
                    if name_part.get("type") == "given":
                        person["name_given"] = name_part.text
                    elif name_part.get("type") == "family":
                        person["name_family"] = name_part.text
                    elif name_part.get("type") == "date":
                        date = name_part.text.replace("(", "").replace(")", "")
                        minus_index = date.find("-")
                        if minus_index == -1:
                            person["date_of_birth"] = date
                        else:
                            person["date_of_birth"] = date[:minus_index]
                            person["date_of_death"] = date[minus_index+1:]
                    elif name_part.get("termsOfAddress") == "date":
                        person["name_terms_of_address"] = name_part.text

            contributor["person"] = person
        print name_type, name_id, name_parts, name_affiliations, name_roleterm, name_descriptions
        return contributor


def convert_mods_name_roleterms(mods_roleterms):
    if mods_roleterms:
        for mods_roleterm in mods_roleterms:
            authority = mods_roleterm.get("authority")
            term_type = mods_roleterm.get("type")
            value = mods_roleterm.text
            print authority, term_type, value


def test():
    metajson_list = convert_mods_file_to_metajson_document_list("../test/data/mods2.xml")
    file_export.export_metajson(metajson_list, "../test/data/result_mods_metajon.json")
    print json.dumps(metajson_list, indent=4, ensure_ascii=False, encoding="utf-8", sort_keys=True)

other_util.setup_console()
test()
