#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import xml.etree.ElementTree as ET

from biblib.metajson import Creator
from biblib.metajson import Document
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Resource
from biblib.metajson import Rights
from biblib.services import country_service
from biblib.services import creator_service
from biblib.services import date_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import constants
from biblib.util import jsonbson
from biblib.util import xmletree


####################
# MODS -> MetaJSON #
####################

MODS_PART_FIELDS = ["part_chapter_number", "part_chapter_title", "part_chronology", "part_column", "part_issue", "part_month", "part_name", "part_number", "part_page_begin", "part_page_end", "part_paragraph_number", "part_quarter", "part_season", "part_section_title", "part_session", "part_timecode_begin", "part_timecode_end", "part_track_number", "part_track_title", "part_volume", "part_week"]

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
    "loose-leaf": constants.DOC_TYPE_LOOSELEAFPUBLICATION,
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

# Last chance...
MODS_GENRE_FREE_TO_METAJSON_DOCUMENT_TYPE = {
    "journal article": constants.DOC_TYPE_JOURNALARTICLE,
    "Website": constants.DOC_TYPE_WEBSITE
}

MODS_TYPEOFRESOURCE_TO_METAJSON_DOCUMENT_TYPE = {
    "text": constants.DOC_TYPE_DOCUMENT,
    "cartographic": constants.DOC_TYPE_MAP,
    "notated music": constants.DOC_TYPE_MUSICALSCORE,
    "sound recording-musical": constants.DOC_TYPE_MUSICRECORDING,
    "sound recording-nonmusical": constants.DOC_TYPE_AUDIORECORDING,
    "sound recording": constants.DOC_TYPE_AUDIORECORDING,
    "still image": constants.DOC_TYPE_IMAGE,
    "moving image": constants.DOC_TYPE_VIDEORECORDING,
    "three dimensional object": constants.DOC_TYPE_PHYSICALOBJECT,
    "software, multimedia": constants.DOC_TYPE_SOFTWARE,
    "mixed material": constants.DOC_TYPE_MIXEDMATERIAL
}

METAJSON_DOCUMENT_TYPE_TO_MODS_TYPEOFRESOURCE = {
    constants.DOC_TYPE_ANCIENTTEXT : "text",
    constants.DOC_TYPE_ANNOTATIONARTICLE : "text",
    constants.DOC_TYPE_ARTICLEREVIEW : "text",
    constants.DOC_TYPE_ARTWORK : "still image",
    constants.DOC_TYPE_AUDIOBOOK : "sound recording-nonmusical",
    constants.DOC_TYPE_AUDIOBROADCAST : "sound recording",
    constants.DOC_TYPE_AUDIOPART : "sound recording",
    constants.DOC_TYPE_AUDIORECORDING : "sound recording",
    constants.DOC_TYPE_BIBLIOGRAPHY : "text",
    constants.DOC_TYPE_BILL : "text",
    constants.DOC_TYPE_BOOK : "text",
    constants.DOC_TYPE_BOOKLET : "text",
    constants.DOC_TYPE_BOOKPART : "text",
    constants.DOC_TYPE_BOOKREVIEW : "text",
    constants.DOC_TYPE_CASEBRIEF : "text",
    constants.DOC_TYPE_CHART : "still image",
    constants.DOC_TYPE_CODE : "text",
    constants.DOC_TYPE_COLLECTION : "mixed material",
    constants.DOC_TYPE_CONFERENCECONTRIBUTION : "text",
    constants.DOC_TYPE_CONFERENCEPAPER : "text",
    constants.DOC_TYPE_CONFERENCEPOSTER : "still image",
    constants.DOC_TYPE_CONFERENCEPROCEEDINGS : "text",
    constants.DOC_TYPE_COURTREPORTER : "text",
    constants.DOC_TYPE_CURRICULUMVITAE : "text",
    constants.DOC_TYPE_DATABASE : "software, multimedia",
    constants.DOC_TYPE_DATASET : "software, multimedia",
    constants.DOC_TYPE_DATASETQUALI : "software, multimedia",
    constants.DOC_TYPE_DATASETQUANTI : "software, multimedia",
    constants.DOC_TYPE_DICTIONARY : "text",
    constants.DOC_TYPE_DICTIONARYENTRY : "text",
    constants.DOC_TYPE_DISSERTATION : "text",
    constants.DOC_TYPE_DOCTORALTHESIS : "text",
    constants.DOC_TYPE_DOCUMENT : "text",
    constants.DOC_TYPE_DRAWING : "still image",
    constants.DOC_TYPE_EBOOK : "text",
    constants.DOC_TYPE_EDITEDBOOK : "text",
    constants.DOC_TYPE_EJOURNAL : "text",
    constants.DOC_TYPE_EJOURNALARTICLE : "text",
    constants.DOC_TYPE_EMAIL : "text",
    constants.DOC_TYPE_ENCYCLOPEDIA : "text",
    constants.DOC_TYPE_ENCYCLOPEDIAARTICLE : "text",
    constants.DOC_TYPE_ENGRAVE : "still image",
    constants.DOC_TYPE_EQUATION : "text",
    constants.DOC_TYPE_ERESOURCE : "text",
    constants.DOC_TYPE_EVENT : "mixed material",
    constants.DOC_TYPE_EXCERPT : "text",
    constants.DOC_TYPE_FILM : "moving image",
    constants.DOC_TYPE_FONT : "software, multimedia",
    constants.DOC_TYPE_GAME : "software, multimedia",
    constants.DOC_TYPE_GOVERNMENTPUBLICATION : "text",
    constants.DOC_TYPE_GRANT : "text",
    constants.DOC_TYPE_HEARING : "text",
    constants.DOC_TYPE_IMAGE : "still image",
    constants.DOC_TYPE_INSTANTMESSAGE : "text",
    constants.DOC_TYPE_INTERVIEWARTICLE : "text",
    constants.DOC_TYPE_JOURNAL : "text",
    constants.DOC_TYPE_JOURNALARTICLE : "text",
    constants.DOC_TYPE_KIT : "mixed material",
    constants.DOC_TYPE_LEGALCASE : "text",
    constants.DOC_TYPE_LEGALDECISION : "text",
    constants.DOC_TYPE_LETTER : "text",
    constants.DOC_TYPE_LOOSELEAFPUBLICATION : "text",
    constants.DOC_TYPE_MAGAZINE : "text",
    constants.DOC_TYPE_MAGAZINEARTICLE : "text",
    constants.DOC_TYPE_MANUEL : "text",
    constants.DOC_TYPE_MANUSCRIPT : "text",
    constants.DOC_TYPE_MAP : "cartographic",
    constants.DOC_TYPE_MASTERTHESIS : "text",
    constants.DOC_TYPE_MIXEDMATERIAL : "mixed material",
    constants.DOC_TYPE_MULTIMEDIA : "software, multimedia",
    constants.DOC_TYPE_MULTIVOLUMEBOOK : "text",
    constants.DOC_TYPE_MUSICALSCORE : "notated music",
    constants.DOC_TYPE_MUSICRECORDING : "sound recording-musical",
    constants.DOC_TYPE_NEWSPAPER : "text",
    constants.DOC_TYPE_NEWSPAPERARTICLE : "text",
    constants.DOC_TYPE_NOTE : "text",
    constants.DOC_TYPE_PAINTING : "still image",
    constants.DOC_TYPE_PATENT : "text",
    constants.DOC_TYPE_PERFORMANCE : "mixed material",
    constants.DOC_TYPE_PERIODICALISSUE : "text",
    constants.DOC_TYPE_PERSONALCOMMUNICATION : "text",
    constants.DOC_TYPE_PHOTOGRAPH : "still image",
    constants.DOC_TYPE_PHYSICALOBJECT : "three dimensional object",
    constants.DOC_TYPE_POSTER : "text",
    constants.DOC_TYPE_PREPRINT : "text",
    constants.DOC_TYPE_PRESSCLIPPING : "text",
    constants.DOC_TYPE_PROFESSORALTHESIS : "text",
    constants.DOC_TYPE_REPORT : "text",
    constants.DOC_TYPE_REPORTPART : "text",
    constants.DOC_TYPE_RESEARCHPROPOSAL : "text",
    constants.DOC_TYPE_SERIES : "text",
    constants.DOC_TYPE_SERVICE : "software, multimedia",
    constants.DOC_TYPE_SLIDE : "still image",
    constants.DOC_TYPE_SOFTWARE : "software, multimedia",
    constants.DOC_TYPE_SPEECH : "text",
    constants.DOC_TYPE_STANDARD : "text",
    constants.DOC_TYPE_STATUTE : "text",
    constants.DOC_TYPE_TREATY : "text",
    constants.DOC_TYPE_TECHREPORT : "text",
    constants.DOC_TYPE_TEST : "text",
    constants.DOC_TYPE_UNPUBLISHEDDOCUMENT : "text",
    constants.DOC_TYPE_VIDEOBROADCAST : "moving image",
    constants.DOC_TYPE_VIDEOPART : "moving image",
    constants.DOC_TYPE_VIDEORECORDING : "moving image",
    constants.DOC_TYPE_WEBARCHIVE : "software, multimedia",
    constants.DOC_TYPE_WEBCLUSTER : "software, multimedia",
    constants.DOC_TYPE_WEBENTITY : "software, multimedia",
    constants.DOC_TYPE_WEBPAGE : "software, multimedia",
    constants.DOC_TYPE_WEBPOST : "software, multimedia",
    constants.DOC_TYPE_WEBSECTION : "software, multimedia",
    constants.DOC_TYPE_WEBSITE : "software, multimedia",
    constants.DOC_TYPE_WORKINGPAPER : "text",
    constants.DOC_TYPE_WORKSHOP : "text"
}

METAJSON_DOCUMENT_TYPE_IS_MODS_COLLECTION = [
    constants.DOC_TYPE_COLLECTION,
    constants.DOC_TYPE_DATABASE,
    constants.DOC_TYPE_DICTIONARY,
    constants.DOC_TYPE_EDITEDBOOK,
    constants.DOC_TYPE_EJOURNAL,
    constants.DOC_TYPE_ENCYCLOPEDIA,
    constants.DOC_TYPE_JOURNAL,
    constants.DOC_TYPE_MAGAZINE,
    constants.DOC_TYPE_MULTIVOLUMEBOOK,
    constants.DOC_TYPE_NEWSPAPER,
    constants.DOC_TYPE_PERIODICALISSUE,
    constants.DOC_TYPE_SERIES,
    constants.DOC_TYPE_WEBCLUSTER,
    constants.DOC_TYPE_WEBENTITY,
    constants.DOC_TYPE_WEBSECTION
]

METAJSON_DOCUMENT_TYPE_IS_MODS_MANUSCRIPT = [
    constants.DOC_TYPE_ANCIENTTEXT,
    constants.DOC_TYPE_MANUSCRIPT
]

METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_EUREPO = {
    constants.DOC_TYPE_ANCIENTTEXT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_ANNOTATIONARTICLE : "info:eu-repo/semantics/annotation",
    constants.DOC_TYPE_ARTICLEREVIEW : "info:eu-repo/semantics/review",
    constants.DOC_TYPE_ARTWORK : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_AUDIOBOOK : "info:eu-repo/semantics/book",
    constants.DOC_TYPE_AUDIOBROADCAST : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_AUDIOPART : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_AUDIORECORDING : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_BIBLIOGRAPHY : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_BILL : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_BOOK : "info:eu-repo/semantics/book",
    constants.DOC_TYPE_BOOKLET : "info:eu-repo/semantics/book",
    constants.DOC_TYPE_BOOKPART : "info:eu-repo/semantics/bookPart",
    constants.DOC_TYPE_BOOKREVIEW : "info:eu-repo/semantics/bookReview",
    constants.DOC_TYPE_CASEBRIEF : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_CHART : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_CODE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_COLLECTION : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_CONFERENCECONTRIBUTION : "info:eu-repo/semantics/conferenceContribution",
    constants.DOC_TYPE_CONFERENCEPAPER : "info:eu-repo/semantics/conferencePaper",
    constants.DOC_TYPE_CONFERENCEPOSTER : "info:eu-repo/semantics/conferencePoster",
    constants.DOC_TYPE_CONFERENCEPROCEEDINGS : "info:eu-repo/semantics/conferenceProceedings",
    constants.DOC_TYPE_COURTREPORTER : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_CURRICULUMVITAE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_DATABASE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_DATASET : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_DATASETQUALI : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_DATASETQUANTI : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_DICTIONARY : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_DICTIONARYENTRY : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_DISSERTATION : "info:eu-repo/semantics/studentThesis",
    constants.DOC_TYPE_DOCTORALTHESIS : "info:eu-repo/semantics/doctoralThesis",
    constants.DOC_TYPE_DOCUMENT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_DRAWING : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_EBOOK : "info:eu-repo/semantics/book",
    constants.DOC_TYPE_EDITEDBOOK : "info:eu-repo/semantics/book",
    constants.DOC_TYPE_EJOURNAL : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_EJOURNALARTICLE : "info:eu-repo/semantics/article",
    constants.DOC_TYPE_EMAIL : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_ENCYCLOPEDIA : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_ENCYCLOPEDIAARTICLE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_ENGRAVE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_EQUATION : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_ERESOURCE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_EVENT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_EXCERPT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_FILM : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_FONT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_GAME : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_GOVERNMENTPUBLICATION : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_GRANT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_HEARING : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_IMAGE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_INSTANTMESSAGE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_INTERVIEWARTICLE : "info:eu-repo/semantics/article",
    constants.DOC_TYPE_JOURNAL : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_JOURNALARTICLE : "info:eu-repo/semantics/article",
    constants.DOC_TYPE_KIT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_LEGALCASE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_LEGALDECISION : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_LETTER : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_LOOSELEAFPUBLICATION : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_MAGAZINE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_MAGAZINEARTICLE : "info:eu-repo/semantics/contributionToPeriodical",
    constants.DOC_TYPE_MANUEL : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_MANUSCRIPT : "info:eu-repo/semantics/preprint",
    constants.DOC_TYPE_MAP : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_MASTERTHESIS : "info:eu-repo/semantics/masterThesis",
    constants.DOC_TYPE_MIXEDMATERIAL : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_MULTIMEDIA : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_MULTIVOLUMEBOOK : "info:eu-repo/semantics/book",
    constants.DOC_TYPE_MUSICALSCORE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_MUSICRECORDING : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_NEWSPAPER : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_NEWSPAPERARTICLE : "info:eu-repo/semantics/contributionToPeriodical",
    constants.DOC_TYPE_NOTE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_OFFPRINT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_PAINTING : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_PATENT : "info:eu-repo/semantics/patent",
    constants.DOC_TYPE_PERFORMANCE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_PERIODICALISSUE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_PERSONALCOMMUNICATION : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_PHOTOGRAPH : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_PHYSICALOBJECT : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_POSTER : "info:eu-repo/semantics/conferencePoster",
    constants.DOC_TYPE_PREPRINT : "info:eu-repo/semantics/preprint",
    constants.DOC_TYPE_PRESSCLIPPING : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_PROFESSORALTHESIS : "info:eu-repo/semantics/doctoralThesis",
    constants.DOC_TYPE_REPORT : "info:eu-repo/semantics/report",
    constants.DOC_TYPE_REPORTPART : "info:eu-repo/semantics/reportPart",
    constants.DOC_TYPE_RESEARCHPROPOSAL : "info:eu-repo/semantics/researchProposal",
    constants.DOC_TYPE_SERIES : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_SERVICE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_SLIDE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_SOFTWARE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_SPEECH : "info:eu-repo/semantics/lecture",
    constants.DOC_TYPE_STANDARD : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_STATUTE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_TREATY : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_TECHREPORT : "info:eu-repo/semantics/technicalDocumentation",
    constants.DOC_TYPE_TEST : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_UNPUBLISHEDDOCUMENT : "info:eu-repo/semantics/preprint",
    constants.DOC_TYPE_VIDEOBROADCAST : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_VIDEOPART : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_VIDEORECORDING : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_WEBARCHIVE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_WEBCLUSTER : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_WEBENTITY : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_WEBPAGE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_WEBPOST : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_WEBSECTION : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_WEBSITE : "info:eu-repo/semantics/other",
    constants.DOC_TYPE_WORKINGPAPER : "info:eu-repo/semantics/workingPaper",
    constants.DOC_TYPE_WORKSHOP : "info:eu-repo/semantics/other"
}

METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_EPRINT = {
    constants.DOC_TYPE_ANNOTATIONARTICLE : "http://purl.org/eprint/type/JournalArticle",
    constants.DOC_TYPE_ARTICLEREVIEW : "http://purl.org/eprint/type/JournalArticle",
    constants.DOC_TYPE_BOOK : "http://purl.org/eprint/type/Book",
    constants.DOC_TYPE_BOOKLET : "http://purl.org/eprint/type/Book",
    constants.DOC_TYPE_BOOKPART : "http://purl.org/eprint/type/BookItem",
    constants.DOC_TYPE_BOOKREVIEW : "http://purl.org/eprint/type/JournalArticle",
    constants.DOC_TYPE_CONFERENCECONTRIBUTION : "http://purl.org/eprint/type/ConferenceItem",
    constants.DOC_TYPE_CONFERENCEPAPER : "http://purl.org/eprint/type/ConferencePaper",
    constants.DOC_TYPE_CONFERENCEPOSTER : "http://purl.org/eprint/type/ConferencePoster",
    constants.DOC_TYPE_CONFERENCEPROCEEDINGS : "http://purl.org/eprint/type/Book",
    constants.DOC_TYPE_DOCTORALTHESIS : "http://purl.org/eprint/type/Thesis",
    constants.DOC_TYPE_EBOOK : "http://purl.org/eprint/type/Book",
    constants.DOC_TYPE_EDITEDBOOK : "http://purl.org/eprint/type/Book",
    constants.DOC_TYPE_EJOURNALARTICLE : "http://purl.org/eprint/type/JournalArticle",
    constants.DOC_TYPE_INTERVIEWARTICLE : "http://purl.org/eprint/type/JournalArticle",
    constants.DOC_TYPE_JOURNALARTICLE : "http://purl.org/eprint/type/JournalArticle",
    constants.DOC_TYPE_MAGAZINEARTICLE : "http://purl.org/eprint/type/NewsItem",
    constants.DOC_TYPE_MASTERTHESIS : "http://purl.org/eprint/type/Thesis",
    constants.DOC_TYPE_MULTIVOLUMEBOOK : "http://purl.org/eprint/type/Book",
    constants.DOC_TYPE_NEWSPAPERARTICLE : "http://purl.org/eprint/type/NewsItem",
    constants.DOC_TYPE_PATENT : "http://purl.org/eprint/type/Patent",
    constants.DOC_TYPE_PERIODICALISSUE : "http://purl.org/eprint/type/JournalItem",
    constants.DOC_TYPE_PREPRINT : "http://purl.org/eprint/type/SubmittedJournalArticle",
    constants.DOC_TYPE_PROFESSORALTHESIS : "http://purl.org/eprint/type/Thesis",
    constants.DOC_TYPE_REPORT : "http://purl.org/eprint/type/Report",
    constants.DOC_TYPE_REPORTPART : "http://purl.org/eprint/type/Report",
    constants.DOC_TYPE_SPEECH : "http://purl.org/eprint/type/ConferenceItem",
    constants.DOC_TYPE_TECHREPORT : "http://purl.org/eprint/type/Report",
    constants.DOC_TYPE_WORKINGPAPER : "http://purl.org/eprint/type/WorkingPaper"
}

METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_MARCGT = {
    constants.DOC_TYPE_ANNOTATIONARTICLE : "legal article",
    constants.DOC_TYPE_ARTICLEREVIEW : "review",
    constants.DOC_TYPE_ARTWORK : "art original",
    constants.DOC_TYPE_AUDIOBOOK : "book",
    constants.DOC_TYPE_AUDIOBROADCAST : "sound",
    constants.DOC_TYPE_AUDIOPART : "sound",
    constants.DOC_TYPE_AUDIORECORDING : "sound",
    constants.DOC_TYPE_BIBLIOGRAPHY : "bibliography",
    constants.DOC_TYPE_BILL : "legislation",
    constants.DOC_TYPE_BOOK : "book",
    constants.DOC_TYPE_BOOKLET : "book",
    constants.DOC_TYPE_BOOKREVIEW : "review",
    constants.DOC_TYPE_CASEBRIEF : "legal case and case notes",
    constants.DOC_TYPE_CHART : "chart",
    constants.DOC_TYPE_CONFERENCEPROCEEDINGS : "book",
    constants.DOC_TYPE_COURTREPORTER : "law report or digest",
    constants.DOC_TYPE_DATABASE : "database",
    constants.DOC_TYPE_DATASET : "numeric data",
    constants.DOC_TYPE_DATASETQUALI : "numeric data",
    constants.DOC_TYPE_DATASETQUANTI : "numeric data",
    constants.DOC_TYPE_DICTIONARY : "dictionary",
    constants.DOC_TYPE_DISSERTATION : "thesis",
    constants.DOC_TYPE_DOCTORALTHESIS : "thesis",
    constants.DOC_TYPE_DRAWING : "art original",
    constants.DOC_TYPE_EBOOK : "book",
    constants.DOC_TYPE_EDITEDBOOK : "book",
    constants.DOC_TYPE_EJOURNAL : "journal",
    constants.DOC_TYPE_EJOURNALARTICLE : "article",
    constants.DOC_TYPE_ENCYCLOPEDIA : "encyclopedia",
    constants.DOC_TYPE_FILM : "motion picture",
    constants.DOC_TYPE_FONT : "font",
    constants.DOC_TYPE_GAME : "game",
    constants.DOC_TYPE_GOVERNMENTPUBLICATION : "government publication",
    constants.DOC_TYPE_IMAGE : "picture",
    constants.DOC_TYPE_INTERVIEWARTICLE : "interview",
    constants.DOC_TYPE_JOURNAL : "journal",
    constants.DOC_TYPE_JOURNALARTICLE : "article",
    constants.DOC_TYPE_KIT : "kit",
    constants.DOC_TYPE_LEGALCASE : "legal case and case notes",
    constants.DOC_TYPE_LEGALDECISION : "legal case and case notes",
    constants.DOC_TYPE_LETTER : "letter",
    constants.DOC_TYPE_LOOSELEAFPUBLICATION : "loose-leaf",
    constants.DOC_TYPE_MAGAZINE : "periodical",
    constants.DOC_TYPE_MAGAZINEARTICLE : "article",
    constants.DOC_TYPE_MANUEL : "handbook",
    constants.DOC_TYPE_MAP : "map",
    constants.DOC_TYPE_MASTERTHESIS : "thesis",
    constants.DOC_TYPE_MIXEDMATERIAL : "kit",
    constants.DOC_TYPE_MULTIVOLUMEBOOK : "multivolume monograph",
    constants.DOC_TYPE_MUSICRECORDING : "sound",
    constants.DOC_TYPE_NEWSPAPER : "newspaper",
    constants.DOC_TYPE_NEWSPAPERARTICLE : "article",
    constants.DOC_TYPE_OFFPRINT : "offprint",
    constants.DOC_TYPE_PAINTING : "art original",
    constants.DOC_TYPE_PATENT : "patent",
    constants.DOC_TYPE_PERIODICALISSUE : "issue",
    constants.DOC_TYPE_PHOTOGRAPH : "picture",
    constants.DOC_TYPE_PROFESSORALTHESIS : "thesis",
    constants.DOC_TYPE_REPORT : "report",
    constants.DOC_TYPE_SERIES : "series",
    constants.DOC_TYPE_SERVICE : "online system or service",
    constants.DOC_TYPE_SLIDE : "slide",
    constants.DOC_TYPE_SOFTWARE : "programmed text",
    constants.DOC_TYPE_SPEECH : "speech",
    constants.DOC_TYPE_STANDARD : "standard or specification",
    constants.DOC_TYPE_STATUTE : "legislation",
    constants.DOC_TYPE_TREATY : "treaty",
    constants.DOC_TYPE_TECHREPORT : "technical report",
    constants.DOC_TYPE_UNPUBLISHEDDOCUMENT : "preprint",
    constants.DOC_TYPE_VIDEOBROADCAST : "videorecording",
    constants.DOC_TYPE_VIDEOPART : "videorecording",
    constants.DOC_TYPE_VIDEORECORDING : "videorecording",
    constants.DOC_TYPE_WEBARCHIVE : "web site",
    constants.DOC_TYPE_WEBCLUSTER : "web site",
    constants.DOC_TYPE_WEBENTITY : "web site",
    constants.DOC_TYPE_WEBPAGE : "web site",
    constants.DOC_TYPE_WEBPOST : "web site",
    constants.DOC_TYPE_WEBSECTION : "web site",
    constants.DOC_TYPE_WEBSITE : "web site"
}

METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_OTHER = {
    constants.DOC_TYPE_ANCIENTTEXT : "ancient text",
    constants.DOC_TYPE_BOOKPART : "book chapter",
    constants.DOC_TYPE_CODE : "code",
    constants.DOC_TYPE_COLLECTION : "collection",
    constants.DOC_TYPE_CONFERENCECONTRIBUTION : "conference contribution",
    constants.DOC_TYPE_CONFERENCEPAPER : "conference paper",
    constants.DOC_TYPE_CONFERENCEPOSTER : "conference poster",
    constants.DOC_TYPE_CURRICULUMVITAE : "other",
    constants.DOC_TYPE_DICTIONARYENTRY : "dictionary entry",
    constants.DOC_TYPE_DOCUMENT : "other",
    constants.DOC_TYPE_EMAIL : "email",
    constants.DOC_TYPE_ENCYCLOPEDIAARTICLE : "encyclopedia article",
    constants.DOC_TYPE_ENGRAVE : "engrave",
    constants.DOC_TYPE_EQUATION : "equation",
    constants.DOC_TYPE_ERESOURCE : "eresource",
    constants.DOC_TYPE_EVENT : "event",
    constants.DOC_TYPE_EXCERPT : "excerpt",
    constants.DOC_TYPE_GRANT : "grant",
    constants.DOC_TYPE_HEARING : "hearing",
    constants.DOC_TYPE_INSTANTMESSAGE : "instant message",
    constants.DOC_TYPE_MANUSCRIPT : "manuscript",
    constants.DOC_TYPE_MULTIMEDIA : "multimedia",
    constants.DOC_TYPE_MUSICALSCORE : "musical score",
    constants.DOC_TYPE_NOTE : "note",
    constants.DOC_TYPE_PERFORMANCE : "performance",
    constants.DOC_TYPE_PERSONALCOMMUNICATION : "personal communication",
    constants.DOC_TYPE_PHYSICALOBJECT : "physical object",
    constants.DOC_TYPE_POSTER : "poster",
    constants.DOC_TYPE_PREPRINT : "preprint",
    constants.DOC_TYPE_PRESSCLIPPING : "press clipping",
    constants.DOC_TYPE_REPORTPART : "report part",
    constants.DOC_TYPE_RESEARCHPROPOSAL : "research proposal",
    constants.DOC_TYPE_TEST : "test",
    constants.DOC_TYPE_WORKINGPAPER : "working paper",
    constants.DOC_TYPE_WORKSHOP : "workshop"
}

def mods_xmletree_to_metajson_list(mods_root, source, rec_id_prefix, only_first_record):
    """  MODS xmletree -> MetaJSON Document list"""
    if mods_root is not None:
        if mods_root.tag.endswith("mods"):
            yield mods_xmletree_to_metajson(mods_root, source, rec_id_prefix)
        elif mods_root.tag.endswith("modsCollection"):
            mods_list = mods_root.findall(xmletree.prefixtag("mods", "mods"))
            if mods_list:
                for mods in mods_list:
                    yield mods_xmletree_to_metajson(mods, source, rec_id_prefix)


def mods_xmletree_to_metajson(mods, source, rec_id_prefix):
    """ MODS xmletree -> MetaJSON Document """
    if mods is None:
        return None

    # @version -> null
    #mods_version = mods.get("version")
    #logging.debug("# mods_version: {}".format(mods_version))

    document = mods_root_or_related_item_to_metajson(mods, None)

    # source
    if source:
        document["rec_source"] = source

    metajson_service.pretty_print_document(document)
    return document


def mods_root_or_related_item_to_metajson(mods, root_rec_type):
    """ MODS root or relatedItem -> MetaJSON Document """
    if mods is None:
        return None

    #logging.debug("root_rec_type: {}".format(root_rec_type))

    document = Document()

    # related_item_type
    related_item_type = mods.get("type")

    # typeOfResource, genre -> rec_type, genres
    rec_type = None
    document.update(get_mods_genres_type_of_resources(mods))
    if "rec_type" not in document:
        if related_item_type == "original":
            # In case of original relatedItem
            rec_type = root_rec_type
        elif related_item_type == "host" and root_rec_type is not None and root_rec_type in constants.root_rec_type_to_is_part_of_rec_type:
            # In case of host relatedItem
            rec_type = constants.root_rec_type_to_is_part_of_rec_type[root_rec_type]
        else:
            # Default
            rec_type = constants.DOC_TYPE_DOCUMENT
        document["rec_type"] = rec_type
    else:
        rec_type = document["rec_type"]

    # identifier, ID -> rec_id, identifiers
    document.update(get_mods_identifiers_and_rec_id(mods))

    # titleInfo -> title, title_non_sort, title_sub, part_number, part_name,
    # title_abbreviateds, title_alternatives, title_translateds, title_uniforms
    document.update(get_mods_title_infos(mods))

    # name, extension/daiList -> creators[]
    document.update(get_mods_names(mods))

    # originInfo -> 
    # date_issued, date_created, date_captured, date_valid, date_modified, date_copyrighted, date_other,
    # edition, frequency, issuance, publication_countries, publication_places, publishers
    document.update(get_mods_origin_info(mods))

    # language/languageTerm -> languages
    document.update(get_mods_languages(mods))

    # physicalDescription ->
    # extent_duration, extent_dimension, extent_pages, form, physical_description_notes, reformatting_quality
    document.update(get_mods_physical_description(mods, rec_type))

    # abstract -> descriptions
    document.update(get_mods_abstracts(mods))

    # tableOfContents -> table_of_contentss
    document.update(get_mods_table_of_contentss(mods))

    # targetAudience -> target_audiences
    document.update(get_mods_target_audiences(mods))

    # note -> notes
    document.update(get_mods_notes(mods))

    # subject -> keywords, subjects
    document.update(get_mods_subjects(mods))

    # classification -> classifications, peer_review, peer_review_geo, citation_databases, expert_committees
    document.update(get_mods_classifications(mods))

    # relatedItem -> ...
    document.update(get_mods_related_items(mods, rec_type))

    # location -> resources
    document.update(get_mods_locations(mods))

    # accessCondition -> rights
    document.update(get_mods_access_conditions(mods))

    # part/detail/number -> part_chapter_number, part_issue, part_paragraph_number, part_track_number, part_volume
    # part/detail/title -> part_chapter_title, part_section_title, part_track_title
    # part/extent/start -> part_page_begin, part_timecode_begin
    # part/extent/end -> part_page_end, part_timecode_end
    document.update(get_mods_parts(mods))

    # extension
    # dailist is managed by the function get_mods_names

    # recordInfo -> rec_ 
    document.update(get_mods_record_info(mods))

    return document


def get_mods_genres_type_of_resources(mods):
    """ genre, typeOfResource -> rec_type, genres """
    rec_type = None
    genres = []

    # genre
    mods_genres = mods.findall(xmletree.prefixtag("mods", "genre"))
    if mods_genres:
        genre_eurepo = None
        genre_eprint = None
        genre_marcgt = None
        genre_free = None
        for mods_genre in mods_genres:
            if mods_genre.text is not None:
                genre_value = mods_genre.text.strip()
                genre_authority = mods_genre.get("authority")
                genre_type = mods_genre.get("type")
                # text
                if genre_value.startswith("info:eu-repo/semantics/"):
                    # last occurrence of eu-repo
                    genre_eurepo = genre_value
                elif genre_value.startswith("http://purl.org/eprint/type/"):
                    # last occurrence of eprint
                    genre_eprint = genre_value
                elif genre_marcgt is None and genre_value in MODS_GENRE_MARCGT_TO_METAJSON_DOCUMENT_TYPE:
                    # first occurrence of marcgt
                    genre_marcgt = genre_value
                elif genre_value in MODS_GENRE_FREE_TO_METAJSON_DOCUMENT_TYPE:
                    # last chance...
                    genre_free = genre_value
                else:
                    genre = {}
                    genre["value"] = genre_value
                    if genre_authority:
                        # authority
                        genre["authority"] = genre_authority
                    if genre_type:
                        # type (examples: class, work type, or style)
                        genre["type"] = genre_type
                    genres.append(genre)
        # rec_type is based on authorities by order: eu-repo, eprint, marcgt, free
        if genre_eurepo:
            rec_type = MODS_GENRE_EUREPO_TO_METAJSON_DOCUMENT_TYPE[genre_eurepo]
        elif rec_type is None and genre_eprint:
            rec_type = MODS_GENRE_EPRINT_TO_METAJSON_DOCUMENT_TYPE[genre_eprint]
        elif rec_type is None and genre_marcgt:
            rec_type = MODS_GENRE_MARCGT_TO_METAJSON_DOCUMENT_TYPE[genre_marcgt]
        elif rec_type is None and genre_free:
            rec_type = MODS_GENRE_FREE_TO_METAJSON_DOCUMENT_TYPE[genre_free]

    # typeOfResource
    if rec_type is None:
        rml_type_of_resource = mods.find(xmletree.prefixtag("mods", "typeOfResource"))
        if rml_type_of_resource is not None:
            type_of_resource_value = xmletree.get_element_text(rml_type_of_resource)
            #type_of_resource_collection = xmletree.get_element_attribute(rml_type_of_resource, "collection")
            type_of_resource_manuscript = xmletree.get_element_attribute(rml_type_of_resource, "manuscript")
            if type_of_resource_manuscript == "yes":
                rec_type = constants.DOC_TYPE_MANUSCRIPT
            elif type_of_resource_value in MODS_TYPEOFRESOURCE_TO_METAJSON_DOCUMENT_TYPE:
                rec_type = MODS_TYPEOFRESOURCE_TO_METAJSON_DOCUMENT_TYPE[type_of_resource_value]

    result = {}
    if rec_type:
        result["rec_type"] = rec_type
    else:
        result["rec_type"] = constants.DOC_TYPE_DOCUMENT
    if genres:
        result["genres"] = genres
    return result


def get_mods_abstracts(mods):
    """ abstract -> descriptions """
    result = {}
    mods_abstracts = mods.findall(xmletree.prefixtag("mods", "abstract"))
    if mods_abstracts is not None:
        descriptions = convert_mods_string_langs(mods_abstracts)
        if descriptions:
            result["descriptions"] = descriptions
    return result


def get_mods_access_conditions(mods):
    """ accessCondition -> rights """
    result = {}
    mods_access_conditions = mods.findall(xmletree.prefixtag("mods", "accessCondition"))
    if mods_access_conditions is not None:
        mods_type_to_metajson_type  = {
            "restriction on access": "display",
            "use and reproduction": "print"
        }
        permissions = []
        for mods_access_condition in mods_access_conditions:
            if mods_access_condition is not None and mods_access_condition.text is not None:
                description_value = mods_access_condition.text.strip()
                description_language = mods_access_condition.get("lang")
                mods_permission_type = mods_access_condition.get("type")
                if description_value is not None:
                    description = {"value": description_value}
                    if description_language is not None:
                        description["language"] = description_language.strip()
                    permission_type = "other"
                    if mods_permission_type is not None and mods_permission_type in mods_type_to_metajson_type:
                        permission_type = mods_type_to_metajson_type[mods_permission_type]
                    permissions.append({"permission_type": permission_type, "descriptions": [description]})
        if permissions:
            rights = Rights()
            rights["rights_type"] = "unknown"
            rights["permissions"] = permissions
            result["rights"] = rights
    return result


