#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

TYPE_BIBTEX = 'bibtex'
TYPE_CSV = 'csv'
TYPE_JSON = 'json'
TYPE_MARC = 'marc'
TYPE_TXT = 'txt'
TYPE_XMLETREE = 'xmletree'

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
    'bib': TYPE_BIBTEX,
    'json': TYPE_JSON,
    'marc': TYPE_MARC,
    'mrc': TYPE_MARC,
    'ris': TYPE_TXT,
    'xml': TYPE_XMLETREE
}

type_to_file_extension = {
    TYPE_BIBTEX: 'bib',
    TYPE_JSON: 'json',
    TYPE_MARC: 'mrc',# todo list with marc
    TYPE_TXT: 'ris',
    TYPE_XMLETREE: 'xml'
}

input_format_to_type = {
    'alto': TYPE_BIBTEX,
    'bibjson': TYPE_JSON,
    'bibtex': TYPE_BIBTEX,
    'dc': TYPE_XMLETREE,
    'ddi': TYPE_XMLETREE,
    'endnotexml': TYPE_XMLETREE,
    'metajson': TYPE_JSON,
    'mets': TYPE_XMLETREE,
    'mix': TYPE_XMLETREE,
    'mods': TYPE_XMLETREE,
    'oai_dc': TYPE_XMLETREE,
    'premis': TYPE_XMLETREE,
    'repec': TYPE_TXT,
    'ris': TYPE_TXT,
    'researcherml': TYPE_XMLETREE,
    'summonjson': TYPE_JSON,
    'unixref': TYPE_XMLETREE
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
