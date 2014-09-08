#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import urllib
from xml.sax.saxutils import quoteattr

from biblib.metajson import Document
from biblib.metajson import Identifier
from biblib.metajson import Resource
from biblib.services import creator_service
from biblib.util import constants
from biblib.util import xmletree
from biblib.util import jsonbson

CTX_VER = "Z39.88-2004"

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

# rft_val_fmt
RFT_VAL_FMT_BOOK = "info:ofi/fmt:kev:mtx:book"
# http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:book
RFT_VAL_FMT_JOURNAL = "info:ofi/fmt:kev:mtx:journal"
# http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:journal
RFT_VAL_FMT_DISSERTATION = "info:ofi/fmt:kev:mtx:dissertation"
# http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:dissertation
RFT_VAL_FMT_PATENT = "info:ofi/fmt:kev:mtx:patent"
# http://alcme.oclc.org/openurl/servlet/OAIHandler/extension?verb=GetMetadata&metadataPrefix=mtx&identifier=info:ofi/fmt:kev:mtx:patent

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


def metajson_to_openurl_params(document):
    # ctx_ver
    openurl = {"ctx_ver": CTX_VER}

    if "rec_type" not in document:
        return

    rec_type = document["rec_type"]

    if rec_type in metajson_type_to_openurl_book_genre:
        # book
        openurl["rft_val_fmt"] = RFT_VAL_FMT_BOOK

        # genre
        openurl["rft.genre"] = metajson_type_to_openurl_book_genre[rec_type]

        # atitle, btitle
        if "is_part_ofs" in document and "title" in document["is_part_ofs"][0]:
            openurl["rft.atitle"] = document["title"]
            openurl["rft.btitle"] = document["is_part_ofs"][0]["title"]
        elif "title" in document:
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
        openurl["rft_val_fmt"] = RFT_VAL_FMT_JOURNAL

        # genre
        openurl["rft.genre"] = metajson_type_to_openurl_journal_genre[rec_type]

        # atitle, jtitle
        if "is_part_ofs" in document and "title" in document["is_part_ofs"][0] and "title" in document:
            openurl["rft.atitle"] = document["title"]
            openurl["rft.jtitle"] = document["is_part_ofs"][0]["title"]
        elif "title" in document:
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
        openurl["rft_val_fmt"] = RFT_VAL_FMT_DISSERTATION

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
        openurl["rft_val_fmt"] = RFT_VAL_FMT_PATENT

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

    if openurl["rft_val_fmt"] in [RFT_VAL_FMT_BOOK, RFT_VAL_FMT_DISSERTATION, RFT_VAL_FMT_JOURNAL]:
        # common properties for book, dissertation and journal

        # isbn
        isbn = document.get_first_value_for_type_in_list_from_all_level("identifiers", "isbn")
        if isbn:
            openurl["rft.isbn"] = isbn

    if openurl["rft_val_fmt"] in [RFT_VAL_FMT_BOOK, RFT_VAL_FMT_JOURNAL]:
        # common properties for book and journal

        # au, aucorp
        if "creators" in document:
            for creator in document["creators"]:
                if "roles" in creator and creator["roles"] and creator["roles"][0] in creator_service.creator_citable_roles:
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

    if openurl["rft_val_fmt"] in [RFT_VAL_FMT_BOOK, RFT_VAL_FMT_DISSERTATION]:
        # common properties for book and dissertation

        # tpages
        tpages = document.get_extent_pages()
        if tpages:
            openurl["rft.tpages"] = tpages

    return openurl


def metajson_to_openurl(document):
    rec_id = document["rec_id"]
    openurl_dict = metajson_to_openurl_params(document)
    openurl_str = {}
    if openurl_dict:
        for k, v in openurl_dict.iteritems():
            openurl_str[k] = str(v)
            #openurl_str[k] = unicode(v, errors='ignore').encode('utf-8')
    if openurl_str:
        result = quoteattr(urllib.urlencode(openurl_str))
        #logging.debug("{}".format(result))
        return (rec_id, result)
    else:
        return (rec_id, None)



def metajson_to_openurlcoins(document):
    rec_id = document["rec_id"]
    result = metajson_to_openurl(document)
    if result[1]:
        return (rec_id, "<span class=\"Z3988\" title=" + result[1] + "></span>")
    else:
        return (rec_id, "")


