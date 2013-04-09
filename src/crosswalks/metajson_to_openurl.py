#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import urllib
from xml.sax.saxutils import quoteattr
from metadatas import metajson_contrib_util

metajson_type_to_openurl_book_genre = {
    "Book" : "book",
    "BookPart" : "book",
    "ConferencePaper" : "conference",
    "ConferenceProceedings" : "proceeding",
    "Dictionary" : "book",
    "Document" : "unknown",
    "EditedBook" : "book",
    "Encyclopedia" : "book",
    "Report" : "report"
}

metajson_type_to_openurl_dissertation = {
    "DoctoralThesis" : "dissertation",
    "MasterThesis" : "dissertation",
    "ProfessoralThesis" : "dissertation",
    "Thesis" : "dissertation"
}

metajson_type_to_openurl_journal_genre = {
    "Annotation" : "article",
    "Article" : "article",
    "BookReview" : "article",
    "ConferencePaper" : "conference",
    "ConferenceProceedings" : "proceeding",
    "Document" : "unknown",
    "InterviewArticle" : "article",
    "Journal" : "journal",
    "JournalArticle" : "article",
    "Magazine" : "journal",
    "MagazineArticle" : "article",
    "Newspaper" : "journal",
    "NewspaperArticle" : "article",
    "Periodical" : "journal",
    "PeriodicalIssue" : "issue",
    "Preprint" : "issue"
}

metajson_type_to_openurl_patent = {
    "Patent" : "patent"
}

