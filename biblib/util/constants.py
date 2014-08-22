#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

BIBLIB_VERSION = '0.9'
METAJSON_VERSION = 1

FILE_TYPE_BIBTEX = 'bibtex'
FILE_TYPE_CSV = 'csv'
FILE_TYPE_PDF = 'pdf'
FILE_TYPE_HTML = 'html'
FILE_TYPE_JSON = 'json'
FILE_TYPE_MARC = 'marc'
FILE_TYPE_TXT = 'txt'
FILE_TYPE_XMLETREE = 'xmletree'

FORMAT_ALTO = 'alto'
FORMAT_BIBJSON = 'bibjson'
FORMAT_BIBTEX = 'bibtex'
FORMAT_CSV_METAJSON = 'csv_metajson'
FORMAT_CSV_SITPOL = 'csv_sitpol'
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
FORMAT_OAI_DC = 'oai_dc'
FORMAT_OPENURL = 'openurl'
FORMAT_OPENURLCOINS = 'openurlcoins'
FORMAT_PREMIS = 'premis'
FORMAT_REPEC = 'repec'
FORMAT_RESEARCHERML = 'researcherml'
FORMAT_RIS = 'ris'
FORMAT_SUMMONJSON = 'summonjson'
FORMAT_TEI = 'tei'
FORMAT_UNIMARC = 'unimarc'
FORMAT_UNIXREF = 'unixref'


STYLE_MLA = 'mla'


LANGUAGE_UNDETERMINED = "und"
CLASSIFICATION_UNDETERMINED = "und"

file_extension_to_file_type = {
    'bib': FILE_TYPE_BIBTEX,
    'csv': FILE_TYPE_CSV,
    'htm': FILE_TYPE_HTML,
    'html': FILE_TYPE_HTML,
    'json': FILE_TYPE_JSON,
    'marc': FILE_TYPE_MARC,
    'mrc': FILE_TYPE_MARC,
    'ris': FILE_TYPE_TXT,
    'txt': FILE_TYPE_TXT,
    'xml': FILE_TYPE_XMLETREE
}

file_type_to_file_extension = {
    FILE_TYPE_BIBTEX: 'bib',
    FILE_TYPE_CSV: 'csv',
    FILE_TYPE_PDF: 'pdf',
    FILE_TYPE_HTML: 'html',
    FILE_TYPE_JSON: 'json',
    FILE_TYPE_MARC: 'mrc',
    FILE_TYPE_TXT: 'ris',
    FILE_TYPE_XMLETREE: 'xml'
}