def get_mods_classifications(mods):
    """ classification -> classifications, peer_review, peer_review_geo, citation_databases, expert_committees """
    result = {}
    mods_classifications = mods.findall(xmletree.prefixtag("mods", "classification"))
    if mods_classifications is not None:
        classifications_dict = {}
        peer_review = False
        peer_review_geo = []
        citation_databases = []
        expert_committees = []
        for mods_classification in mods_classifications:
            if mods_classification is not None:
                mods_classification_authority = mods_classification.get("authority")
                #mods_classification_lang = mods_classification.get("lang")
                if mods_classification.text is not None:
                    if mods_classification_authority is None:
                        mods_classification_authority = constants.CLASSIFICATION_UNDETERMINED
                    if mods_classification_authority == "peer-review" and mods_classification.text == "yes":
                        # peer_review
                        peer_review = True
                    elif mods_classification_authority == "peer-review-geo":
                        # peer_review_geo
                        peer_review_geo.append(mods_classification.text.strip())
                    elif mods_classification_authority == "citation-databases":
                        # citation_databases
                        citation_databases.append(mods_classification.text.strip())
                    elif mods_classification_authority == "expert-committee":
                        # expert_committees
                        expert_committees.append(mods_classification.text.strip())
                    else:
                        if mods_classification_authority not in classifications_dict:
                            classifications_dict[mods_classification_authority] = []
                        classifications_dict[mods_classification_authority].append({"term_id":mods_classification.text.strip()})

        if classifications_dict:
            result["classifications"] = classifications_dict
        if peer_review:
            result["peer_review"] = peer_review
        if peer_review_geo:
            result["peer_review_geo"] = peer_review_geo
        if citation_databases:
            result["citation_databases"] = citation_databases
        if expert_committees:
            result["expert_committees"] = expert_committees
    return result


def get_mods_identifiers_and_rec_id(mods):
    """ identifier, ID -> rec_id, identifiers """
    result = {}

    # rec_id
    rec_id = None
    mods_id = mods.get("ID")
    if mods_id is not None:
        rec_id = mods_id
    else:
        pass

    # identifiers
    mods_identifiers = mods.findall(xmletree.prefixtag("mods", "identifier"))
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


def get_mods_languages(mods):
    """ language/languageTerm -> languages """
    result = {}
    mods_languages = mods.findall(xmletree.prefixtag("mods", "language"))
    if mods_languages is not None:
        languages = []
        for mods_language in mods_languages:
            if mods_language is not None:
                mods_terms = mods_language.findall(xmletree.prefixtag("mods", "languageTerm"))
                if mods_terms is not None:
                    language = None
                    for mods_term in mods_terms:
                        # only one languageTerm by language is parsed
                        if mods_term.text is not None and language is None:
                            mods_term_value = mods_term.text.strip()
                            if mods_term.get("type") == "code":
                                # code
                                if mods_term.get("authority") in ["rfc3066", "rfc4646", "rfc5646"]:
                                    # rfc5646
                                    language = language_service.extract_rfc5646_language(mods_term_value)

                                elif mods_term.get("authority") == "iso639-2b":
                                    # iso639-2b
                                    language = language_service.convert_iso639_2b_to_rfc5646(mods_term_value)

                                elif mods_term.get("authority") == "iso639-3":
                                    # iso639-3
                                    # todo
                                    language = language_service.convert_unknown_format_to_rfc5646(mods_term_value)
                            else:
                                # text: natural language like french or english
                                language = language_service.convert_unknown_format_to_rfc5646(mods_term_value)
                    if language:
                        languages.append(language)
        if languages:
            result["languages"] = languages
    return result


def get_mods_locations(mods):
    """ location -> resources """
    result = {}
    locations = mods.findall(xmletree.prefixtag("mods", "location"))
    if locations is not None:
        resources = []
        for location in locations:
            if location is not None:
                resource = Resource()
                # url -> remote
                mods_url = location.find(xmletree.prefixtag("mods", "url"))
                if mods_url is not None:
                    url = mods_url.text.strip()
                    date_last_accessed = mods_url.get("dateLastAccessed")
                    if url:
                        resource["rec_type"] = "remote"
                        resource["url"] = url
                        if date_last_accessed is not None:
                            resource["dateLastAccessed"] = date_last_accessed.strip()

                # todo
                # physicalLocation
                # shelfLocator
                # holdingSimple
                # holdingExternal

                resources.append(resource)
        if resources:
            result["resources"] = resources
    return result


def get_mods_names(mods):
    """ name, extension/daiList -> creators list """
    result = {}
    mods_names = mods.findall(xmletree.prefixtag("mods", "name"))
    if mods_names:
        dai_dict = get_mods_dailist_as_dict(mods)
        creators = []
        for mods_name in mods_names:
            creator = convert_mods_name_dai_dict_to_creator(mods_name, dai_dict)
            if creator is not None:
                creators.append(creator)
        if creators:
            result["creators"] = creators
    return result


def get_mods_dailist_as_dict(mods):
    """ extension/daiList -> temporary dict """
    mods_extension = mods.find(xmletree.prefixtag("mods", "extension"))
    if mods_extension is not None:
        mods_dai_list = mods_extension.find(xmletree.prefixtag("dai", "daiList"))
        if mods_dai_list is not None:
            mods_dai_identifiers = mods_dai_list.findall(xmletree.prefixtag("dai", "identifier"))
            if mods_dai_identifiers:
                result = {}
                for mods_dai_identifier in mods_dai_identifiers:
                    authority = mods_dai_identifier.get("authority")
                    dai = mods_dai_identifier.text.strip()
                    result[mods_dai_identifier.get("IDref")] = {"authority": authority, "value": dai}
                return result


def convert_mods_name_dai_dict_to_creator(mods_name, dai_dict):
    """ name, extension/daiList -> creator """
    if mods_name is not None:
        creator = Creator()
        # extract mods properties
        # type
        mods_name_type = mods_name.get("type")
        # ID
        mods_name_id = mods_name.get("ID")
        # namePart
        mods_name_parts = mods_name.findall(xmletree.prefixtag("mods", "namePart"))
        # affiliation
        mods_name_affiliations = mods_name.findall(xmletree.prefixtag("mods", "affiliation"))
        # role
        mods_name_role = mods_name.find(xmletree.prefixtag("mods", "role"))
        mods_name_roleterm = None
        if mods_name_role is not None:
            mods_name_roleterm = mods_name_role.find(xmletree.prefixtag("mods", "roleTerm"))
        # description
        mods_name_descriptions = mods_name.findall(xmletree.prefixtag("mods", "description"))

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
            # logging.debug("personal")
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
            # logging.debug("corporate")
            orgunit = Orgunit()
            creator["agent"] = orgunit

            if mods_name_parts:
                orgunit["name"] = mods_name_parts[0].text.strip()

        elif mods_name_type == "conference":
            # logging.debug("conference")
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
                            event["date_begin"] = date
                        else:
                            event["date_begin"] = date[:slash_index]
                            event["date_end"] = date[slash_index+1:]

        elif mods_name_type == "family":
            # logging.debug("family")
            family = Family()
            creator["agent"] = family

            if mods_name_parts:
                orgunit["name"] = mods_name_parts[0].text.strip()

        if affiliation:
            creator["affiliations"] = [affiliation]

        if mods_name_roleterm is not None:
            creator["roles"] = convert_mods_name_roleterm(mods_name_roleterm)

        #logging.debug("{} {} {} {} {} {}".format(name_type, name_id, name_parts, name_affiliations, name_roleterm, name_descriptions))
        return creator


def convert_mods_name_roleterm(mods_roleterm):
    """ role/roleTerm -> role """
    if mods_roleterm is not None:
        authority = mods_roleterm.get("authority")
        term_type = mods_roleterm.get("type")
        value = mods_roleterm.text.strip()
        # logging.debug("{} {} {}".format(authority, term_type, value))
        if not value:
            # default creator role
            return ["cre"]
        else:
            if authority == "marcrelator":
                if term_type == "code":
                    return [value]
                elif value in creator_service.role_text_to_role_code:
                    return [creator_service.role_text_to_role_code[value]]
                else:
                    return ["cre"]
            elif authority == "unimarc" and value in creator_service.role_unimarc_to_role_code:
                return [creator_service.role_unimarc_to_role_code[value]]
            else:
                return ["cre"]
    else:
        return ["cre"]


def get_mods_notes(mods):
    """ note -> notes  """
    result = {}
    mods_notes = mods.findall(xmletree.prefixtag("mods", "note"))
    if mods_notes is not None:
        notes = convert_mods_string_lang_types(mods_notes, "note_type")
        if notes:
            result["notes"] = notes
    return result


def get_mods_origin_info(mods):
    """ originInfo -> 
        date_issued, date_created, date_captured, date_valid, date_modified, date_copyrighted, date_other,
        edition, frequency, issuance, publication_countries, publication_places, publishers
    """
    mods_origin_info = mods.find(xmletree.prefixtag("mods", "originInfo"))
    result = {}
    if mods_origin_info is not None:
        # dateIssued -> date_issued
        date_issued = convert_mods_date(mods_origin_info.find(xmletree.prefixtag("mods", "dateIssued")))
        if date_issued:
            result["date_issued"] = date_issued

        # dateCreated -> date_created
        date_created = convert_mods_date(mods_origin_info.find(xmletree.prefixtag("mods", "dateCreated")))
        if date_created:
            result["date_created"] = date_created

        # dateCaptured -> date_captured
        date_captured = convert_mods_date(mods_origin_info.find(xmletree.prefixtag("mods", "dateCaptured")))
        if date_captured:
            result["date_captured"] = date_captured

        # dateValid -> date_valid
        date_valid = convert_mods_date(mods_origin_info.find(xmletree.prefixtag("mods", "dateValid")))
        if date_valid:
            result["date_valid"] = date_valid

        # dateModified -> date_modified
        date_modified = convert_mods_date(mods_origin_info.find(xmletree.prefixtag("mods", "dateModified")))
        if date_modified:
            result["date_modified"] = date_modified

        # copyrightDate -> date_copyrighted
        date_copyrighted = convert_mods_date(mods_origin_info.find(xmletree.prefixtag("mods", "copyrightDate")))
        if date_copyrighted:
            result["date_copyrighted"] = date_copyrighted

        # dateOther -> date_other
        date_other = convert_mods_date(mods_origin_info.find(xmletree.prefixtag("mods", "dateOther")))
        if date_other:
            result["date_other"] = date_other

        # edition -> edition
        mods_edition = mods_origin_info.find(xmletree.prefixtag("mods", "edition"))
        if mods_edition is not None:
            result["edition"] = mods_edition.text.strip()

        # frequency -> frequency
        mods_frequency = mods_origin_info.find(xmletree.prefixtag("mods", "frequency"))
        if mods_frequency is not None:
            result["frequency"] = mods_frequency.text.strip()

        # issuance -> issuance
        mods_issuance = mods_origin_info.find(xmletree.prefixtag("mods", "issuance"))
        if mods_issuance is not None:
            result["issuance"] = mods_issuance.text.strip()

        # place/placeTerm -> publication_countries, publication_places
        mods_places = mods_origin_info.findall(xmletree.prefixtag("mods", "place"))
        if mods_places is not None:
            publication_countries = []
            publication_places = []
            for mods_place in mods_places:
                if mods_place is not None:
                    mods_place_term = mods_place.find(xmletree.prefixtag("mods", "placeTerm"))
                    if mods_place_term is not None:
                        place_value = mods_place_term.text.strip()
                        #place_type = mods_place_term.get("type")
                        place_authority = mods_place_term.get("authority")
                        if place_value:
                            if place_authority == "iso3166" and place_value in country_service.iso3166_alpha3_list:
                                publication_countries.append(place_value)
                            elif place_authority == "marccountry" and place_value in country_service.marccountry_to_iso3166_alpha2:
                                publication_countries.append(country_service.marccountry_to_iso3166_alpha2[place_value])
                            elif place_authority == "marcgac" and place_value in country_service.marcgac_to_iso3166_alpha2:
                                publication_countries.append(country_service.marcgac_to_iso3166_alpha2[place_value])
                            else:
                                publication_places.append(place_value)
            if publication_countries:
                result["publication_countries"] = publication_countries
            if publication_places:
                result["publication_places"] = publication_places

        # publisher -> publishers
        mods_publishers = mods_origin_info.findall(xmletree.prefixtag("mods", "publisher"))
        if mods_publishers is not None:
            publishers = []
            for mods_publisher in mods_publishers:
                if mods_publisher is not None:
                    publishers.append(mods_publisher.text.strip())
            if publishers:
                result["publishers"] = publishers

    return result


