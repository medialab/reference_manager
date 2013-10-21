#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import urllib
from xml.sax.saxutils import quoteattr
from biblib.services import creator_service
from biblib.util import constants

GENRE_BOOK_BOOK = "book"
GENRE_BOOK_CONFERENCE = "conference"
GENRE_BOOK_PROCEEDING = "proceeding"
GENRE_BOOK_REPORT = "report"
GENRE_BOOK_UNKNOWN = "unknown"

GENRE_DISSERTATION = "dissertation"

GENRE_JOURNAL_ARTICLE = "article"
GENRE_JOURNAL_CONFERENCE = "conference"
GENRE_JOURNAL_ISSUE = "issue"
GENRE_JOURNAL_JOURNAL = "journal"
GENRE_JOURNAL_PROCEEDING = "proceeding"
GENRE_JOURNAL_UNKNOWN = "unknown"

GENRE_PATENT = "patent"

metajson_type_to_openurl_book_genre = {
    constants.DOC_TYPE_BOOK: GENRE_BOOK_BOOK,
    constants.DOC_TYPE_BOOKLET: GENRE_BOOK_BOOK,
    constants.DOC_TYPE_BOOKPART: GENRE_BOOK_BOOK,
    constants.DOC_TYPE_CONFERENCEPAPER: GENRE_BOOK_CONFERENCE,
    constants.DOC_TYPE_CONFERENCEPROCEEDINGS: GENRE_BOOK_PROCEEDING,
    constants.DOC_TYPE_DICTIONARY: GENRE_BOOK_BOOK,
    constants.DOC_TYPE_EBOOK: GENRE_BOOK_BOOK,
    constants.DOC_TYPE_EDITEDBOOK: GENRE_BOOK_BOOK,
    constants.DOC_TYPE_ENCYCLOPEDIA: GENRE_BOOK_BOOK,
    constants.DOC_TYPE_MULTIVOLUMEBOOK: GENRE_BOOK_BOOK,
    constants.DOC_TYPE_REPORT: GENRE_BOOK_REPORT,
    constants.DOC_TYPE_UNPUBLISHEDDOCUMENT: GENRE_BOOK_UNKNOWN
}

metajson_type_to_openurl_dissertation_genre = {
    constants.DOC_TYPE_DISSERTATION: GENRE_DISSERTATION,
    constants.DOC_TYPE_DOCTORALTHESIS: GENRE_DISSERTATION,
    constants.DOC_TYPE_MASTERTHESIS: GENRE_DISSERTATION,
    constants.DOC_TYPE_PROFESSORALTHESIS: GENRE_DISSERTATION
}

metajson_type_to_openurl_journal_genre = {
    constants.DOC_TYPE_ANNOTATIONARTICLE: GENRE_JOURNAL_ARTICLE,
    constants.DOC_TYPE_ARTICLEREVIEW: GENRE_JOURNAL_ARTICLE,
    constants.DOC_TYPE_BOOKREVIEW: GENRE_JOURNAL_ARTICLE,
    constants.DOC_TYPE_CONFERENCEPAPER: GENRE_JOURNAL_CONFERENCE,
    constants.DOC_TYPE_CONFERENCEPROCEEDINGS: GENRE_JOURNAL_PROCEEDING,
    constants.DOC_TYPE_EJOURNAL: GENRE_JOURNAL_JOURNAL,
    constants.DOC_TYPE_INTERVIEWARTICLE: GENRE_JOURNAL_ARTICLE,
    constants.DOC_TYPE_JOURNAL: GENRE_JOURNAL_JOURNAL,
    constants.DOC_TYPE_JOURNALARTICLE: GENRE_JOURNAL_ARTICLE,
    constants.DOC_TYPE_MAGAZINE: GENRE_JOURNAL_JOURNAL,
    constants.DOC_TYPE_MAGAZINEARTICLE: GENRE_JOURNAL_ARTICLE,
    constants.DOC_TYPE_NEWSPAPER: GENRE_JOURNAL_JOURNAL,
    constants.DOC_TYPE_NEWSPAPERARTICLE: GENRE_JOURNAL_ARTICLE,
    constants.DOC_TYPE_PERIODICALISSUE: GENRE_JOURNAL_ISSUE,
    constants.DOC_TYPE_PREPRINT: GENRE_JOURNAL_UNKNOWN
}