format_to_file_type = {
    FORMAT_ALTO: FILE_TYPE_XMLETREE,
    FORMAT_BIBJSON: FILE_TYPE_JSON,
    FORMAT_BIBTEX: FILE_TYPE_BIBTEX,
    FORMAT_CSV_METAJSON: FILE_TYPE_CSV,
    FORMAT_CSV_SITPOL: FILE_TYPE_CSV,
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
    FORMAT_OAI_DC: FILE_TYPE_XMLETREE,
    FORMAT_OPENURL: FILE_TYPE_XMLETREE,
    FORMAT_PREMIS: FILE_TYPE_XMLETREE,
    FORMAT_REPEC: FILE_TYPE_TXT,
    FORMAT_RESEARCHERML: FILE_TYPE_XMLETREE,
    FORMAT_RIS: FILE_TYPE_TXT,
    FORMAT_SUMMONJSON: FILE_TYPE_JSON,
    FORMAT_TEI: FILE_TYPE_XMLETREE,
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
    'foaf': "http://xmlns.com/foaf/0.1/",
    'gd': "http://schemas.google.com/g/2005",
    'gdocs': "http://schemas.google.com/docs/2007",
    'hal': "http://hal.archives-ouvertes.fr",
    'mml': "http://www.w3.org/1998/Math/MathML",
    'media': "http://search.yahoo.com/mrss/",
    'mets': "http://www.loc.gov/METS/",
    'mix': "http://www.loc.gov/mix/v20",
    'mods': "http://www.loc.gov/mods/v3",
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'oai_rem_rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'opensearch': "http://a9.com/-/spec/opensearch/1.1/",
    'opensearchrss': "http://a9.com/-/spec/opensearchrss/1.0/",
    'ore': "http://www.openarchives.org/ore/terms/",
    'org': "http://www.w3c.org/ns/org#",
    'owl': "http://www.w3.org/2002/07/owl#",
    'premis': "info:lc/xmlns/premis-v2",
    'qualifieddc': "",
    'rml': "http://bibliotheque.sciences-po.fr/standards/researcherml/v1",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'researcherml': "http://bibliotheque.sciences-po.fr/standards/researcherml/v1",
    'simpledc': "",
    'sioc': "http://rdfs.org/sioc/ns#",
    'ssdiag': "http://xml.serialssolutions.com/ns/diagnostics/v1.0",
    'ssopenurl': "http://xml.serialssolutions.com/ns/openurl/v1.0",
    'svg': "http://www.w3.org/2000/svg",
    'tech': "http://ccsd.cnrs.fr",
    'tei': "http://www.tei-c.org/ns/1.0",
    'xi': "http://www.w3.org/2001/XInclude",
    'xml': "http://www.w3.org/XML/1998/namespace",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'yt': "http://gdata.youtube.com/schemas/2007"
}

xmlns_schema_map = {
    'dc': "http://dublincore.org/schemas/xmls/simpledc20021212.xsd",
    'mods': "http://www.loc.gov/standards/mods/v3/mods-3-5.xsd",
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
}

xmlns_to_input_format = {
    'http://schema.ccs-gmbh.com/ALTO': FORMAT_ALTO,
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://www.openarchives.org/OAI/2.0/oai_dc/': FORMAT_OAI_DC,
    'urn:mpeg:mpeg21:2002:02-DIDL-NS': FORMAT_DIDL,
    'http://www.icpsr.umich.edu/DDI': FORMAT_DDI,
    'http://www.loc.gov/METS/': FORMAT_METS,
    'http://www.loc.gov/mix/v20': FORMAT_MIX,
    'http://www.loc.gov/mods/v3': FORMAT_MODS,
    'http://www.tei-c.org/ns/1.0': FORMAT_TEI,
    'info:lc/xmlns/premis-v2': FORMAT_PREMIS,
    'http://bibliotheque.sciences-po.fr/standards/researcherml/v1': FORMAT_RESEARCHERML
}

xmltag_to_input_format = {
    'alto': FORMAT_ALTO,
    'dc': FORMAT_OAI_DC,
    'codeBook': FORMAT_DDI,
    'DIDL': FORMAT_DIDL,
    'mets': FORMAT_METS,
    'mix': FORMAT_MIX,
    'mods': FORMAT_MODS,
    'modsCollection': FORMAT_MODS,
    'oai_dc': FORMAT_OAI_DC,
    'premis': FORMAT_PREMIS,
    'qualifieddc': FORMAT_OAI_DC,
    'researcherml': FORMAT_RESEARCHERML,
    'simpledc': FORMAT_OAI_DC,
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
    'TEI': FORMAT_TEI,
    'title': 'dc',
    'type': 'dc'
}