def get_mods_physical_description(mods, rec_type):
    """ physicalDescription ->
        extent_duration, extent_dimension, extent_pages, form, physical_description_notes, reformatting_quality
    """
    result = {}
    mods_physical_description = mods.find(xmletree.prefixtag("mods", "physicalDescription"))
    if mods_physical_description is not None:

        # digitalOrigin -> digital_origin
        result.update(get_mods_element_text_and_set_key(mods_physical_description, "digitalOrigin", "digital_origin"))

        # extent -> extent_duration, extent_dimension, extent_pages
        extent = get_mods_element_text(mods_physical_description, "extent")
        if extent:
            if rec_type in ["AudioBook", "AudioBroadcast", "AudioRecording", "MusicRecording", "VideoBroadcast", "VideoRecording", "VideoPart"]:
                result["extent_duration"] = extent
            elif rec_type in ["PhysicalObject"]:
                result["extent_dimension"] = extent
            else:
                result["extent_pages"] = extent

        # form -> form
        mods_form = mods_physical_description.find(xmletree.prefixtag("mods", "form"))
        if mods_form is not None:
            value = xmletree.get_element_text(mods_form)
            if value:
                # text -> value
                form = {"value": value}
                if mods_form.get("authority"):
                    # authority -> authority
                    form["authority"] = mods_form.get("authority")
                if mods_form.get("type"):
                    # type -> type
                    form["type"] = mods_form.get("type")
                result["form"] = form

        # internetMediaType -> null

        # note -> physical_description_notes
        mods_notes = mods_physical_description.findall(xmletree.prefixtag("mods", "note"))
        if mods_notes is not None:
            notes = convert_mods_string_langs(mods_notes)
            if notes:
                result["physical_description_notes"] = notes

        # reformattingQuality -> reformatting_quality
        result.update(get_mods_element_text_and_set_key(mods_physical_description, "reformattingQuality", "reformatting_quality"))
    return result


def get_mods_related_items(mods_root, root_rec_type):
    """ relatedItem ->
        is_part_ofs, has_parts, is_review_ofs, originals, seriess, is_referenced_bys, references,
        is_format_ofs, is_version_ofs, is_preceded_bys, is_succeeded_bys
    """
    mods_related_items = mods_root.findall(xmletree.prefixtag("mods", "relatedItem"))
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

                    #logging.debug("root_rec_type: {} related_item_rec_type: {} mods_related_item_type: {} ".format(root_rec_type, related_item_rec_type, mods_related_item_type))

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
                            # original -> is_review_ofs
                            result.add_item_to_key(related_item, "is_review_ofs")
                        else:
                            # original -> originals
                            result.add_item_to_key(related_item, "originals")

                    elif mods_related_item_type == "reviewOf":

                        # reviewOf -> is_review_ofs
                        result.add_item_to_key(related_item, "is_review_ofs")

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

                        # otherVersion -> has_versions
                        result.add_item_to_key(related_item, "has_versions")

                    elif mods_related_item_type == "preceding":

                        # preceding -> is_preceded_bys
                        result.add_item_to_key(related_item, "is_preceded_bys")

                    elif mods_related_item_type == "succeedings":

                        # succeeding -> is_succeeded_bys
                        result.add_item_to_key(related_item, "is_succeeded_bys")

    return result


def get_mods_table_of_contentss(mods):
    """ tableOfContents -> table_of_contentss """
    result = {}
    mods_table_of_contentss = mods.findall(xmletree.prefixtag("mods", "tableOfContents"))
    if mods_table_of_contentss is not None:
        table_of_contentss = convert_mods_string_langs(mods_table_of_contentss)
        if table_of_contentss:
            result["table_of_contentss"] = table_of_contentss
    return result


def get_mods_target_audiences(mods):
    """ targetAudience -> target_audiences """
    result = {}
    mods_target_audiences = mods.findall(xmletree.prefixtag("mods", "targetAudience"))
    if mods_target_audiences is not None:
        target_audiences = convert_mods_string_authorities(mods_target_audiences)
        if target_audiences:
            result["target_audiences"] = target_audiences
    return result


def get_mods_title_infos(mods):
    """ titleInfo ->
        title, title_non_sort, title_sub, part_number, part_name,
        title_abbreviateds, title_alternatives, title_translateds, title_uniforms
    """
    result = {}
    mods_titleinfos = mods.findall(xmletree.prefixtag("mods", "titleInfo"))
    if mods_titleinfos is not None:
        title_abbreviateds = []
        title_alternatives = []
        title_translateds = []
        title_uniforms = []
        for mods_titleinfo in mods_titleinfos:
            if mods_titleinfo is not None:
                title_dict = {}
                # type
                title_type = mods_titleinfo.get("type")
                # title -> title
                title_dict.update(get_mods_element_text_and_set_key(mods_titleinfo, "title", "title"))
                # nonSort -> title_non_sort
                title_dict.update(get_mods_element_text_and_set_key(mods_titleinfo, "nonSort", "title_non_sort", False))
                # subTitle -> title_sub
                title_dict.update(get_mods_element_text_and_set_key(mods_titleinfo, "subTitle", "title_sub"))
                # partNumber -> part_number
                title_dict.update(get_mods_element_text_and_set_key(mods_titleinfo, "partNumber", "part_number"))
                # partName -> part_name
                title_dict.update(get_mods_element_text_and_set_key(mods_titleinfo, "partName", "part_name"))

                if title_type is None and "title" not in result:
                    result.update(title_dict)
                elif title_type == "abbreviated":
                    title_abbreviateds.append(title_dict)
                elif title_type == "alternative":
                    title_alternatives.append(title_dict)
                elif title_type == "translated":
                    title_translateds.append(title_dict)
                elif title_type == "uniform":
                    title_uniforms.append(title_dict)
                else:
                    logging.error("error get_mods_title_infos unknown type: {}".format(title_type))
        if title_abbreviateds:
            result["title_abbreviateds"] = title_abbreviateds
        if title_alternatives:
            result["title_alternatives"] = title_alternatives
        if title_translateds:
            result["title_translateds"] = title_translateds
        if title_uniforms:
            result["title_uniforms"] = title_uniforms
    return result


def get_mods_subjects(mods):
    """ subject -> keywords, subjects """
    result = {}
    mods_subjects = mods.findall(xmletree.prefixtag("mods", "subject"))
    if mods_subjects is not None:
        result_subjects = []
        result_keywords_dict = {}
        for mods_subject in mods_subjects:
            if mods_subject is not None:
                # get mods data
                mods_subject_authority = mods_subject.get("authority")
                mods_subject_authority_uri = mods_subject.get("authorityURI")
                mods_subject_lang = mods_subject.get("lang")
                mods_cartographicss = mods_subject.findall(xmletree.prefixtag("mods", "cartographics"))
                mods_genres = mods_subject.findall(xmletree.prefixtag("mods", "genre"))
                mods_geographics = mods_subject.findall(xmletree.prefixtag("mods", "geographic"))
                mods_geographic_codes = mods_subject.findall(xmletree.prefixtag("mods", "geographicCode"))
                mods_hierarchical_geographics = mods_subject.findall(xmletree.prefixtag("mods", "hierarchicalGeographic"))
                mods_names = mods_subject.findall(xmletree.prefixtag("mods", "name"))
                mods_occupations = mods_subject.findall(xmletree.prefixtag("mods", "occupation"))
                mods_temporals = mods_subject.findall(xmletree.prefixtag("mods", "temporal"))
                mods_title_infos = mods_subject.findall(xmletree.prefixtag("mods", "titleInfo"))
                mods_topics = mods_subject.findall(xmletree.prefixtag("mods", "topic"))

                # subject
                subject = {}
                # @authority -> authority
                if mods_subject_authority is not None:
                    subject["authority"] = mods_subject_authority
                if mods_subject_authority_uri is not None:
                    subject["authority"] = mods_subject_authority_uri

                # @lang -> language
                if mods_subject_lang is not None:
                    subject["language"] = mods_subject_lang

                # @valueURI -> subject_id
                subject_id = mods_subject.get("valueURI")
                if subject_id is not None:
                    subject["subject_id"] = subject_id

                # topic -> keywords if authority and authorityURI is None
                # topic -> subjects[] topics[]
                if mods_topics is not None:
                    if mods_subject_authority is None and mods_subject_authority_uri is None:

                        # Undetermined language
                        if mods_subject_lang is None:
                            mods_subject_lang = constants.LANGUAGE_UNDETERMINED

                        # Verify that this key is in the dict
                        if mods_subject_lang is not None and mods_subject_lang not in result_keywords_dict:
                            result_keywords_dict[mods_subject_lang] = []

                        for mods_topic in mods_topics:
                            if mods_topic.text is not None:
                                # in case of multiple keywords in the same topic, split it
                                terms = None
                                if mods_topic.text.find(";") != -1:
                                    terms = mods_topic.text.split(";")
                                elif mods_topic.text.find(",") != -1:
                                    terms = mods_topic.text.split(",")
                                else:
                                    terms = [mods_topic.text]
                                if terms is not None:
                                    for term in terms:
                                        result_keywords_dict[mods_subject_lang].append(term.strip())
                    else:
                        topics = []
                        for mods_topic in mods_topics:
                            if mods_topic.text is not None:
                                topics.append(mods_topic.text)
                        if topics:
                            subject["topics"] = topics

                # cartographics -> cartographics[]
                if mods_cartographicss is not None:
                    cartographics = []
                    for mods_cartographics in mods_cartographicss:
                        cartographic = {}
                        mods_coordinates = mods_cartographics.find(xmletree.prefixtag("mods", "coordinates"))
                        mods_scale = mods_cartographics.find(xmletree.prefixtag("mods", "scale"))
                        mods_projection = mods_cartographics.find(xmletree.prefixtag("mods", "projection"))

                        # coordinates -> coordinates[].latitude, coordinates[].longitude, coordinates[].altitude
                        if mods_coordinates is not None:
                            # todo : extract coordinates latitude, longitude, altitude of each points
                            coordinates = []
                            coordinate = {"latitude" : mods_coordinates.text}
                            coordinates.append(coordinate)
                            cartographic["coordinates"] = coordinates

                        # scale -> scale
                        if mods_scale is not None:
                            cartographic["scale"] = mods_scale.text

                        # projection -> projection
                        if mods_projection is not None:
                            cartographic["projection"] = mods_projection.text

                        if cartographic:
                            cartographics.append(cartographic)

                    if cartographics:
                        subject["cartographics"] = cartographics

                # genre -> genres
                if mods_genres is not None:
                    genres = []
                    for mods_genre in mods_genres:
                        genres.append(mods_genre.text)
                    if genres:
                        subject["genres"] = genres

                geographics = []
                # geographic
                if mods_geographics is not None:
                    for mods_geographic in mods_geographics:
                        geographic = {}
                        mods_geographic_authority = mods_geographic.get("authority")
                        mods_geographic_authority_uri = mods_geographic.get("authorityURI")
                        mods_geographic_value_uri = mods_geographic.get("valueURI")
                        mods_geographic_value = mods_geographic.text

                        if mods_geographic_authority is not None:
                            geographic["authority"] = mods_geographic_authority
                        if mods_geographic_authority_uri is not None:
                            geographic["authority"] = mods_geographic_authority_uri
                        if mods_geographic_value_uri is not None:
                            geographic["geo_id"] = mods_geographic_value_uri
                        if mods_geographic_value is not None:
                            geographic["value"] = mods_geographic_value

                        if geographic:
                            geographics.append(geographic)

                # geographicCode
                if mods_geographic_codes is not None:
                    for mods_geographic_code in mods_geographic_codes:
                        geographic = {}
                        mods_geographic_code_authority = mods_geographic_code.get("authority")
                        mods_geographic_code_authority_uri = mods_geographic_code.get("authorityURI")
                        mods_geographic_code_value_uri = mods_geographic_code.get("valueURI")
                        mods_geographic_code_value = mods_geographic_code.text

                        if mods_geographic_code_authority is not None:
                            geographic["authority"] = mods_geographic_code_authority
                        if mods_geographic_code_authority_uri is not None:
                            geographic["authority"] = mods_geographic_code_authority_uri
                        if mods_geographic_code_value is not None:
                            geographic["geo_id"] = mods_geographic_code_value
                        if mods_geographic_code_value_uri is not None:
                            geographic["geo_id"] = mods_geographic_code_value_uri

                        if geographic:
                            geographics.append(geographic)

                if geographics:
                    subject["geographics"] = geographics


                # hierarchicalGeographic
                # - continent
                # - country
                # - province
                # - region
                # - state
                # - territory
                # - county
                # - city
                # - island
                # - area
                # - extraterrestrialArea
                # - citySection
                if mods_hierarchical_geographics is not None:
                    for mods_hierarchical_geographic in mods_hierarchical_geographics:
                        geographic = {}
                        mods_hierarchical_geographic_authority = mods_hierarchical_geographic.get("authority")
                        mods_hierarchical_geographic_authority_uri = mods_hierarchical_geographic.get("authorityURI")
                        mods_hierarchical_geographic_value_uri = mods_hierarchical_geographic.get("valueURI")

                        if mods_hierarchical_geographic_authority is not None:
                            geographic["authority"] = mods_hierarchical_geographic_authority
                        if mods_hierarchical_geographic_authority_uri is not None:
                            geographic["authority"] = mods_hierarchical_geographic_authority_uri
                        if mods_hierarchical_geographic_value_uri is not None:
                            geographic["geo_id"] = mods_hierarchical_geographic_value_uri

                        if geographic:
                            geographics.append(geographic)

                # TODO
                # name
                # occupation
                # temporal
                # titleInfo

                if subject and not (len(subject) == 1 and "language" in subject):
                    result_subjects.append(subject)

        if result_subjects:
            result["subjects"] = result_subjects
        if result_keywords_dict:
            result["keywords"] = result_keywords_dict
    return result


