#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.citations import citations_manager
from biblib.services import crosswalks_service
from biblib.services import metajson_service
from biblib.services import repository_service
from biblib.util import constants
from biblib.util import jsonbson


def export_corpus(corpus, output_file_path, output_format, error_file):
    if corpus and output_file_path:
        # fetch
        metajson_list = repository_service.get_documents(corpus)
        print len(metajson_list)
        # convert
        results = crosswalks_service.convert_metajson_list(metajson_list, output_format)
        # export
        export(corpus, corpus, results, output_file_path, output_format, error_file)


def export(col_id, col_title, items, output_file_path, output_format, error_file):
    output_type = crosswalks_service.guess_format_type(output_format)
    if output_type is not None:
        if output_type == constants.FILE_TYPE_JSON:
            return export_metajson_collection(col_id, col_title, items, output_file_path)
        elif output_type == constants.FILE_TYPE_TXT:
            return export_txt(items, output_file_path)
        elif output_type == constants.FILE_TYPE_XMLETREE:
            return export_xml(items, output_file_path)
        elif output_type == constants.FILE_TYPE_HTML:
            return export_html(col_id, col_title, items, output_file_path)


def export_metajson_collection(col_id, col_title, metajson_list, output_file_path):
    if metajson_list:
        with open(output_file_path, "w") as output_file:
            collection = metajson_service.create_collection(col_id, col_title, metajson_list)
            dump = jsonbson.dumps_bson(collection, True)
            output_file.write(dump)
            return dump


def export_txt(txt_list, output_file_path):
    if txt_list:
        with open(output_file_path, "w") as output_file:
            for txt in txt_list:
                if txt:
                    output_file.write(txt)


def export_xml(xml_list, output_file_path):
    # todo
    return None


def export_bibtex():
    # todo
    return None


def export_html(col_id, col_title, metajson_list, output_file_path, style="mla"):
    with open(output_file_path, "w") as output_file:
        header = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n"
        header += "<head>\n"
        header += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>"
        if col_title:
            header += "<title>" + col_title + "</title>\n"
        else:
            header += "<title>BibLib HTML export</title>\n"
        header += "</head>\n"
        header += "<body>\n"
        output_file.write(header)

        for document in metajson_list:
            source_info = ""
            if "rec_source" in document and document["rec_source"]:
                source_info += document["rec_source"] + ":"
            if "rec_id" in document and document["rec_id"]:
                source_info += document["rec_id"] + ":"
            citation = citations_manager.cite(document, style, "html")

            debug = True
            if debug:
                meta = jsonbson.dumps_bson(document, True)
                output_file.write("<pre>" + meta + "</pre>\n")

                output_file.write("<xmp>" + citation + "</xmp>\n")

            output_file.write("<div>" + citation + "</div>\n")

        footer = "</body>\n"
        footer += "</html>"
        output_file.write(footer)