REC_CLASS_BRAND = "Brand"
REC_CLASS_CALL = "Call"
REC_CLASS_COLLECTION = "Collection"
REC_CLASS_DOCUMENT = "Document"
REC_CLASS_EVENT = "Event"
REC_CLASS_FAMILY = "Family"
REC_CLASS_FIELD = "Field"
REC_CLASS_ORGUNIT = "Orgunit"
REC_CLASS_PERSON = "Person"
REC_CLASS_PROJECT = "Project"
REC_CLASS_RESOURCE = "Resource"
REC_CLASS_SEARCH_QUERY = "SearchQuery"
REC_CLASS_SEARCH_RESPONSE = "SearchResponse"
REC_CLASS_SOFTWARE = "Software"
REC_CLASS_TARGET = "Target"
REC_CLASS_TYPE = "Type"
REC_CLASS_WARPPER = "Warpper"

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
DOC_TYPE_COLLECTION = "Collection"
DOC_TYPE_CONFERENCECONTRIBUTION = "ConferenceContribution"
DOC_TYPE_CONFERENCEPAPER = "ConferencePaper"
DOC_TYPE_CONFERENCEPOSTER = "ConferencePoster"
DOC_TYPE_CONFERENCEPROCEEDINGS = "ConferenceProceedings"
DOC_TYPE_COURTREPORTER = "CourtReporter"
DOC_TYPE_CURRICULUMVITAE = "CurriculumVitae"
DOC_TYPE_DATABASE = "Database"
DOC_TYPE_DATASET = "Dataset"
DOC_TYPE_DATASETQUALI = "DatasetQuali"
DOC_TYPE_DATASETQUANTI = "DatasetQuanti"
DOC_TYPE_DICTIONARY = "Dictionary"
DOC_TYPE_DICTIONARYENTRY = "DictionaryEntry"
DOC_TYPE_DISSERTATION = "Dissertation"
DOC_TYPE_DOCTORALTHESIS = "DoctoralThesis"
DOC_TYPE_DOCUMENT = "Document"
DOC_TYPE_DRAWING = "Drawing"
DOC_TYPE_EBOOK = "EBook"
DOC_TYPE_EDITEDBOOK = "EditedBook"
DOC_TYPE_EJOURNAL = "EJournal"
DOC_TYPE_EJOURNALARTICLE = "EJournalArticle"
DOC_TYPE_EMAIL = "Email"
DOC_TYPE_ENCYCLOPEDIA = "Encyclopedia"
DOC_TYPE_ENCYCLOPEDIAARTICLE = "EncyclopediaArticle"
DOC_TYPE_ENGRAVE = "Engrave"
DOC_TYPE_EQUATION = "Equation"
DOC_TYPE_ERESOURCE = "EResource"
DOC_TYPE_EVENT = "Event"
DOC_TYPE_EXCERPT = "Excerpt"
DOC_TYPE_FILM = "Film"
DOC_TYPE_FONT = "Font"
DOC_TYPE_GAME = "Game"
DOC_TYPE_GOVERNMENTPUBLICATION = "GovernmentPublication"
DOC_TYPE_GRANT = "Grant"
DOC_TYPE_HEARING = "Hearing"
DOC_TYPE_IMAGE = "Image"
DOC_TYPE_INSTANTMESSAGE = "InstantMessage"
DOC_TYPE_INTERVIEWARTICLE = "InterviewArticle"
DOC_TYPE_JOURNAL = "Journal"
DOC_TYPE_JOURNALARTICLE = "JournalArticle"
DOC_TYPE_KIT = "Kit"
DOC_TYPE_LEGALCASE = "LegalCase"
DOC_TYPE_LEGALDECISION = "LegalDecision"  # Judgment
DOC_TYPE_LETTER = "Letter"
DOC_TYPE_LOOSELEAFPUBLICATION = "LooseleafPublication"
DOC_TYPE_MAGAZINE = "Magazine"
DOC_TYPE_MAGAZINEARTICLE = "MagazineArticle"
DOC_TYPE_MANUEL = "Manuel"
DOC_TYPE_MANUSCRIPT = "Manuscript"
DOC_TYPE_MAP = "Map"
DOC_TYPE_MASTERTHESIS = "MasterThesis"
DOC_TYPE_MIXEDMATERIAL = "MixedMaterial"
DOC_TYPE_MULTIMEDIA = "Multimedia"
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
DOC_TYPE_PRESSCLIPPING = "PressClipping"
DOC_TYPE_PROFESSORALTHESIS = "ProfessoralThesis"
DOC_TYPE_REPORT = "Report"
DOC_TYPE_REPORTPART = "ReportPart"
DOC_TYPE_RESEARCHPROPOSAL = "ResearchProposal"
DOC_TYPE_SERIES = "Series"
DOC_TYPE_SERVICE = "Service"
DOC_TYPE_SLIDE = "Slide"
DOC_TYPE_SOFTWARE = "Software"
DOC_TYPE_SPEECH = "Speech"
DOC_TYPE_STANDARD = "Standard"
DOC_TYPE_STATUTE = "Statute"  # Act / Statute: a bill passed and adopted by legislative assemblies that has become law.
DOC_TYPE_TECHREPORT = "TechReport"
DOC_TYPE_TEST = "Test"
DOC_TYPE_TREATY = "Treaty"
DOC_TYPE_UNPUBLISHEDDOCUMENT = "UnpublishedDocument"
DOC_TYPE_VIDEOBROADCAST = "VideoBroadcast"
DOC_TYPE_VIDEOPART = "VideoPart"
DOC_TYPE_VIDEORECORDING = "VideoRecording"
DOC_TYPE_WEBARCHIVE = "WebArchive"
DOC_TYPE_WEBCLUSTER = "WebCluster"
DOC_TYPE_WEBENTITY = "WebEntity"
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