def get_mods_parts(mods):
    """ part/detail/number -> part_chapter_number, part_issue, part_paragraph_number, part_track_number, part_volume
        part/detail/title -> part_chapter_title, part_section_title, part_track_title
        part/extent/start -> part_page_begin, part_timecode_begin
        part/extent/end -> part_page_end, part_timecode_end
    """
    result = {}
    mods_parts = mods.findall(xmletree.prefixtag("mods", "part"))
    if mods_parts is not None:
        result = {}
        for mods_part in mods_parts:
            if mods_part is not None:
                # detail
                mods_part_details = mods_part.findall(xmletree.prefixtag("mods", "detail"))
                if mods_part_details is not None:
                    for mods_part_detail in mods_part_details:
                        mods_part_detail_type = mods_part_detail.get("type")
                        mods_part_detail_number = get_mods_element_text(mods_part_detail, "number")
                        mods_part_detail_title = get_mods_element_text(mods_part_detail, "title")
                        if mods_part_detail_type is not None:
                            # number
                            if mods_part_detail_number is not None:
                                if mods_part_detail_type == "chapter":
                                    # part/detail@type=chapter/number -> part_chapter_number
                                    result["part_chapter_number"] = mods_part_detail_number
                                elif mods_part_detail_type == "issue":
                                    # part/detail@type=issue/number -> part_issue
                                    result["part_issue"] = mods_part_detail_number
                                elif mods_part_detail_type == "paragraph":
                                    # part/detail@type=paragraph/number -> part_paragraph_number
                                    result["part_paragraph_number"] = mods_part_detail_number
                                elif mods_part_detail_type == "track":
                                    # part/detail@type=track/number -> part_track_number
                                    result["part_track_number"] = mods_part_detail_number
                                elif mods_part_detail_type == "volume":
                                    # part/detail@type=volume/number -> part_volume
                                    result["part_volume"] = mods_part_detail_number
                            # title
                            if mods_part_detail_title is not None:
                                if mods_part_detail_type == "chapter":
                                    # part/detail@type=chapter/title -> part_chapter_title
                                    result["part_chapter_title"] = mods_part_detail_title
                                elif mods_part_detail_type == "section":
                                    # part/detail@type=section/title -> part_section_title
                                    result["part_section_title"] = mods_part_detail_title
                                elif mods_part_detail_type == "track":
                                    # part/detail@type=section/title -> part_track_title
                                    result["part_track_title"] = mods_part_detail_title

                # extent
                mods_part_extents = mods_part.findall(xmletree.prefixtag("mods", "extent"))
                if mods_part_extents is not None:
                    for mods_part_extent in mods_part_extents:
                        mods_part_extent_unit = mods_part_extent.get("unit")
                        mods_part_extent_begin = get_mods_element_text(mods_part_extent, "start")
                        mods_part_extent_end = get_mods_element_text(mods_part_extent, "end")
                        if mods_part_extent_unit in ["page", "pages"]:
                            if mods_part_extent_begin is not None:
                                # part/extent@unit=[page|pages]/start
                                result["part_page_begin"] = mods_part_extent_begin
                            if mods_part_extent_end is not None:
                                # part/extent@unit=[page|pages]/end
                                result["part_page_end"] = mods_part_extent_end
                        elif mods_part_extent_unit in ["minute", "minutes"]:
                            if mods_part_extent_begin is not None:
                                # part/extent@unit=[minute|minutes]/start
                                result["part_timecode_begin"] = mods_part_extent_begin
                            if mods_part_extent_end is not None:
                                # part/extent@unit=[minute|minutes]/end
                                result["part_timecode_end"] = mods_part_extent_end
    return result


def get_mods_record_info(mods):
    """ recordInfo -> rec_ """
    result = {}
    mods_record_info = mods.find(xmletree.prefixtag("mods", "recordInfo"))
    if mods_record_info is not None:
        # descriptionStandard -> rec_cataloging_rules
        rec_cataloging_rules = get_mods_elements_text(mods_record_info, "descriptionStandard")
        if rec_cataloging_rules:
            result["rec_cataloging_rules"] = rec_cataloging_rules
        # languageOfCataloging -> rec_cataloging_languages
        rec_cataloging_languages = get_mods_elements_text(mods_record_info, "languageOfCataloging")
        if rec_cataloging_languages:
            result["rec_cataloging_languages"] = rec_cataloging_languages
        # recordContentSource -> rec_source
        rec_source = get_mods_element_text(mods_record_info, "recordContentSource")
        if rec_source:
            result["rec_source"] = rec_source
        # recordCreationDate -> rec_created_date
        mods_record_creation_date = mods_record_info.find(xmletree.prefixtag("mods", "recordCreationDate"))
        rec_created_date = convert_mods_date(mods_record_creation_date)
        if rec_created_date:
            result["rec_created_date"] = rec_created_date
        # recordChangeDate -> rec_modified_date
        mods_record_change_date = mods_record_info.find(xmletree.prefixtag("mods", "recordChangeDate"))
        rec_modified_date = convert_mods_date(mods_record_change_date)
        if rec_modified_date:
            result["rec_modified_date"] = rec_modified_date
        # recordIdentifier -> rec_id
        rec_id = get_mods_element_text(mods_record_info, "recordIdentifier")
        if rec_id:
            result["rec_id"] = rec_id
        # recordOrigin -> null

    return result


####################
# MetaJSON -> MODS #
####################

def create_mods_collection_xmletree(mods_root_list):
    """ MODS xmletree list -> modsCollection xmletree """
    xmletree.register_namespaces()
    # mods collection root
    mods_collection_root = ET.Element(xmletree.prefixtag("mods", "modsCollection"))
    mods_collection_root.set(xmletree.prefixtag("xsi", "schemaLocation"), constants.xmlns_map["mods"] + " " + constants.xmlns_schema_map["mods"])

    for mods_root in mods_root_list:
        if mods_root[1] is not None:
            mods_collection_root.append(mods_root[1])
    
    return mods_collection_root


def metajson_list_to_mods_xmletree(documents):
    """ MetaJSON Document -> MODS xmletree """
    xmletree.register_namespaces()
    # mods collection root
    mods_collection_root = ET.Element(xmletree.prefixtag("mods", "modsCollection"))
    mods_collection_root.set(xmletree.prefixtag("xsi", "schemaLocation"), constants.xmlns_map["mods"] + " " + constants.xmlns_schema_map["mods"])

    for document in documents:
        mods_root = metajson_to_mods_xmletree(document, False)
        if mods_root is not None:
            mods_collection_root.append(mods_root)
    
    return mods_collection_root


def metajson_to_mods_xmletree(document, with_schema_location=True):
    """ MetaJSON Document -> MODS xmletree """
    # rec_id
    rec_id = document["rec_id"]

    # mods_root
    xmletree.register_namespaces()
    mods_root = ET.Element(xmletree.prefixtag("mods", "mods"), version="3.5")
    if with_schema_location:
        mods_root.set(xmletree.prefixtag("xsi", "schemaLocation"), constants.xmlns_map["mods"] + " " + constants.xmlns_schema_map["mods"])

    metajson_to_mods_root_or_related_item(document, mods_root)

    return (rec_id, mods_root)


def metajson_to_mods_root_or_related_item(document, mods_item):
    # titleInfo
    convert_metajson_document_titles(document, mods_item)

    # name
    convert_metajson_document_creators(document, mods_item)

    # typeOfResource, genre
    convert_metajson_document_type(document, mods_item)

    # originInfo
    convert_metajson_document_origin_info(document, mods_item)

    # language
    convert_metajson_document_languages(document, mods_item)

    # physicalDescription
    convert_metajson_document_physical_description(document, mods_item)

    # abstract
    convert_metajson_document_descriptions(document, mods_item)

    # tableOfContents
    convert_metajson_document_table_of_contentss(document, mods_item)

    # targetAudience
    convert_metajson_document_target_audiences(document, mods_item)

    # note
    convert_metajson_document_notes(document, mods_item)

    # subject
    convert_metajson_document_subjects(document, mods_item)

    # classification
    convert_metajson_document_classifications(document, mods_item)

    # relatedItem
    convert_metajson_document_related_items(document, mods_item)

    # identifier
    convert_metajson_document_identifiers(document, mods_item)

    # location
    convert_metajson_document_resources(document, mods_item)

    # accessCondition
    convert_metajson_document_rights(document, mods_item)

    # part
    convert_metajson_document_parts(document, mods_item)

    # extension

    # recordInfo
    convert_metajson_document_rec_infos(document, mods_item)


