#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

VERSION = '0.5'

FILE_TYPE_BIBTEX = 'bibtex'
FILE_TYPE_CSV = 'csv'
FILE_TYPE_HTML = 'html'
FILE_TYPE_JSON = 'json'
FILE_TYPE_MARC = 'marc'
FILE_TYPE_TXT = 'txt'
FILE_TYPE_XMLETREE = 'xmletree'

FORMAT_ALTO = 'alto'
FORMAT_BIBJSON = 'bibjson'
FORMAT_BIBTEX = 'bibtex'
FORMAT_DDI = 'ddi'
FORMAT_DIDL = 'didl'
FORMAT_EAD = 'ead'
FORMAT_ENDNOTEXML = 'endnotexml'
FORMAT_HTML = 'html'
FORMAT_LOM = 'lom'
FORMAT_METAJSON = 'metajson'
FORMAT_METS = 'mets'
FORMAT_MIX = 'mix'
FORMAT_MODS = 'mods'
FORMAT_OAIDC = 'oai_dc'
FORMAT_OPENURL = 'openurl'
FORMAT_OPENURLCOINS = 'openurlcoins'
FORMAT_PREMIS = 'premis'
FORMAT_REPEC = 'repec'
FORMAT_RESEARCHERML = 'researcherml'
FORMAT_RIS = 'ris'
FORMAT_SUMMONJSON = 'summonjson'
FORMAT_UNIMARC = 'unimarc'
FORMAT_UNIXREF = 'unixref'

LANGUAGE_UNDETERMINED = "und"
CLASSIFICATION_UNDETERMINED = "und"

file_extension_to_type = {
    'bib': FILE_TYPE_BIBTEX,
    'htm': FILE_TYPE_HTML,
    'html': FILE_TYPE_HTML,
    'json': FILE_TYPE_JSON,
    'marc': FILE_TYPE_MARC,
    'mrc': FILE_TYPE_MARC,
    'ris': FILE_TYPE_TXT,
    'xml': FILE_TYPE_XMLETREE
}

type_to_file_extension = {
    FILE_TYPE_BIBTEX: 'bib',
    FILE_TYPE_HTML: 'html',
    FILE_TYPE_JSON: 'json',
    FILE_TYPE_MARC: 'mrc',  # todo list with marc
    FILE_TYPE_TXT: 'ris',
    FILE_TYPE_XMLETREE: 'xml'
}

input_format_to_type = {
    FORMAT_ALTO: FILE_TYPE_XMLETREE,
    FORMAT_BIBJSON: FILE_TYPE_JSON,
    FORMAT_BIBTEX: FILE_TYPE_BIBTEX,
    'dc': FILE_TYPE_XMLETREE,
    FORMAT_DDI: FILE_TYPE_XMLETREE,
    FORMAT_DIDL: FILE_TYPE_XMLETREE,
    FORMAT_EAD: FILE_TYPE_XMLETREE,
    FORMAT_ENDNOTEXML: FILE_TYPE_XMLETREE,
    FORMAT_HTML: FILE_TYPE_HTML,
    FORMAT_METAJSON: FILE_TYPE_JSON,
    FORMAT_METS: FILE_TYPE_XMLETREE,
    FORMAT_MIX: FILE_TYPE_XMLETREE,
    FORMAT_MODS: FILE_TYPE_XMLETREE,
    FORMAT_OAIDC: FILE_TYPE_XMLETREE,
    FORMAT_PREMIS: FILE_TYPE_XMLETREE,
    FORMAT_REPEC: FILE_TYPE_TXT,
    FORMAT_RESEARCHERML: FILE_TYPE_XMLETREE,
    FORMAT_RIS: FILE_TYPE_TXT,
    FORMAT_SUMMONJSON: FILE_TYPE_JSON,
    FORMAT_UNIMARC: FILE_TYPE_MARC,
    FORMAT_UNIXREF: FILE_TYPE_XMLETREE
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
    'dii': "urn:mpeg:mpeg21:2002:01-DII-NS",
    'dip': "urn:mpeg:mpeg21:2005:01-DIP-NS",
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
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'researcherml': "http://bibliotheque.sciences-po.fr/standards/researcherml/v1",
    'simpledc': "",
    'yt': "http://gdata.youtube.com/schemas/2007"
}