root_rec_type_to_is_part_of_rec_type = {
    DOC_TYPE_ANNOTATIONARTICLE: DOC_TYPE_JOURNAL,
    DOC_TYPE_ARTICLEREVIEW: DOC_TYPE_JOURNAL,
    DOC_TYPE_AUDIOPART: DOC_TYPE_AUDIORECORDING,
    DOC_TYPE_BOOK: DOC_TYPE_MULTIVOLUMEBOOK,
    DOC_TYPE_BOOKPART: DOC_TYPE_BOOK,
    DOC_TYPE_BOOKREVIEW: DOC_TYPE_JOURNAL,
    DOC_TYPE_CONFERENCEPAPER: DOC_TYPE_CONFERENCEPROCEEDINGS,
    DOC_TYPE_DICTIONARYENTRY: DOC_TYPE_DICTIONARY,
    DOC_TYPE_DOCUMENT: DOC_TYPE_DOCUMENT,
    DOC_TYPE_EBOOK: DOC_TYPE_MULTIVOLUMEBOOK,
    DOC_TYPE_EJOURNALARTICLE: DOC_TYPE_EJOURNAL,
    DOC_TYPE_ENCYCLOPEDIAARTICLE: DOC_TYPE_ENCYCLOPEDIA,
    DOC_TYPE_JOURNAL: DOC_TYPE_JOURNAL,
    DOC_TYPE_JOURNALARTICLE: DOC_TYPE_JOURNAL,
    DOC_TYPE_KIT: DOC_TYPE_COLLECTION,
    DOC_TYPE_MAGAZINEARTICLE: DOC_TYPE_MAGAZINE,
    DOC_TYPE_MANUSCRIPT: DOC_TYPE_MANUSCRIPT,
    DOC_TYPE_MAP: DOC_TYPE_BOOK,
    DOC_TYPE_NEWSPAPERARTICLE: DOC_TYPE_NEWSPAPER,
    DOC_TYPE_PERIODICALISSUE: DOC_TYPE_JOURNAL,
    DOC_TYPE_PRESSCLIPPING: DOC_TYPE_PRESSCLIPPING,
    DOC_TYPE_REPORTPART: DOC_TYPE_REPORT,
    DOC_TYPE_VIDEOPART: DOC_TYPE_VIDEORECORDING,
    DOC_TYPE_VIDEORECORDING: DOC_TYPE_VIDEORECORDING,
    DOC_TYPE_WEBSITE: DOC_TYPE_WEBARCHIVE
}

