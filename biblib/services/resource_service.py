#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import os
import re
import commands
import subprocess
import httplib
import urllib2
import cookielib

from biblib.services import creator_service


file_type_to_file_extension = {
    "pdf": "pdf"
}


def convert_rtf_to_txt(input_path, output_path, input_filename, output_filename):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    command = "textutil -convert txt "
    command += "'" + input_path + "/" + input_filename + "'"
    command += " -output "
    command += "'" + output_path + "/" + output_filename + "'"
    result = commands.getstatusoutput(command)
    if result[0] != 0:
        logging.debug(output_filename)
        logging.debug(result)
    return result


def convert_pdf_to_txt(pdf):
    """Convert a pdf file to txet and return the text.

    This method requires pdftotext to be installed.
    """
    stdout = subprocess.Popen(["pdftotext", "-q", pdf, "-"], stdout=subprocess.PIPE).communicate()[0]
    return stdout


def extract_title_from_txt(txt):
    # remove all non alphanumeric characters
    txt = re.sub("\W", " ", txt)
    words = txt.strip().split()[:20]
    return " ".join(words)


def format_filename(matajson, file_extension):
    date_issued = None
    first_contrib = None
    title = None
    if "date_issued" in matajson and matajson["date_issued"]:
        # todo get year
        date_issued = matajson["date_issued"]
    else:
        date_issued = ""
    if "creators" in matajson and matajson["creators"]:
        first_contrib = creator_service.formatted_name(matajson["creators"][0])
    else:
        first_contrib = ""

    if "title" in matajson:
        title = matajson["title"]
    else:
        title = ""
    result = []
    for i in date_issued, first_contrib, title:
        if i:
            result.append(i)
    return ".".join("-".join(result), file_extension)


def rename_file(file_path, matajson):
    old_filename = os.path.basename(file_path)
    file_extension = get_file_extension_form_file_name(old_filename)
    new_filename = format_filename(matajson, file_extension)
    new_file_path = file_path.replace(old_filename, new_filename)
    os.rename(file_path, new_file_path)


def get_file_extension_form_file_type(file_type):
    if file_type and file_type in file_type_to_file_extension:
        return file_type_to_file_extension[file_type]
    return None


def get_file_extension_form_file_name(file_name):
    if file_name:
        dot_index = file_name.find(".")
        if dot_index != -1:
            return file_name[dot_index + 1:]
    return None


def fetch_url(url):
    url = url.strip()
    # cookies management
    cookie_jar = cookielib.CookieJar()
    url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))

    # User-Agent
    request_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.28.10 (KHTML, like Gecko) Version/6.0.3 Safari/536.28.10"}

    request = urllib2.Request(url, None, headers=request_headers)

    result_error = True
    result_code = None
    result_redirect = False
    result_redirect_url = None
    result_info = None
    result_data = None

    try:
        response = url_opener.open(request)

    except IOError, e:
        result_error = True
        result_code = "IOError:"
        if hasattr(e, 'code'):
            result_code += " " + str(e.code)
        if hasattr(e, 'reason'):
            result_code += " " + str(e.reason)

    except ValueError, e:
        result_error = True
        result_code = "ValueError: " + str(e)

    except httplib.BadStatusLine, e:
        result_error = True
        result_code = "httplib.BadStatusLine: " + str(e)

    else:
        result_error = False
        result_code = str(response.code)

        info_str = str(response.info())
        result_info = {}
        for line in info_str.split("\n"):
            index_sep = line.find(":")
            if index_sep != -1:
                result_info[line[:index_sep].strip()] = line[index_sep + 1:].strip()

        if url != response.geturl():
            result_redirect = True
            result_redirect_url = response.geturl()
        #result_data = response.read()

    finally:
        result_dict = {}
        result_dict["error"] = result_error
        result_code = result_code.replace("''", "")
        if not result_code:
            result_code = "?"
        result_dict["code"] = result_code
        result_dict["redirect"] = result_redirect
        if result_redirect_url:
            result_dict["redirect_url"] = result_redirect_url
        if result_info:
            result_dict["info"] = result_info

        logging.debug("{0}\t\t: {1}".format(result_code, url))
        #return result_dict, result_data
        return result_dict, result_data


#logging.debug(fetch_url("URL"))
#logging.debug(fetch_url("http://bibliotheque.sciences-po.fr/"))
#logging.debug(fetch_url("http://intranet.tdmu.edu.ua/data/kafedra/internal/ginecology2/classes_stud/en/med/lik/ptn/Obstetrics and gynecology/5 year/05_Operative obstetric. Lacerations of the birth canal.files/image008.jpg"))
#logging.debug(fetch_url("http://commons.wikimedia.org/wiki/File:Saint-Menoux_debredinoire.JPG?uselang=fr"))
#logging.debug(fetch_url("http://france.meteofrance.com/france/actu/archives/2009/2009?page_id=10320&document_id=21075&portlet_id=42233"))
