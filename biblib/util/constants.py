#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

FILE_TYPE_BIBTEX = 'bibtex'
FILE_TYPE_CSV = 'csv'
FILE_TYPE_JSON = 'json'
FILE_TYPE_MARC = 'marc'
FILE_TYPE_TXT = 'txt'
FILE_TYPE_XMLETREE = 'xmletree'

FORMAT_ALTO = 'alto'
FORMAT_BIBJSON = 'bibjson'
FORMAT_BIBTEX = 'bibtex'
FORMAT_DDI = 'ddi'
FORMAT_EAD = 'ead'
FORMAT_ENDNOTEXML = 'endnotexml'
FORMAT_LOM = 'lom'
FORMAT_METAJSON = 'metajson'
FORMAT_METAJSONUI = 'metajsonui'
FORMAT_METS = 'mets'
FORMAT_MIX = 'mix'
FORMAT_MODS = 'mods'
FORMAT_OAIDC = 'oai_dc'
FORMAT_OPENURL = 'openurl'
FORMAT_OPENURLCOINS = 'openurlcoins'
FORMAT_PREMIS = 'premis'
FORMAT_RESEARCHERML = 'researcherml'
FORMAT_SUMMONJSON = 'summonjson'
FORMAT_UNIXREF = 'unixref'

file_extension_to_type = {
    'bib': FILE_TYPE_BIBTEX,
    'json': FILE_TYPE_JSON,
    'marc': FILE_TYPE_MARC,
    'mrc': FILE_TYPE_MARC,
    'ris': FILE_TYPE_TXT,
    'xml': FILE_TYPE_XMLETREE
}

type_to_file_extension = {
    FILE_TYPE_BIBTEX: 'bib',
    FILE_TYPE_JSON: 'json',
    FILE_TYPE_MARC: 'mrc',  # todo list with marc
    FILE_TYPE_TXT: 'ris',
    FILE_TYPE_XMLETREE: 'xml'
}

input_format_to_type = {
    'alto': FILE_TYPE_BIBTEX,
    'bibjson': FILE_TYPE_JSON,
    'bibtex': FILE_TYPE_BIBTEX,
    'dc': FILE_TYPE_XMLETREE,
    'ddi': FILE_TYPE_XMLETREE,
    'endnotexml': FILE_TYPE_XMLETREE,
    'metajson': FILE_TYPE_JSON,
    'mets': FILE_TYPE_XMLETREE,
    'mix': FILE_TYPE_XMLETREE,
    'mods': FILE_TYPE_XMLETREE,
    'oai_dc': FILE_TYPE_XMLETREE,
    'premis': FILE_TYPE_XMLETREE,
    'repec': FILE_TYPE_TXT,
    'ris': FILE_TYPE_TXT,
    'researcherml': FILE_TYPE_XMLETREE,
    'summonjson': FILE_TYPE_JSON,
    'unixref': FILE_TYPE_XMLETREE
}

xmlns_map = {
    'alto': "http://schema.ccs-gmbh.com/ALTO",
    'app': "http://www.w3.org/2007/app",
    'atom': "http://www.w3.org/2005/Atom",
    'dai': "info:eu-repo/dai",
    'dc': "http://purl.org/dc/elements/1.1/",
    'dcmitype': "http://purl.org/dc/dcmitype/",
    'dcterms': "http://purl.org/dc/terms/",
    'didl': "urn:mpeg:mpeg21:2002:02-DIDL-NS",
    'ddi': "http://www.icpsr.umich.edu/DDI",
    'gd': "http://schemas.google.com/g/2005",
    'gdocs': "http://schemas.google.com/docs/2007",
    'media': "http://search.yahoo.com/mrss/",
    'mets': "http://www.loc.gov/METS/",
    'mix': "http://www.loc.gov/mix/v20",
    'mods': "http://www.loc.gov/mods/v3",
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'oai_rem_rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'opensearch': "http://a9.com/-/spec/opensearch/1.1/",
    'opensearchrss': "http://a9.com/-/spec/opensearchrss/1.0/",
    'premis': "info:lc/xmlns/premis-v2",
    'qualifieddc': "",
    'researcherml': "http://bibliotheque.sciences-po.fr/standards/researcherml/v1",
    'simpledc': "",
    'yt': "http://gdata.youtube.com/schemas/2007"
}

xmlns_to_input_format = {
    'http://schema.ccs-gmbh.com/ALTO': FORMAT_ALTO,
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://www.openarchives.org/OAI/2.0/oai_dc/': FORMAT_OAIDC,
    'http://www.icpsr.umich.edu/DDI': FORMAT_DDI,
    'http://www.loc.gov/METS/': FORMAT_METS,
    'http://www.loc.gov/mix/v20': FORMAT_MIX,
    'http://www.loc.gov/mods/v3': FORMAT_MODS,
    'info:lc/xmlns/premis-v2': FORMAT_PREMIS,
    'http://bibliotheque.sciences-po.fr/standards/researcherml/v1': FORMAT_RESEARCHERML
}

xmltag_to_input_format = {
    'alto': FORMAT_ALTO,
    'dc': FORMAT_OAIDC,
    'codeBook': FORMAT_DDI,
    'mets': FORMAT_METS,
    'mix': FORMAT_MIX,
    'mods': FORMAT_MODS,
    'modsCollection': FORMAT_MODS,
    'oai_dc': FORMAT_OAIDC,
    'premis': FORMAT_PREMIS,
    'qualifieddc': FORMAT_OAIDC,
    'researcherml': FORMAT_RESEARCHERML,
    'simpledc': FORMAT_OAIDC,
    'contributor': 'dc',
    'coverage': 'dc',
    'creator': 'dc',
    'date': 'dc',
    'format': 'dc',
    'language': 'dc',
    'publisher': 'dc',
    'rights': 'dc',
    'source': 'dc',
    'subject': 'dc',
    'title': 'dc',
    'type': 'dc'
}

DOC_TYPE_ARTICLE = "Article"
DOC_TYPE_AUDIORECORDING = "AudioRecording"
DOC_TYPE_BOOK = "Book"
DOC_TYPE_BOOKPART = "BookPart"
DOC_TYPE_CONFERENCEPROCEEDINGS = "ConferenceProceedings"
DOC_TYPE_DICTIONARY = "Dictionary"
DOC_TYPE_DOCUMENT = "Document"
DOC_TYPE_FILM = "Film"
DOC_TYPE_IMAGE = "Image"
DOC_TYPE_JOURNAL = "Journal"
DOC_TYPE_JOURNALARTICLE = "JournalArticle"
DOC_TYPE_MAGAZINE = "Magazine"
DOC_TYPE_MAGAZINEARTICLE = "MagazineArticle"
DOC_TYPE_NEWSPAPER = "Newspaper"
DOC_TYPE_NEWSPAPERARTICLE = "NewspaperArticle"
DOC_TYPE_SOFTWARE = "Software"
DOC_TYPE_THESIS = "Thesis"
DOC_TYPE_UNPUBLISHEDDOCUMENT = "UnpublishedDocument"
DOC_TYPE_WEBENTITY = "WebEntity"