xmlns_to_input_format = {
    'http://schema.ccs-gmbh.com/ALTO': FORMAT_ALTO,
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://www.openarchives.org/OAI/2.0/oai_dc/': FORMAT_OAIDC,
    'urn:mpeg:mpeg21:2002:02-DIDL-NS': FORMAT_DIDL,
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
    'DIDL': FORMAT_DIDL,
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

DOC_TYPE_ANCIENTTEXT = "AncientText"
DOC_TYPE_ANNOTATIONARTICLE = "AnnotationArticle"
DOC_TYPE_ARTICLEREVIEW = "ArticleReview"
DOC_TYPE_ARTWORK = "Artwork"
DOC_TYPE_AUDIOBOOK = "AudioBook"
DOC_TYPE_AUDIOBROADCAST = "AudioBroadcast"
DOC_TYPE_AUDIOPART = "AudioPart"
DOC_TYPE_AUDIORECORDING = "AudioRecording"
DOC_TYPE_BIBLIOGRAPHY = "Bibliography"
DOC_TYPE_BILL = "Bill"  # Bill: a proposed Act (a draft) that is before the legislative assemblies for consideration.
DOC_TYPE_BOOK = "Book"
DOC_TYPE_BOOKLET = "Booklet"
DOC_TYPE_BOOKPART = "BookPart"
DOC_TYPE_BOOKREVIEW = "BookReview"
DOC_TYPE_CASEBRIEF = "CaseBrief"
DOC_TYPE_CHART = "Chart"
DOC_TYPE_CODE = "Code"
DOC_TYPE_CONFERENCECONTRIBUTION = "ConferenceContribution"
DOC_TYPE_CONFERENCEPAPER = "ConferencePaper"
DOC_TYPE_CONFERENCEPOSTER = "ConferencePoster"
DOC_TYPE_CONFERENCEPROCEEDINGS = "ConferenceProceedings"
DOC_TYPE_COURTREPORTER = "CourtReporter"
DOC_TYPE_CURRICULUMVITAE = "CurriculumVitae"
DOC_TYPE_DATABASE = "Database"
DOC_TYPE_DATASETQUALI = "DatasetQuali"
DOC_TYPE_DATASETQUANTI = "DatasetQuanti"
DOC_TYPE_DICTIONARY = "Dictionary"
DOC_TYPE_DICTIONARYENTRY = "DictionaryEntry"
DOC_TYPE_DISSERTATION = "Dissertation"
DOC_TYPE_DOCTORALTHESIS = "DoctoralThesis"
DOC_TYPE_DRAWING = "Drawing"
DOC_TYPE_EBOOK = "EBook"
DOC_TYPE_EJOURNAL = "EJournal"
DOC_TYPE_EDITEDBOOK = "EditedBook"
DOC_TYPE_EMAIL = "Email"
DOC_TYPE_ENCYCLOPEDIA = "Encyclopedia"
DOC_TYPE_ENCYCLOPEDIAARTICLE = "EncyclopediaArticle"
DOC_TYPE_ENGRAVE = "Engrave"
DOC_TYPE_EQUATION = "Equation"
DOC_TYPE_EXCERPT = "Excerpt"
DOC_TYPE_FILM = "Film"
DOC_TYPE_GOVERNMENTPUBLICATION = "GovernmentPublication"
DOC_TYPE_GRANT = "Grant"
DOC_TYPE_HEARING = "Hearing"
DOC_TYPE_IMAGE = "Image"
DOC_TYPE_INSTANTMESSAGE = "InstantMessage"
DOC_TYPE_INTERVIEWARTICLE = "InterviewArticle"
DOC_TYPE_JOURNAL = "Journal"
DOC_TYPE_JOURNALARTICLE = "JournalArticle"
DOC_TYPE_LEGALCASE = "LegalCase"
DOC_TYPE_LEGALDECISION = "LegalDecision"  # Judgment
DOC_TYPE_LETTER = "Letter"
DOC_TYPE_MAGAZINE = "Magazine"
DOC_TYPE_MAGAZINEARTICLE = "MagazineArticle"
DOC_TYPE_MANUEL = "Manuel"
DOC_TYPE_MANUSCRIPT = "Manuscript"
DOC_TYPE_MAP = "Map"
DOC_TYPE_MASTERTHESIS = "MasterThesis"
DOC_TYPE_MULTIVOLUMEBOOK = "MultiVolumeBook"
DOC_TYPE_MUSICALSCORE = "MusicalScore"
DOC_TYPE_MUSICRECORDING = "MusicRecording"
DOC_TYPE_NEWSPAPER = "Newspaper"
DOC_TYPE_NEWSPAPERARTICLE = "NewspaperArticle"
DOC_TYPE_NOTE = "Note"
DOC_TYPE_OFFPRINT = "OffPrint"
DOC_TYPE_PAINTING = "Painting"
DOC_TYPE_PATENT = "Patent"
DOC_TYPE_PERFORMANCE = "Performance"
DOC_TYPE_PERIODICALISSUE = "PeriodicalIssue"
DOC_TYPE_PERSONALCOMMUNICATION = "PersonalCommunication"
DOC_TYPE_PHOTOGRAPH = "Photograph"
DOC_TYPE_PHYSICALOBJECT = "PhysicalObject"
DOC_TYPE_POSTER = "Poster"
DOC_TYPE_PREPRINT = "Preprint"
DOC_TYPE_PROFESSORALTHESIS = "ProfessoralThesis"
DOC_TYPE_REPORT = "Report"
DOC_TYPE_REPORTPART = "ReportPart"
DOC_TYPE_RESEARCHPROPOSAL = "ResearchProposal"
DOC_TYPE_SERIES = "Series"
DOC_TYPE_SLIDE = "Slide"
DOC_TYPE_SOFTWARE = "Software"
DOC_TYPE_SPEECH = "Speech"
DOC_TYPE_STANDARD = "Standard"
DOC_TYPE_STATUTE = "Statute"  # Act / Statute: a bill passed and adopted by legislative assemblies that has become law.
DOC_TYPE_TREATY = "Treaty"
DOC_TYPE_TECHREPORT = "TechReport"
DOC_TYPE_TEST = "Test"
DOC_TYPE_UNPUBLISHEDDOCUMENT = "UnpublishedDocument"
DOC_TYPE_VIDEOBROADCAST = "VideoBroadcast"
DOC_TYPE_VIDEOPART = "VideoPart"
DOC_TYPE_VIDEORECORDING = "VideoRecording"
DOC_TYPE_WEBCLUSTER = "WebCluster"
DOC_TYPE_WEBPAGE = "WebPage"
DOC_TYPE_WEBPOST = "WebPost"
DOC_TYPE_WEBSECTION = "WebSection"
DOC_TYPE_WEBSITE = "WebSite"
DOC_TYPE_WORKINGPAPER = "WorkingPaper"
DOC_TYPE_WORKSHOP = "Workshop"

REC_STATUS_PRIVATE = "private"
REC_STATUS_PENDING = "pending"
REC_STATUS_REJECTED = "rejected"
REC_STATUS_PUBLISHED = "published"
REC_STATUS_DELETED = "deleted"