root_rec_type_to_has_part_rec_type = {
    DOC_TYPE_AUDIORECORDING: DOC_TYPE_AUDIOPART,
    DOC_TYPE_BOOK: DOC_TYPE_BOOKPART,
    DOC_TYPE_CONFERENCEPROCEEDINGS: DOC_TYPE_CONFERENCEPAPER,
    DOC_TYPE_DICTIONARY: DOC_TYPE_DICTIONARYENTRY,
    DOC_TYPE_DOCUMENT: DOC_TYPE_DOCUMENT,
    DOC_TYPE_EBOOK: DOC_TYPE_BOOKPART,
    DOC_TYPE_EJOURNAL: DOC_TYPE_EJOURNALARTICLE,
    DOC_TYPE_EJOURNALARTICLE: DOC_TYPE_EJOURNALARTICLE,
    DOC_TYPE_ENCYCLOPEDIA: DOC_TYPE_ENCYCLOPEDIAARTICLE,
    DOC_TYPE_KIT: DOC_TYPE_DOCUMENT,
    DOC_TYPE_MAGAZINE: DOC_TYPE_MAGAZINEARTICLE,
    DOC_TYPE_MANUSCRIPT: DOC_TYPE_MANUSCRIPT,
    DOC_TYPE_NEWSPAPER: DOC_TYPE_NEWSPAPERARTICLE,
    DOC_TYPE_JOURNAL: DOC_TYPE_JOURNALARTICLE,
    DOC_TYPE_JOURNALARTICLE: DOC_TYPE_JOURNALARTICLE,
    DOC_TYPE_PERIODICALISSUE: DOC_TYPE_JOURNALARTICLE,
    DOC_TYPE_PRESSCLIPPING: DOC_TYPE_PRESSCLIPPING,
    DOC_TYPE_REPORT: DOC_TYPE_REPORTPART,
    DOC_TYPE_VIDEORECORDING: DOC_TYPE_VIDEOPART,
    DOC_TYPE_WEBARCHIVE: DOC_TYPE_WEBSITE
}

DOC_TYPES_LIST_ARTICLES = [
    DOC_TYPE_ANNOTATIONARTICLE,
    DOC_TYPE_ARTICLEREVIEW,
    DOC_TYPE_BOOKREVIEW,
    DOC_TYPE_EJOURNALARTICLE,
    DOC_TYPE_INTERVIEWARTICLE,
    DOC_TYPE_JOURNALARTICLE,
    DOC_TYPE_MAGAZINEARTICLE,
    DOC_TYPE_NEWSPAPERARTICLE,
    DOC_TYPE_PERIODICALISSUE
]

csv_metajson_fieldnames = [
    "rec_id",
    "title"
]