def convert_metajson_document_to_openurl(document):
    # ctx_ver
    openurl = {"ctx_ver" : "Z39.88-2004"}

    # rft_val_fmt
    rft_val_fmt_book = "info:ofi/fmt:kev:mtx:book"
    # http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:book

    rft_val_fmt_journal="info:ofi/fmt:kev:mtx:journal"
    # http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:journal

    rft_val_fmt_dissertation="info:ofi/fmt:kev:mtx:dissertation"
    # http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:dissertation

    rft_val_fmt_patent="info:ofi/fmt:kev:mtx:patent"
    # http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:patent

    rec_type=document["rec_type"]

    if rec_type in metajson_type_to_openurl_book_genre :
        # book
        openurl["rft_val_fmt"]=rft_val_fmt_book

        # genre
        openurl["rft.genre"]=metajson_type_to_openurl_book_genre[rec_type]
        
        # atitle, btitle
        if "is_part_of" in document and "title" in document["is_part_of"] :
            openurl["rft.atitle"]=document["title"]
            openurl["rft.btitle"]=document["is_part_of"]["title"]
        else :
            openurl["rft.btitle"]=document["title"]

        # place
        place = document.get_publisher_place()
        if place : openurl["rft.place"] = place

        # pub
        pub = document.get_publisher()
        if pub : openurl["rft.pub"] = pub

        # edition
        edition = document.get_edition()
        if edition : openurl["rft.edition"] = edition

        # series
        series = document.get_series_title()
        if series : openurl["rft.series"] = series

        # bici
        bici = document.get_first_value_for_type_in_list_from_all_level("identifiers", "bici")
        if bici : openurl["rft.bici"] = bici

    elif rec_type in metajson_type_to_openurl_journal_genre :
        # journal
        openurl["rft_val_fmt"]=rft_val_fmt_journal

        # genre
        openurl["rft.genre"]=metajson_type_to_openurl_journal_genre[rec_type]

        # atitle, jtitle
        if "is_part_of" in document and "title" in document["is_part_of"] :
            openurl["rft.atitle"]=document["title"]
            openurl["rft.jtitle"]=document["is_part_of"]["title"]
        else :
            openurl["rft.jtitle"]=document["title"]

        # chron

        # ssn

        # quarter

        # volume
        volume = document.get_part_volume()
        if volume : openurl["rft.volume"] = volume

        # part
        part = document.get_part_name()
        if part : openurl["rft.part"] = part

        # issue
        issue = document.get_part_issue()
        if issue : openurl["rft.issue"] = issue

        # artnum
        artnum = document.get_first_value_for_type_in_list_from_all_level("identifiers", "artnum")
        if artnum : openurl["rft.artnum"] = artnum

        # eissn
        eissn = document.get_first_value_for_type_in_list_from_all_level("identifiers", "eissn")
        if eissn : openurl["rft.eissn"] = eissn

        # coden
        coden = document.get_first_value_for_type_in_list_from_all_level("identifiers", "coden")
        if coden : openurl["rft.coden"] = coden

        # sici
        sici = document.get_first_value_for_type_in_list_from_all_level("identifiers", "sici")
        if sici : openurl["rft.sici"] = sici


    elif rec_type in metajson_type_to_openurl_dissertation :
        # dissertation
        openurl["rft_val_fmt"]=rft_val_fmt_dissertation

        # title
        openurl["rft.atitle"]=document["title"]

        # au
        aus = document.get_contributors_by_role("aut")
        if len(aus) > 0 :
            openurl["rft.au"]=aus[0].get_formated_name()

        # cc
        cc = document.get_publisher_country()
        if cc : openurl["rft.cc"] = cc

        # inst
        insts = document.get_contributors_by_role("dgg")
        if len(insts) > 0 :
            openurl["rft.inst"]=insts[0].get_formated_name()

        # advisor
        advisors = document.get_contributors_by_role("dgg")
        if len(advisors) > 0 :
            openurl["rft.advisor"]=advisors[0].get_formated_name()

        # degree
        degree = document.get_type_degree()
        if degree : openurl["rft.degree"] = degree


    elif rec_type in metajson_type_to_openurl_patent :
        # patent
        openurl["rft_val_fmt"]=rft_val_fmt_patent

        # title
        openurl["rft.atitle"]=document["title"]

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


    # No mapping for Z39.88 OpenURL : Exit !
    if "rft_val_fmt" not in openurl : return None

    # common properties for all types

    # rft_id : doi or resource.url
    doi = document.get_first_value_for_type_in_list_from_all_level("identifiers", "doi")
    if doi : openurl["rft_id"] = doi
    elif "resources" in document :
        resource_url = document.get_property_for_item_in_list("resources", "url")
        if resource_url : openurl["rft_id"] = resource_url

    # date
    date = document.get_date()
    if date : openurl["rft.date"] = date

    if openurl["rft_val_fmt"] in [rft_val_fmt_book, rft_val_fmt_dissertation, rft_val_fmt_journal] :
        # common properties for book, dissertation and journal

        # isbn
        isbn = document.get_first_value_for_type_in_list_from_all_level("identifiers", "isbn")
        if isbn : openurl["rft.isbn"] = isbn

    if openurl["rft_val_fmt"] in [rft_val_fmt_book, rft_val_fmt_journal] :
        # common properties for book and journal

        # au, aucorp
        if "contributors" in document :
            for contributor in document["contributors"] :
                if contributor["role"] in metajson_contrib_util.contributor_citable_roles :
                    if "rft.au" not in openurl and contributor["type"]=="person" :
                        openurl["rft.au"]=contributor.get_formated_name()
                    elif "rft.aucorp" not in openurl and contributor["type"]=="orgunit" :
                        openurl["rft.aucorp"]=contributor.get_formated_name()

        # issn
        issn = document.get_first_value_for_type_in_list_from_all_level("identifiers", "issn")
        if issn : openurl["rft.issn"] = issn

        # spage
        spage = document.get_part_page_start()
        if spage : openurl["rft.spage"] = spage

        # epage
        epage = document.get_part_page_end()
        if epage : openurl["rft.epage"] = epage


    if openurl["rft_val_fmt"] in [rft_val_fmt_book, rft_val_fmt_dissertation] :
        # common properties for book and dissertation

        # tpages
        tpages = document.get_extent_pages()
        if tpages : openurl["rft.tpages"] = tpages

    openurl_str = {}
    for k, v in openurl.iteritems():
        openurl_str[k] = unicode(v).encode('utf-8')
    result = quoteattr(urllib.urlencode(openurl_str))
    #print result
    return result


def convert_metajson_document_to_openurl_coins(document):
    result = convert_metajson_document_to_openurl(document)
    if result : return "<span class=\"Z3988\" title=" + result + "></span>"
    else : return ""