def convert_metajson_document_titles(document, mods_item):
    # document title properties -> titleInfo @type=null (proper)
    convert_metajson_title(document, None, mods_item)
    # title_abbreviateds -> titleInfo @type=abbreviated
    if "title_abbreviateds" in document:
        for title in document["title_abbreviateds"]:
            convert_metajson_title(title, "abbreviated", mods_item)
    # title_alternatives -> titleInfo @type=alternative
    if "title_alternatives" in document:
        for title in document["title_alternatives"]:
            convert_metajson_title(title, "alternative", mods_item)
    # title_forms -> ?
    # title_translateds -> titleInfo @type=translated
    if "title_translateds" in document:
        for title in document["title_translateds"]:
            convert_metajson_title(title, "translated", mods_item)
    # title_uniforms -> titleInfo @type=uniform
    if "title_uniforms" in document:
        for title in document["title_uniforms"]:
            convert_metajson_title(title, "uniform", mods_item)


def convert_metajson_title(document, title_type, mods_item):
    titleInfo = ET.SubElement(mods_item, xmletree.prefixtag("mods", "titleInfo"))
    if title_type:
        titleInfo.set("type", title_type)
    if "title" in document:
        title = ET.SubElement(titleInfo, xmletree.prefixtag("mods", "title"))
        title.text = document["title"]
    if "title_non_sort" in document:
        nonSort = ET.SubElement(titleInfo, xmletree.prefixtag("mods", "nonSort"))
        nonSort.text = document["title_non_sort"]
    if "title_sub" in document:
        subTitle = ET.SubElement(titleInfo, xmletree.prefixtag("mods", "subTitle"))
        subTitle.text = document["title_sub"]
    if "part_name" in document:
        partName = ET.SubElement(titleInfo, xmletree.prefixtag("mods", "partName"))
        partName.text = document["part_name"]
    if "part_number" in document:
        partNumber = ET.SubElement(titleInfo, xmletree.prefixtag("mods", "partNumber"))
        partNumber.text = document["part_number"]


def convert_metajson_document_creators(document, mods_item):
    if "creators" in document:
        for creator in document["creators"]:
            convert_metajson_document_creator(creator, mods_item)


def convert_metajson_document_creator(creator, mods_item):
    if creator is not None:
        if "agent" in creator:
            # agent -> name
            mods_name = convert_metajson_agent(creator["agent"], mods_item)
            # roles -> role/roleTerm
            if "roles" in creator and creator["roles"]:
                for role in creator["roles"]:
                    mods_role = ET.SubElement(mods_name, xmletree.prefixtag("mods", "role"))
                    mods_roleTerm = ET.SubElement(mods_role, xmletree.prefixtag("mods", "roleTerm"), type="code", authority="marcrelator")
                    mods_roleTerm.text = role


def convert_metajson_agent(agent, mods_item):
    mods_name = None
    # Person
    if agent["rec_class"] == constants.REC_CLASS_PERSON:
        mods_name = ET.SubElement(mods_item, xmletree.prefixtag("mods", "name"), type="personal")
        if "name_family" in agent:
            namePart_family = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"), type="family")
            namePart_family.text = agent["name_family"]
        # TODO
        # name_middle
        # name_prefix
        # name_prefix_dropping
        # name_suffix
        # titles[i]/value
        if "name_given" in agent:
            namePart_given = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"), type="given")
            namePart_given.text = agent["name_given"]
        if "date_birth" in agent or "date_death" in agent:
            date = ""
            if "date_birth" in agent:
                date += agent["date_birth"]
            date += "-"
            if "date_death" in agent:
                date += agent["date_death"]
            if date != "-":
                namePart_date = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"), type="date")
                namePart_date.text = date
    # Orgunit
    elif agent["rec_class"] == constants.REC_CLASS_ORGUNIT:
        mods_name = ET.SubElement(mods_item, xmletree.prefixtag("mods", "name"), type="corporate")
        if "name" in agent:
            namePart_main = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"))
            namePart_main.text = agent["name"]
        if "date_foundation" in agent or "date_dissolution" in agent:
            date = ""
            if "date_foundation" in agent:
                date += agent["date_foundation"]
            date += "-"
            if "date_dissolution" in agent:
                date += agent["date_dissolution"]
            if date != "-":
                namePart_date = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"), type="date")
                namePart_date.text = date
    # Event
    elif agent["rec_class"] == constants.REC_CLASS_EVENT:
        mods_name = ET.SubElement(mods_item, xmletree.prefixtag("mods", "name"), type="conference")
        # title -> namePart@type=null
        if "title" in agent:
            namePart_main = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"))
            namePart_main.text = agent["title"]
        # number -> description(first token ;)
        # international -> description(second token ;)
        if "number" in agent or "international" in agent:
            description_text = ""
            if "number" in agent:
                description_text = agent["number"]
            if "international" in agent:
                description_text = description_text + ";" + agent["international"]
                description_mods = ET.SubElement(mods_name, xmletree.prefixtag("mods", "description"))
                description_mods.text = description_text
        # date_begin -> namePart@type=date(first token /)
        # date_end -> namePart@type=date(second token /)
        if "date_begin" in agent or "date_end" in agent:
            date = ""
            if "date_begin" in agent:
                date += agent["date_begin"]
            date += "-"
            if "date_end" in agent:
                date += agent["date_end"]
            if date != "-":
                namePart_date = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"), type="date")
                namePart_date.text = date
        # place -> name@type=conference/namePart@type=termsOfAddress/(first token ;)
        # country -> name@type=conference/namePart@type=termsOfAddress/(second token ;)
        if "place" in agent or "country" in agent:
            termsOfAddress_text = ""
            if "place" in agent:
                termsOfAddress_text = agent["place"]
            if "country" in agent:
                termsOfAddress_text = termsOfAddress_text + ";" + agent["international"]
                termsOfAddress = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"), type="termsOfAddress")
                termsOfAddress.text = termsOfAddress_text
    # Family
    elif agent["rec_class"] == constants.REC_CLASS_FAMILY:
        mods_name = ET.SubElement(mods_item, xmletree.prefixtag("mods", "name"), type="family")
        if "name_family" in agent:
            namePart_main = ET.SubElement(mods_name, xmletree.prefixtag("mods", "namePart"), type="family")
            namePart_main.text = agent["name_family"]
    # commons
    # affiliations -> affiliation
    if "affiliations" in agent:
        for affiliation in agent["affiliations"]:
            if "agent" in affiliation and "name" in affiliation["agent"]:
                mods_affiliation = ET.SubElement(mods_name, xmletree.prefixtag("mods", "affiliation"))
                mods_affiliation.text = affiliation["agent"]["name"]
    # biographies_short[i]/value -> description
    if "biographies_short" in agent:
        for biographie_short in agent["biographies_short"]:
            description_mods = ET.SubElement(mods_name, xmletree.prefixtag("mods", "description"))
            description_mods.text = biographie_short["value"]
    # biographies[i]/value -> description
    if "biographies" in agent:
        for biographie in agent["biographies"]:
            description_mods = ET.SubElement(mods_name, xmletree.prefixtag("mods", "description"))
            description_mods.text = biographie["value"]
    # descriptions[i]/value -> description
    if "descriptions" in agent:
        for description in agent["descriptions"]:
            description_mods = ET.SubElement(mods_name, xmletree.prefixtag("mods", "description"))
            description_mods.text = description["value"]
    # descriptions_short[i]/value -> description
    if "descriptions_short" in agent:
        for description_short in agent["descriptions_short"]:
            description_mods = ET.SubElement(mods_name, xmletree.prefixtag("mods", "description"))
            description_mods.text = description_short["value"]
    # notes[i]/value -> description
    if "notes" in agent:
        for note in agent["notes"]:
            description_mods = ET.SubElement(mods_name, xmletree.prefixtag("mods", "description"))
            description_mods.text = note["value"]
    return mods_name


def convert_metajson_document_type(document, mods_item):
    rec_type = document["rec_type"]
    # typeOfResource
    typeOfResource_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "typeOfResource"))
    typeOfResource_mods.text = METAJSON_DOCUMENT_TYPE_TO_MODS_TYPEOFRESOURCE[document["rec_type"]]
    if document["rec_type"] in METAJSON_DOCUMENT_TYPE_IS_MODS_COLLECTION:
        typeOfResource_mods.set("collection", "yes")
    if document["rec_type"] in METAJSON_DOCUMENT_TYPE_IS_MODS_MANUSCRIPT:
        typeOfResource_mods.set("manuscript", "yes")
    # genre
    if rec_type in METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_EUREPO:
        genre_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "genre"))
        genre_mods.text = METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_EUREPO[rec_type]
    if rec_type in METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_EPRINT:
        genre_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "genre"))
        genre_mods.text = METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_EPRINT[rec_type]
    if rec_type in METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_MARCGT:
        genre_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "genre"))
        genre_mods.set("authority", "marcgt")
        genre_mods.text = METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_MARCGT[rec_type]
    if rec_type in METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_OTHER:
        genre_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "genre"))
        genre_mods.text = METAJSON_DOCUMENT_TYPE_TO_MODS_GENRE_OTHER[rec_type]


def convert_metajson_document_origin_info(document, mods_item):
    # todo
    # publication_countries, publication_places, publication_states -> place/placeTerm
    # publishers -> publisher
    # date_issued -> dateIssued
    # date_created -> dateCreated
    # date_captured -> dateCaptured
    # date_valid_begin, date_valid_end -> dateValid
    # date_modified -> dateModified
    # date_copyright -> copyrightDate
    # date_other -> dateOther
    # edition -> edition
    # issuance -> issuance
    # frequency -> frequency
    pass


def convert_metajson_document_languages(document, mods_item):
    if "languages" in document:
        for language in document["languages"]:
            language_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "language"))
            languageTerm_mods = ET.SubElement(language_mods, xmletree.prefixtag("mods", "languageTerm"))
            languageTerm_mods.set("type", "code")
            languageTerm_mods.set("authority", "rfc4646")
            languageTerm_mods.text = language


def convert_metajson_document_physical_description(document, mods_item):
    # TODO
    # form -> form
    # reformatting_quality -> reformattingQuality
    # -> internetMediaType
    # -> extent
    # digital_origin -> digitalOrigin
    # physical_description_notes -> note
    pass


def convert_metajson_document_descriptions(document, mods_item):
    if "descriptions" in document:
        for description in document["descriptions"]:
            if "value" in description:
                abstract_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "abstract"))
                abstract_mods.text = description["value"]
                if "language" in description:
                    abstract_mods.set("lang", description["language"])


def convert_metajson_document_table_of_contentss(document, mods_item):
    if "table_of_contentss" in document:
        for table_of_contents in document["table_of_contentss"]:
            if "value" in table_of_contents:
                tableOfContents_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "tableOfContents"))
                tableOfContents_mods.text = table_of_contents["value"]
                if "language" in table_of_contents:
                    tableOfContents_mods.set("lang", table_of_contents["language"])
                if "content_type" in table_of_contents:
                    tableOfContents_mods.set("type", table_of_contents["content_type"])


def convert_metajson_document_target_audiences(document, mods_item):
    if "target_audiences" in document:
        for authority in document["target_audiences"].keys():
            for value in document["target_audiences"][authority]:
                targetAudience_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "targetAudience"))
                targetAudience_mods.set("authority", authority)
                targetAudience_mods.text = value


def convert_metajson_document_notes(document, mods_item):
    if "notes" in document:
        for note in document["notes"]:
            if "value" in note:
                note_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "note"))
                note_mods.text = note["value"]
                if "language" in note:
                    note_mods.set("lang", note["language"])
                if "note_type" in note:
                    note_mods.set("type", note["note_type"])