def openurl_xmletree_to_metajson_list(openurl_response, source, rec_id_prefix, only_first_record):
    documents = []
    if openurl_response is not None:
        #logging.debug(type(openurl_response))
        #logging.debug(openurl_response)
        # results
        openurl_results = openurl_response.find(xmletree.prefixtag("ssopenurl", "results"))
        if openurl_results is not None:
            # result
            openurl_result_list = openurl_results.findall(xmletree.prefixtag("ssopenurl", "result"))
            if openurl_result_list:
                for openurl_result in openurl_result_list:
                    document = Document()
                    if source:
                        document["source"] = source
                    # citation
                    openurl_citation = openurl_result.find(xmletree.prefixtag("ssopenurl", "citation"))
                    if openurl_citation is not None:
                        # issn
                        openurl_issn = openurl_citation.find(xmletree.prefixtag("ssopenurl", "issn"))
                        if openurl_issn is not None:
                            identifier_issn = Identifier()
                            identifier_issn["id_type"] = "issn"
                            identifier_issn["value"] = openurl_issn.text
                            document.add_item_to_key(identifier_issn, "identifiers")
                        # eissn
                        openurl_eissn = openurl_citation.find(xmletree.prefixtag("ssopenurl", "eissn"))
                        if openurl_eissn is not None:
                            identifier_eissn = Identifier()
                            identifier_eissn["id_type"] = "eissn"
                            identifier_eissn["value"] = openurl_eissn.text
                            document.add_item_to_key(identifier_eissn, "identifiers")
                    # linkGroups
                    openurl_linkgroups = openurl_result.find(xmletree.prefixtag("ssopenurl", "linkGroups"))
                    if openurl_linkgroups is not None:
                        # linkGroup
                        openurl_linkgroup_list = openurl_linkgroups.findall(xmletree.prefixtag("ssopenurl", "linkGroup"))
                        if openurl_linkgroup_list is not None:
                            for openurl_linkgroup in openurl_linkgroup_list:
                                service_name = None
                                institution_name = None
                                period_begin = None
                                period_end = None
                                url = None
                                # holdingData
                                openurl_holdingdata = openurl_linkgroup.find(xmletree.prefixtag("ssopenurl", "holdingData"))
                                if openurl_holdingdata is not None:
                                    # institution_name
                                    openurl_providername = openurl_holdingdata.find(xmletree.prefixtag("ssopenurl", "providerName"))
                                    if openurl_providername is not None:
                                        institution_name = openurl_providername.text
                                    # service_name
                                    openurl_databasename = openurl_holdingdata.find(xmletree.prefixtag("ssopenurl", "databaseName"))
                                    if openurl_databasename is not None:
                                        service_name = openurl_databasename.text
                                    # normalizedData
                                    openurl_normalizeddata = openurl_holdingdata.find(xmletree.prefixtag("ssopenurl", "normalizedData"))
                                    if openurl_normalizeddata is not None:
                                        # startDate
                                        openurl_startdate = openurl_normalizeddata.find(xmletree.prefixtag("ssopenurl", "startDate"))
                                        if openurl_startdate is not None:
                                            period_begin = openurl_startdate.text
                                        # endDate
                                        openurl_enddate = openurl_normalizeddata.find(xmletree.prefixtag("ssopenurl", "endDate"))
                                        if openurl_enddate is not None:
                                            period_end = openurl_enddate.text
                                # url
                                openurl_url_list = openurl_linkgroup.findall(xmletree.prefixtag("ssopenurl", "url"))
                                if openurl_url_list is not None:
                                    for openurl_url in openurl_url_list:
                                        if openurl_url.get("type") == "journal":
                                            url = openurl_url.text
                                        elif openurl_url.get("type") == "source":
                                            url = openurl_url.text
                                if url:
                                    resource = Resource()
                                    resource["rec_type"] = "ResourceRemote"
                                    resource["rec_state"] = "published"
                                    resource["relation_type"] = "eResource"
                                    resource["version_type"] = "publishedVersion"
                                    resource["access_rights"] = "closedAccess"
                                    resource["format_mimetype"] = "text/html"
                                    resource["url"] = url
                                    if service_name:
                                        resource["service_name"] = service_name
                                    if institution_name:
                                        resource["institution_name"] = institution_name
                                    if period_begin:
                                        resource["period_begin"] = period_begin
                                    if period_end:
                                        resource["period_end"] = period_end
                                    document.add_item_to_key(resource, "resources")
                    documents.append(document)
                    if only_first_record:
                        break
    #logging.debug(jsonbson.dumps_json(documents))
    return documents