TITLE_NON_SORT = {
    "en": [
        "a",
        "about",
        "above",
        "across",
        "after",
        "again",
        "against",
        "almost",
        "along",
        "always",
        "am",
        "an",
        "and",
        "another",
        "any",
        "anybody",
        "anything",
        "anyway",
        "anywhere",
        "are",
        "around",
        "as",
        "aside",
        "at",
        "away",
        "be",
        "because",
        "been",
        "before",
        "behind",
        "below",
        "beneath",
        "beside",
        "between",
        "beyond",
        "both",
        "but",
        "can",
        "cannot",
        "could",
        "did",
        "do ",
        "does",
        "done",
        "down",
        "during",
        "each",
        "else",
        "elsewhere",
        "enough",
        "even",
        "ever",
        "every",
        "everything",
        "everywhere",
        "followed",
        "following",
        "for",
        "forever",
        "forward",
        "from",
        "further",
        "furthermore",
        "had",
        "has",
        "have",
        "he",
        "hence",
        "her",
        "here",
        "hers",
        "herself",
        "him",
        "himself",
        "his",
        "i",
        "if",
        "in",
        "inside",
        "into",
        "is",
        "it",
        "its",
        "itself",
        "like",
        "me",
        "mine",
        "more",
        "my",
        "myself",
        "never",
        "no",
        "nor",
        "not",
        "nothing",
        "of",
        "on",
        "or",
        "other",
        "others",
        "otherwise",
        "our",
        "ourselves",
        "out",
        "outside",
        "over",
        "overall",
        "shall",
        "she",
        "should",
        "since",
        "so",
        "some",
        "somebody",
        "somehow",
        "sometimes",
        "somewhat",
        "somewhere",
        "that",
        "the",
        "their",
        "them",
        "themselves",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "thus",
        "till",
        "to",
        "too",
        "toward",
        "towards",
        "under",
        "until",
        "upon",
        "very",
        "was",
        "we",
        "were",
        "what",
        "whatever",
        "when",
        "where",
        "whereas",
        "whereby",
        "wherein",
        "wherever",
        "whether",
        "which",
        "while",
        "who",
        "whom",
        "whose",
        "with",
        "within",
        "without",
        "would",
        "yet",
        "you",
        "your",
        "yours",
        "yourself"
    ],
    "fr": [
        "à",
        "au",
        "auprès",
        "autre",
        "autres",
        "aux",
        "avec",
        "c",
        "ce",
        "celle",
        "celles",
        "ces",
        "cet",
        "cette",
        "ceux",
        "chez",
        "d",
        "dans",
        "de",
        "derrière",
        "des",
        "devant",
        "dont",
        "du",
        "elle",
        "elles",
        "en",
        "et",
        "eux",
        "il",
        "ils",
        "je",
        "l",
        "la",
        "le",
        "les",
        "m",
        "ma",
        "me",
        "mes",
        "mon",
        "n",
        "ne",
        "ni",
        "nous",
        "on",
        "ou",
        "où",
        "par",
        "pendant",
        "pour",
        "près",
        "qu",
        "que",
        "quel",
        "quelle",
        "quelles",
        "quelqu",
        "quelque",
        "quelques",
        "quels",
        "qui",
        "s",
        "sa",
        "sans",
        "se",
        "ses",
        "suivi",
        "suivie",
        "suivies",
        "suivis",
        "sur",
        "t",
        "ta",
        "te",
        "tes",
        "tu",
        "un",
        "une",
        "uns",
        "vous",
        "y"
    ],
    "de": [
        "ab",
        "alle",
        "allem",
        "allen",
        "aller",
        "alles",
        "als",
        "am",
        "an",
        "andere",
        "anderem",
        "anderen",
        "anderer",
        "anderes",
        "auf",
        "aufs",
        "bei",
        "beim",
        "bevor",
        "bis",
        "das",
        "dass",
        "dein",
        "deine",
        "deinem",
        "deinen",
        "deiner",
        "deines",
        "dem",
        "den",
        "denen",
        "der",
        "deren",
        "derer",
        "des",
        "dessen",
        "die",
        "dies",
        "diese",
        "diesen",
        "dieser",
        "dieses",
        "durch",
        "ein",
        "eine",
        "einem",
        "einen",
        "einer",
        "eines",
        "er",
        "es",
        "euch",
        "euer",
        "eure",
        "eurem",
        "euren",
        "eurer",
        "eures",
        "für",
        "fürs",
        "gegen",
        "gemäss",
        "ihm",
        "ihn",
        "ihnen",
        "ihr",
        "ihre",
        "ihrem",
        "ihren",
        "ihrer",
        "ihres",
        "im",
        "in",
        "insbesondere",
        "irgenwelche",
        "irgenwelchem",
        "irgenwelcher",
        "irgenwelches",
        "jede",
        "jedem",
        "jeden",
        "jeder",
        "jedes",
        "jene",
        "jenem",
        "jenen",
        "jener",
        "jenes",
        "kein",
        "keine",
        "keinem",
        "keinen",
        "keiner",
        "keines",
        "manch",
        "manche",
        "manchem",
        "mancher",
        "manches",
        "mein",
        "meine",
        "meinem",
        "meinen",
        "meiner",
        "meines",
        "mit",
        "oder",
        "ohne",
        "sein",
        "seine",
        "seinem",
        "seinen",
        "seiner",
        "seines",
        "seit",
        "sie",
        "sondern",
        "sowie",
        "über",
        "überm",
        "übers",
        "um",
        "und",
        "uns",
        "unser",
        "unsere",
        "unserem",
        "unseren",
        "unserer",
        "unseres",
        "unserm",
        "unsern",
        "unsers",
        "unter",
        "verschieden",
        "verschiedene",
        "verschiedenem",
        "verschiedenen",
        "verschiedener",
        "verschiedenes",
        "vom",
        "von",
        "vor",
        "wegen",
        "welch",
        "welche",
        "welchem",
        "welchen",
        "welcher",
        "welches",
        "wem",
        "wen",
        "wenn",
        "were",
        "zu",
        "zum",
        "zur"
    ],
    "it": [
        "agli",
        "ai",
        "al",
        "all",
        "alla",
        "alle",
        "allo",
        "altra",
        "altre",
        "altri",
        "altro",
        "c",
        "che",
        "chi",
        "ci",
        "ciò",
        "cioè",
        "codesta",
        "codeste",
        "codesti",
        "codesto",
        "cogli",
        "coi",
        "col",
        "colà",
        "coll",
        "coloro",
        "come",
        "con",
        "contro",
        "cosi",
        "costà",
        "costei",
        "costi",
        "costoro",
        "costui",
        "cui",
        "d",
        "da",
        "dagli",
        "dal",
        "dall",
        "dalla",
        "dalle",
        "dallo",
        "davanti",
        "del",
        "dell",
        "della",
        "delle",
        "dello",
        "dentro",
        "di",
        "dietro",
        "dopo",
        "dove",
        "durante",
        "egli",
        "ella",
        "essa",
        "esse",
        "essi",
        "esso",
        "fra",
        "gl",
        "gli",
        "gliela",
        "gliele",
        "glielo",
        "gliene",
        "il",
        "in",
        "io",
        "l",
        "la",
        "là",
        "le",
        "lei",
        "li",
        "lo",
        "loro",
        "lui",
        "ma",
        "me",
        "menos",
        "mi",
        "mia",
        "miei",
        "mientras",
        "moi",
        "ne",
        "nè",
        "negli",
        "nei",
        "nel",
        "nell",
        "nella",
        "nelle",
        "nello",
        "no",
        "noi",
        "non",
        "nostra",
        "nostre",
        "nostri",
        "nostro",
        "ovvero",
        "percio",
        "pero",
        "piu",
        "qua",
        "qual",
        "quale",
        "quali",
        "quanta",
        "quante",
        "quanti",
        "quanto",
        "quegli",
        "quei",
        "quel",
        "quell",
        "quella",
        "quelle",
        "quelli",
        "quello",
        "quest",
        "questa",
        "queste",
        "questi",
        "questo",
        "qui",
        "se",
        "sè",
        "si",
        "sopra",
        "sotto",
        "su",
        "sua",
        "sue",
        "sugli",
        "sui",
        "sul",
        "sull",
        "sulla",
        "sulle",
        "sullo",
        "suo",
        "suoi",
        "tanto",
        "ti",
        "tras",
        "tu",
        "tua",
        "tue",
        "tuo",
        "tuoi",
        "un",
        "un",
        "una",
        "uno",
        "v",
        "vi",
        "voi",
        "vostra",
        "vostre",
        "vostri",
        "vostro"
    ],
    "ru": [
        "â",
        "bez",
        "dlâ",
        "gde",
        "ili",
        "iz",
        "kak",
        "kotoraâ",
        "kotoroë",
        "kotorye",
        "kotoryj",
        "moâ",
        "moë",
        "moi",
        "moj",
        "my",
        "na",
        "nekotoraâ",
        "nekotoroë",
        "nekotorye",
        "nekotoryj",
        "ob",
        "odin",
        "odna",
        "odni",
        "okolo",
        "on",
        "ona",
        "oni",
        "ot",
        "pered",
        "posie",
        "pri",
        "protiv",
        "svoâ",
        "svoë",
        "svoi",
        "svoj",
        "tvoâ",
        "tvoë",
        "tvoi",
        "tvoj",
        "ty",
        "v tecenie",
        "vy",
        "za"
    ],
    "es": [
        "acà",
        "adónde",
        "adónde",
        "afuera",
        "ahí",
        "ahora",
        "al",
        "alguien",
        "algún",
        "alguna",
        "alguno",
        "ante",
        "antes",
        "apenas",
        "aquél",
        "aquélla",
        "aquéllas",
        "aquello",
        "aquéllos",
        "aquí",
        "así",
        "aún",
        "aunque",
        "bajo",
        "bastante ",
        "cada",
        "calquier",
        "calquiera",
        "casi",
        "cómo",
        "con",
        "conmigo",
        "consigo",
        "contigo",
        "cuàl",
        "cuales",
        "cualesquier",
        "cualesquiera",
        "cuàn",
        "cuando",
        "cuanta",
        "cuantas",
        "cuanto",
        "cuantos",
        "cuya",
        "cuyas",
        "cuyo",
        "cuyos",
        "de",
        "del",
        "demás",
        "demasiada",
        "demasiadas",
        "demasiado",
        "demasiados",
        "desde",
        "después",
        "detrás",
        "dondequiere",
        "durante",
        "él",
        "ella",
        "ellas",
        "ello",
        "ellos",
        "en",
        "entonces",
        "entre",
        "ésa",
        "ésas",
        "ése",
        "eso",
        "ésos",
        "ésta",
        "éstas",
        "éste",
        "esto",
        "éstos",
        "fuera",
        "hasta",
        "jamás",
        "la",
        "las",
        "le",
        "lejos",
        "les",
        "lo",
        "los",
        "luego",
        "más",
        "menos",
        "mí",
        "mía",
        "mías",
        "mientras",
        "mío",
        "míos",
        "mis",
        "misma",
        "mismas",
        "mismo",
        "mismos",
        "mucha",
        "muchas",
        "mucho",
        "muchos",
        "muy",
        "nada",
        "ningún",
        "ninguna",
        "ninguno",
        "no",
        "nos",
        "nosotras",
        "nosotros",
        "nuestra",
        "nuestras",
        "nuestro",
        "nuestros",
        "otra",
        "otras",
        "otro",
        "otros",
        "para",
        "pero",
        "poca",
        "pocas",
        "poco",
        "pocos",
        "por",
        "porque",
        "pues",
        "que",
        "quién",
        "quiénes",
        "quienesquiera",
        "quienquiera",
        "se",
        "sí",
        "siempre",
        "sin",
        "so",
        "sobre",
        "su",
        "sus",
        "suya",
        "suyas",
        "suyo",
        "suyos",
        "tal",
        "también",
        "tampoco",
        "tan",
        "tanta",
        "tantas",
        "tanto",
        "tantos",
        "te",
        "ti",
        "toda",
        "todas",
        "todavía",
        "todo",
        "todos",
        "tras",
        "tú",
        "tus",
        "tuya",
        "tuyo",
        "tuyos",
        "un",
        "una",
        "unas",
        "uno",
        "unos",
        "vos",
        "vosotras",
        "vosotros",
        "vuestra",
        "vuestras",
        "vuestro",
        "vuestros",
        "ya",
        "yo"
    ]
}