def convert_metajson_document_subjects(document, mods_item):
    if "subjects" in document:
        #logging.debug(jsonbson.dumps_json(document["subjects"], True))
        for subject in document["subjects"]:
            subject_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "subject"))
            # authority -> @authority
            if "authority" in subject:
                subject_mods.set("authority", subject["authority"])
            if "subject_id" in subject:
                subject_mods.set("authority", subject["subject_id"])
            if "language" in subject:
                subject_mods.set("lang", subject["language"])
            #subject_type = subject["subject_type"]
            # topics -> topic
            if "topics" in subject:
                for topic in subject["topics"]:
                    topic_mods = ET.SubElement(subject_mods, xmletree.prefixtag("mods", "topic"))
                    topic_mods.text = topic["value"]
            # geographics -> geographic or geographicCode or hierarchicalGeographic
            if "geographics" in subject:
                for geographic in subject["geographics"]:
                    geographic_mods = ET.SubElement(subject_mods, xmletree.prefixtag("mods", "geographic"))
                    geographic_mods.text = geographic["value"]
            # temporals -> temporal
            if "temporals" in subject:
                for temporal in subject["temporals"]:
                    temporal_mods = ET.SubElement(subject_mods, xmletree.prefixtag("mods", "temporal"))
                    temporal_mods.text = temporal["value"]
            # documents -> titleInfo
            if "documents" in subject:
                for sub_doc in subject["documents"]:
                    convert_metajson_document_titles(sub_doc, subject_mods)
            # agents -> name
            if "agents" in subject:
                for agent in subject["agents"]:
                    convert_metajson_agent(agent, subject_mods)
            # genres -> genre
            if "genres" in subject:
                for genre in subject["genres"]:
                    genre_mods = ET.SubElement(subject_mods, xmletree.prefixtag("mods", "genre"))
                    genre_mods.text = genre
            # occupations -> occupation
            if "occupations" in subject:
                for occupation in subject["occupations"]:
                    occupation_mods = ET.SubElement(subject_mods, xmletree.prefixtag("mods", "occupation"))
                    occupation_mods.text = occupation
    # cartographics -> cartographics
    if "cartographics" in document:
        #logging.debug(jsonbson.dumps_json(document["cartographics"], True))
        subject_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "subject"))
        for cartographic in document["cartographics"]:
            cartographics_mods = ET.SubElement(subject_mods, xmletree.prefixtag("mods", "cartographics"))
            if "scale" in cartographic:
                scale_mods = ET.SubElement(cartographics_mods, xmletree.prefixtag("mods", "scale"))
                scale_mods.text = cartographic["scale"]
            if "projection" in cartographic:
                projection_mods = ET.SubElement(cartographics_mods, xmletree.prefixtag("mods", "projection"))
                projection_mods.text = cartographic["projection"]
            if "coordinates" in cartographic:
                coordinates_value = ""
                for coordinate in cartographic["coordinates"]:
                    coordinates_value = coordinates_value + " " + coordinate
                if coordinates_value:
                    coordinates_mods = ET.SubElement(cartographics_mods, xmletree.prefixtag("mods", "coordinates"))
                    coordinates_mods.text = coordinates_value
            if "coordinates_unstructured" in cartographic:
                coordinates_mods = ET.SubElement(cartographics_mods, xmletree.prefixtag("mods", "coordinates"))
                coordinates_mods.text = cartographic["coordinates_unstructured"]


def convert_metajson_document_classifications(document, mods_item):
    if "classifications" in document:
        for autority in document["classifications"].keys():
            if document["classifications"][autority] is not None:
                for value in document["classifications"][autority]:
                    classification_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "classification"))
                    classification_mods.set("authority", autority)
                    classification_mods.text = value


def convert_metajson_document_related_items(document, mods_item):
    prop_to_mods_type = {
        "absorbs": "succeeding",
        "aggregates": "succeeding",
        "becomes": "preceding",
        "conforms_tos": "references",
        "continues": "succeeding",
        "describes": "references",
        "has_formats": "otherFormat",
        "has_offprints": "constituent",
        "has_parts": "constituent",
        "has_relation_withs": "references",
        "has_reviews": "isReferencedBy",
        "has_supplements": "constituent",
        "has_translations": "otherVersion",
        "has_versions": "otherVersion",
        "is_absorbed_intos": "preceding",
        "is_aggregated_bys": "preceding",
        "is_bound_afters": "host",
        "is_bound_withs": "host",
        "is_described_bys": "is_described_bys",
        "is_format_ofs": "otherFormat",
        "is_merged_froms": "succeeding",
        "is_offprint_ofs": "host",
        "is_part_ofs": "host",
        "is_partially_absorbed_intos": "preceding",
        "is_partially_replaced_bys": "preceding",
        "is_preceded_bys": "succeeding",
        "is_published_withs": "host",
        "is_referenced_bys": "isReferencedBy",
        "is_replaced_bys": "preceding",
        "is_review_ofs": "reviewOf",
        "is_split_intos": "preceding",
        "is_splitted_froms": "succeeding",
        "is_succeeded_bys": "preceding",
        "is_supplement_ofs": "host",
        "is_translation_ofs": "otherVersion",
        "is_updated_bys": "preceding",
        "merges_withs": "succeeding",
        "originals": "original",
        "partially_absorbs": "succeeding",
        "partially_becomes": "preceding",
        "partially_continues": "succeeding",
        "partially_replaces": "succeeding",
        "re_becomes": "succeeding",
        "references": "references",
        "replaces": "succeeding",
        "requires": "references",
        "seriess": "series",
        "sub_series": "constituent",
        "updates": "succeeding"
    }
    for key in prop_to_mods_type.keys():
        if key in document and document[key] is not None:
            for related in document[key]:
                relatedItem_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "relatedItem"))
                relatedItem_mods.set("type", prop_to_mods_type[key])
                metajson_to_mods_root_or_related_item(related, relatedItem_mods)


def convert_metajson_document_identifiers(document, mods_item):
    if "identifiers" in document:
        for identifier in document["identifiers"]:
            if "value" in identifier:
                identifier_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "identifier"))
                identifier_mods.text = identifier["value"]
                if "language" in identifier:
                    identifier_mods.set("lang", identifier["language"])
                if "id_type" in identifier:
                    identifier_mods.set("type", identifier["id_type"])


def convert_metajson_document_resources(document, mods_item):
    # todo
    pass


def convert_metajson_document_rights(document, mods_item):
    if "rights" in document:
        rights = document["rights"]
        if "rights_holders" in rights:
            for rights_holder in rights["rights_holders"]:
                convert_metajson_document_creator(rights_holder, mods_item)
        if "permissions" in rights:
            metajson_type_to_mods_type  = {
                "discover": "restriction on access",
                "display": "restriction on access",
                "print": "use and reproduction",
                "play": "use and reproduction",
                "execute": "use and reproduction"
            }
            for permission in rights["permissions"]:
                if "descriptions" in permission:
                    for description in permission["descriptions"]:
                        accessCondition_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "accessCondition"))
                        accessCondition_mods.text = description
                        ac_type = "use and reproduction"
                        if permission["permission_type"] in metajson_type_to_mods_type:
                            ac_type = metajson_type_to_mods_type[permission["permission_type"]]
                        accessCondition_mods.set("type", ac_type)


def convert_metajson_document_parts(document, mods_item):
    # todo
    pass


def convert_metajson_document_rec_infos(document, mods_item):
    recordInfo_mods = ET.SubElement(mods_item, xmletree.prefixtag("mods", "recordInfo"))
    # rec_cataloging_charactersets -> 
    # rec_cataloging_languages -> languageOfCataloging/languageTerm
    if "rec_cataloging_languages" in document:
        for rec_cataloging_language in document["rec_cataloging_languages"]:
            languageOfCataloging_mods = ET.SubElement(recordInfo_mods, xmletree.prefixtag("mods", "languageOfCataloging"))
            languageTerm_mods = ET.SubElement(languageOfCataloging_mods, xmletree.prefixtag("mods", "languageTerm"))
            languageTerm_mods.set("type", "code")
            languageTerm_mods.set("authority", "rfc4646")
            languageTerm_mods.text = rec_cataloging_language
    # rec_cataloging_transliteration -> languageOfCataloging/scriptTerm
    # rec_created_date -> recordCreationDate
    if "rec_created_date" in document:
        recordCreationDate_mods = ET.SubElement(recordInfo_mods, xmletree.prefixtag("mods", "recordCreationDate"))
        recordCreationDate_mods.set("encoding", "iso8601")
        recordCreationDate_mods.text = document["rec_created_date"]
    # rec_id -> recordIdentifier
    if "rec_id" in document:
        recordIdentifier_mods = ET.SubElement(recordInfo_mods, xmletree.prefixtag("mods", "recordIdentifier"))
        recordIdentifier_mods.text = document["rec_id"]
    # rec_modified_date -> recordChangeDate
    if "rec_modified_date" in document:
        recordChangeDate_mods = ET.SubElement(recordInfo_mods, xmletree.prefixtag("mods", "recordChangeDate"))
        recordChangeDate_mods.set("encoding", "iso8601")
        recordChangeDate_mods.text = document["rec_modified_date"]
    # rec_source -> recordOrigin
    if "rec_source" in document:
        recordOrigin_mods = ET.SubElement(recordInfo_mods, xmletree.prefixtag("mods", "recordOrigin"))
        recordOrigin_mods.text = document["rec_source"]
    # rec_source_cataloging_rule -> ?
    # rec_source_country -> ?
    # rec_source_date -> ?
    # rec_source_rec_id -> ?
    # rec_type_description -> descriptionStandard


#########
# Utils #
#########

def convert_mods_date(mods_date):
    """ Extract and convert MODS date to ISO 8601 """
    if mods_date is not None and mods_date.text is not None:
        encoding = mods_date.get("encoding")
        #point = mods_date.get("point")
        #key_date = mods_date.get("keyDate")
        #qualifier = mods_date.get("qualifier")
        value = mods_date.text.strip()
        if encoding in ["iso8601"]:
            return value
        else:
            # todo
            #parsed_date = date_service.parse_to_iso8601(value)
            #if parsed_date:
            #    return parsed_date
            return value


def convert_mods_string_authorities(mods_string_authorities):
    """ text, authority -> value, authority """
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


def convert_mods_string_langs(mods_string_langs):
    """ lang, text -> language, value """
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
                    else:
                        result["language"] = "und"
                    results.append(result)
        return results


def convert_mods_string_lang_types(mods_string_lang_types, type_field):
    if mods_string_lang_types is not None:
        results = []
        for mods_string_lang_type in mods_string_lang_types:
            if mods_string_lang_type is not None and mods_string_lang_type.text is not None:
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


def get_mods_textlangs_as_list(rml, element):
    """ @xml:lang -> language
        text -> value """
    rml_sls = rml.findall(xmletree.prefixtag("mods", element))
    if rml_sls is not None:
        sls = []
        for rml_sl in rml_sls:
            if rml_sl is not None and rml_sl.text is not None:
                language = rml_sl.get(xmletree.prefixtag("xml", "lang"))
                value = rml_sl.text.strip()
                if value is not None:
                    sl = {"value": value}
                    if language is not None:
                        sl["language"] = language.strip()
                    sls.append(sl)
        if sls:
            return sls


def get_mods_textlangs_and_set_key(rml, element, key):
    """ element -> key
        @xml:lang -> language
        text -> value """
    result = {}
    sls = get_mods_textlangs_as_list(rml, element)
    if sls:
        result[key] = sls
    return result


def get_mods_element_text(rml, element, strip=True):
    element_xmletree = rml.find(xmletree.prefixtag("mods", element))
    return xmletree.get_element_text(element_xmletree, strip)


def get_mods_element_text_as_boolean(rml, element):    
    element_xmletree = rml.find(xmletree.prefixtag("mods", element))
    return xmletree.get_element_text_as_boolean(element_xmletree)


def get_mods_element_text_and_set_key(rml, element, key, strip=True):
    result = {}
    key_value = get_mods_element_text(rml, element, strip)
    if key_value is not None:
        result[key] = key_value
    return result


def get_mods_elements_text(rml, element):
    elements_xmletree = rml.findall(xmletree.prefixtag("mods", element))
    if elements_xmletree is not None:
        results = []
        for element_xmletree in elements_xmletree:
            if element_xmletree is not None:
                results.append(xmletree.get_element_text(element_xmletree))
        if results:
            return results
    return None


def get_mods_elements_text_and_set_key(rml, element, key):
    result = {}
    values = get_mods_elements_text(rml, element)
    if values is not None:
        result[key] = values
    return result
