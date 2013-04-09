#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from metadatas import metajson
from metadatas.metajson import Common, Document, Contributor, Identifier, Resource
from metadatas import metajson_contrib_util
from util import language_util
from util import other_util
from dissemination import file_export
import xml.etree.ElementTree as ET

XMLNS_MODS = "http://www.loc.gov/mods/v3"
XMLNS_DAI = "info:eu-repo/dai"
XMLNS_RESEARCHERML = "http://bibliotheque.sciences-po.fr/standards/researcherml/v1"

xmlns_map = {
    "mods" : XMLNS_MODS, 
    "dai" : XMLNS_DAI,
    "researcherml" : XMLNS_RESEARCHERML
}

mods_genre_uri_to_metajson_document_type = {
    # info:eu-repo/semantics
    "info:eu-repo/semantics/annotation" : "Annotation",
    "info:eu-repo/semantics/article" : "JournalArticle",
    "info:eu-repo/semantics/bachelorThesis" : "MasterThesis",
    "info:eu-repo/semantics/book" : "Book",
    "info:eu-repo/semantics/bookPart" : "BookPart",
    "info:eu-repo/semantics/bookReview" : "BookReview",
    "info:eu-repo/semantics/conferenceContribution" : "ConferenceContribution",
    "info:eu-repo/semantics/conferenceItem" : "ConferenceContribution",
    "info:eu-repo/semantics/conferenceObject" : "ConferenceContribution",
    "info:eu-repo/semantics/conferencePaper" : "ConferencePaper",
    "info:eu-repo/semantics/conferencePoster" : "ConferencePoster",
    "info:eu-repo/semantics/conferenceProceedings" : "ConferenceProceedings",
    "info:eu-repo/semantics/contributionToPeriodical" : "ContributionToPeriodical",
    "info:eu-repo/semantics/doctoralThesis" : "DoctoralThesis",
    "info:eu-repo/semantics/lecture" : "ConferenceContribution",
    "info:eu-repo/semantics/masterThesis" : "MasterThesis",
    "info:eu-repo/semantics/other" : "Document",
    "info:eu-repo/semantics/patent" : "Patent",
    "info:eu-repo/semantics/preprint" : "Preprint",
    "info:eu-repo/semantics/report" : "Report",
    "info:eu-repo/semantics/reportPart" : "ReportPart",
    "info:eu-repo/semantics/researchProposal" : "Document",
    "info:eu-repo/semantics/review" : "BookReview",
    "info:eu-repo/semantics/studentThesis" : "MasterThesis",
    "info:eu-repo/semantics/technicalDocumentation" : "Document",
    "info:eu-repo/semantics/workingPaper" : "WorkingPaper",
    # not registered info:eu-repo/semantics types
    "info:eu-repo/semantics/audiovisual" : "Audiovisual",
    "info:eu-repo/semantics/interview" : "Interview",
    "info:eu-repo/semantics/map" : "Map",
    "info:eu-repo/semantics/periodicalIssue" : "PeriodicalIssue",
    "info:eu-repo/semantics/professoralThesis" : "ProfessoralThesis",
    "info:eu-repo/semantics/series" : "Series",
    "info:eu-repo/semantics/unspecified" : "Document",
    "info:eu-repo/semantics/website" : "Website",
    "info:eu-repo/semantics/websiteContribution" : "WebsiteContribution",

    # http://purl.org/eprint/type/
    "http://purl.org/eprint/type/Book" : "Book",
    "http://purl.org/eprint/type/BookItem" : "BookPart",
    "http://purl.org/eprint/type/BookReview" : "BookReview",
    "http://purl.org/eprint/type/ConferenceItem" : "ConferenceContribution",
    "http://purl.org/eprint/type/ConferencePaper" : "ConferencePaper",
    "http://purl.org/eprint/type/ConferencePoster" : "ConferencePoster",
    "http://purl.org/eprint/type/JournalArticle" : "JournalArticle",
    "http://purl.org/eprint/type/JournalItem" : "PeriodicalIssue",
    "http://purl.org/eprint/type/NewsItem" : "ContributionToPeriodical",
    "http://purl.org/eprint/type/Patent" : "Patent",
    "http://purl.org/eprint/type/Report" : "Report",
    "http://purl.org/eprint/type/SubmittedJournalArticle" : "Preprint",
    "http://purl.org/eprint/type/Thesis" : "DoctoralThesis",
    "http://purl.org/eprint/type/WorkingPaper" : "WorkingPaper"
}