metajson_type_to_openurl_patent = {
    constants.DOC_TYPE_PATENT: GENRE_PATENT
}


def metajson_to_openurl(document):
    # ctx_ver
    openurl = {"ctx_ver": "Z39.88-2004"}

    # rft_val_fmt
    rft_val_fmt_book = "info:ofi/fmt:kev:mtx:book"
    # http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:book

    rft_val_fmt_journal = "info:ofi/fmt:kev:mtx:journal"
    # http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:journal

    rft_val_fmt_dissertation = "info:ofi/fmt:kev:mtx:dissertation"
    # http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:dissertation

    rft_val_fmt_patent = "info:ofi/fmt:kev:mtx:patent"
    # http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:patent

    if "rec_type" not in document:
        return

    rec_type = document["rec_type"]

    if rec_type in metajson_type_to_openurl_book_genre:
        # book
        openurl["rft_val_fmt"] = rft_val_fmt_book

        # genre
        openurl["rft.genre"] = metajson_type_to_openurl_book_genre[rec_type]

        # atitle, btitle
        if "is_part_ofs" in document and "title" in document["is_part_ofs"][0]:
            openurl["rft.atitle"] = document["title"]
            openurl["rft.btitle"] = document["is_part_ofs"][0]["title"]
        else:
            openurl["rft.btitle"] = document["title"]

        # place
        publication_places = document.get_publication_places()
        if publication_places:
            openurl["rft.place"] = publication_places[0]

        # pub
        publishers = document.get_publishers()
        if publishers:
            openurl["rft.pub"] = publishers[0]

        # edition
        edition = document.get_edition()
        if edition:
            openurl["rft.edition"] = edition

        # series
        series = document.get_series_title()
        if series:
            openurl["rft.series"] = series

        # bici
        bici = document.get_first_value_for_type_in_list_from_all_level("identifiers", "bici")
        if bici:
            openurl["rft.bici"] = bici

    elif rec_type in metajson_type_to_openurl_journal_genre:
        # journal
        openurl["rft_val_fmt"] = rft_val_fmt_journal

        # genre
        openurl["rft.genre"] = metajson_type_to_openurl_journal_genre[rec_type]

        # atitle, jtitle
        if "is_part_ofs" in document and "title" in document["is_part_ofs"][0]:
            openurl["rft.atitle"] = document["title"]
            openurl["rft.jtitle"] = document["is_part_ofs"][0]["title"]
        else:
            openurl["rft.jtitle"] = document["title"]

        # chron

        # ssn

        # quarter

        # volume
        volume = document.get_part_volume()
        if volume:
            openurl["rft.volume"] = volume

        # part
        part = document.get_part_name()
        if part:
            openurl["rft.part"] = part

        # issue
        issue = document.get_part_issue()
        if issue:
            openurl["rft.issue"] = issue

        # artnum
        artnum = document.get_first_value_for_type_in_list_from_all_level("identifiers", "artnum")
        if artnum:
            openurl["rft.artnum"] = artnum

        # eissn
        eissn = document.get_first_value_for_type_in_list_from_all_level("identifiers", "eissn")
        if eissn:
            openurl["rft.eissn"] = eissn

        # coden
        coden = document.get_first_value_for_type_in_list_from_all_level("identifiers", "coden")
        if coden:
            openurl["rft.coden"] = coden

        # sici
        sici = document.get_first_value_for_type_in_list_from_all_level("identifiers", "sici")
        if sici:
            openurl["rft.sici"] = sici

    elif rec_type in metajson_type_to_openurl_dissertation_genre:
        # dissertation
        openurl["rft_val_fmt"] = rft_val_fmt_dissertation

        # title
        openurl["rft.atitle"] = document["title"]

        # au
        aus = document.get_creators_by_role("aut")
        if len(aus) > 0:
            openurl["rft.au"] = aus[0].formatted_name()

        # cc
        publication_countries = document.get_publication_countries()
        if publication_countries:
            openurl["rft.cc"] = publication_countries[0]

        # inst
        insts = document.get_creators_by_role("dgg")
        if len(insts) > 0:
            openurl["rft.inst"] = insts[0].formatted_name()

        # advisor
        advisors = document.get_creators_by_role("dgg")
        if len(advisors) > 0:
            openurl["rft.advisor"] = advisors[0].formatted_name()

        # degree
        degree = document.get_type_degree()
        if degree:
            openurl["rft.degree"] = degree

    elif rec_type in metajson_type_to_openurl_patent:
        # patent
        openurl["rft_val_fmt"] = rft_val_fmt_patent

        # title
        openurl["rft.atitle"] = document["title"]

        # inventor

        # cc

        # kind

        # applcc

        # applnumber

        # number

        # applyear

        # appldate

        # assignee

        # pubdate

        # prioritydate

    # No mapping for Z39.88 OpenURL: Exit !
    if "rft_val_fmt" not in openurl:
        return None

    # common properties for all types

    # rft_id: doi or resource.url
    doi = document.get_first_value_for_type_in_list_from_all_level("identifiers", "doi")
    if doi:
        openurl["rft_id"] = doi
    elif "resources" in document:
        resource_url = document.get_property_for_item_in_list("resources", "url")
        if resource_url:
            openurl["rft_id"] = resource_url

    # date
    date = document.get_date()
    if date:
        openurl["rft.date"] = date

    if openurl["rft_val_fmt"] in [rft_val_fmt_book, rft_val_fmt_dissertation, rft_val_fmt_journal]:
        # common properties for book, dissertation and journal

        # isbn
        isbn = document.get_first_value_for_type_in_list_from_all_level("identifiers", "isbn")
        if isbn:
            openurl["rft.isbn"] = isbn

    if openurl["rft_val_fmt"] in [rft_val_fmt_book, rft_val_fmt_journal]:
        # common properties for book and journal

        # au, aucorp
        if "creators" in document:
            for creator in document["creators"]:
                if "role" in creator and creator["role"] in creator_service.creator_citable_roles:
                    if "rft.au" not in openurl and "person" in creator:
                        openurl["rft.au"] = creator.formatted_name()
                    elif "rft.aucorp" not in openurl and "orgunit" in creator:
                        openurl["rft.aucorp"] = creator.formatted_name()

        # issn
        issn = document.get_first_value_for_type_in_list_from_all_level("identifiers", "issn")
        if issn:
            openurl["rft.issn"] = issn

        # spage
        spage = document.get_part_page_begin()
        if spage:
            openurl["rft.spage"] = spage

        # epage
        epage = document.get_part_page_end()
        if epage:
            openurl["rft.epage"] = epage

    if openurl["rft_val_fmt"] in [rft_val_fmt_book, rft_val_fmt_dissertation]:
        # common properties for book and dissertation

        # tpages
        tpages = document.get_extent_pages()
        if tpages:
            openurl["rft.tpages"] = tpages

    openurl_str = {}
    for k, v in openurl.iteritems():
        openurl_str[k] = unicode(v).encode('utf-8')
    result = quoteattr(urllib.urlencode(openurl_str))
    #print result
    return result


def metajson_to_openurlcoins(document):
    result = metajson_to_openurl(document)
    if result:
        return "<span class=\"Z3988\" title=" + result + "></span>"
    else:
        return ""