mods_genre_margt_to_metajson_document_type = {
    "abstract or summary" : "Book",
    "article" : "JournalArticle",
    "atlas" : "Map",
    "autobiography" : "Book",
    "bibliography" : "Book",
    "biography" : "Book",
    "book" : "Book",
    "conference publication" : "ConferenceProceedings",
    "catalog" : "Book",
    "chart" : "Map",
    "comic strip" : "Book",
    "database" : "Document",
    "dictionary" : "Book",
    "directory" : "Book",
    "drama" : "Book",
    "encyclopedia" : "Book",
    "essay" : "Book",
    "festschrift" : "Book",
    "fiction" : "Book",
    "folktale" : "Book",
    "globe" : "Map",
    "graphic" : "Map",
    "handbook" : "Book",
    "history" : "Book",
    "humor, satire" : "Book",
    "index" : "Book",
    "instruction" : "Book",
    "issue" : "PeriodicalIssue",
    "interview" : "Interview",
    "journal" : "journal",
    "kit" : "Book",
    "language instruction" : "Audiovisual",
    "law report or digest" : "Annotation",
    "legislation" : "Annotation",
    "letter" : "Preprint",
    "loose-leaf" : "Periodical",
    "map" : "Map",
    "motion picture" : "Audiovisual",
    "memoir" : "Book",
    "newspaper" : "Newspaper",
    "novel" : "Book",
    "numeric data" : "Book",
    "online system or service" : "Website",
    "patent" : "Patent",
    "periodical" : "Periodical",
    "picture" : "Map",
    "poetry" : "Book",
    "programmed text" : "Book",
    "rehearsal" : "Book",
    "remote sensing image" : "Map",
    "report" : "Report",
    "reporting" : "Report",
    "review" : "BookReview",
    "series" : "Series",
    "short story" : "Book",
    "slide" : "Audiovisual",
    "sound" : "Audiovisual",
    "speech" : "ConferenceContribution",
    "statistics" : "Book",
    "survey of literature" : "BookReview",
    "technical drawing" : "Map",
    "technical report" : "Report",
    "thesis" : "DoctoralThesis",
    "treaty" : "Book",
    "videorecording" : "Audiovisual",
    "web site" : "Website",
    "websiteContribution" : "websiteContribution"
}

def register_namespaces():
    for key in xmlns_map:
        ET.register_namespace(key, xmlns_map[key])


def convert_mods_file_to_metajson_document_list(mods_filename):
    register_namespaces()

    parser = ET.XMLParser(encoding = "utf-8")
    tree = ET.parse(mods_filename, parser = parser)

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

    # identifiers
    identifiers = convert_mods_identifiers(mods.findall("./{"+XMLNS_MODS+"}identifier"))
    rec_id = None
    if identifiers:
        rec_id = identifiers[0]["value"]
    
    rec_type = None
    type_dict = extract_class_type_genres(mods)
    if type_dict and "rec_type" in type_dict:
        rec_type = type_dict["rec_type"]

    # rec_id, rec_source
    document["rec_id"] = rec_id
    document["rec_source"] = source
    document["identifiers"] = identifiers

    document["rec_type"] = rec_type
    return document


def extract_class_type_genres(mods):
    mods_genres = mods.findall("./{"+XMLNS_MODS+"}genre")
    if mods_genres:
        rec_type = None
        genres = []
        metajson_class = None
        for mods_genre in mods_genres:
            if mods_genre.text in mods_genre_uri_to_metajson_document_type:
                rec_type = mods_genre_uri_to_metajson_document_type[mods_genre.text]
                metajson_class = "Document"
            elif mods_genre.text in mods_genre_margt_to_metajson_document_type:
                rec_type = mods_genre_margt_to_metajson_document_type[mods_genre.text]
                metajson_class = "Document"
            else:
                genres.append(mods_genre.text)
        if rec_type or genres or metajson_class:
            result = {}
            if rec_type:
                result["rec_type"] = rec_type
            if genres:
                result["genres"] = genres
            if metajson_class:
                result["metajson_class"] = metajson_class
            return result


def convert_mods_genre_list_to_metajson_document_type(genre_list):
    if genre_list:
        for genre in genre_list:
            if genre in mods_genre_uri_to_metajson_document_type:
                return mods_genre_uri_to_metajson_document_type[genre]
            elif genre in mods_genre_margt_to_metajson_document_type:
                return mods_genre_margt_to_metajson_document_type


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


def test():
    metajson_list = convert_mods_file_to_metajson_document_list("../test/data/mods.xml")
    file_export.export_metajson(metajson_list, "../test/data/result_mods_metajon.json")
    print json.dumps(metajson_list, indent = 4, ensure_ascii = False, encoding = "utf-8", sort_keys = True)
 

other_util.setup_console()
test()

