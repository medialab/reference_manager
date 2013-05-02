#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import re
import commands
import subprocess
import urllib2
import cookielib


def convert_rtf_to_txt(input_path, output_path, input_filename, output_filename):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    command = "textutil -convert txt "
    command += "'" + input_path + "/" + input_filename + "'"
    command += " -output "
    command += "'" + output_path + "/" + output_filename + "'"
    result = commands.getstatusoutput(command)
    if result[0] != 0:
        print output_filename
        print result
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


def format_filename(matajson):
    date_issued = None
    first_contrib = None
    title = None
    if "date_issued" in matajson:
        date_issued = matajson["date_issued"]
        # get year
    first_contrib = ""

    if "title" in matajson:
        title = matajson["title"]
    l = []
    for i in date_issued, first_contrib, title:
        if i:
            l.append(i)
    return "-".join(l) + ".pdf"


def rename_file(file_path, matajson):
    filename = format_filename(matajson)
    new_file_path = file_path.replace(os.path.basename(file_path), filename)
    os.rename(file_path, new_file_path)


def verify_url(url):
    # cookies management
    cookie_jar = cookielib.CookieJar()
    url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))

    # User-Agent
    request_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.28.10 (KHTML, like Gecko) Version/6.0.3 Safari/536.28.10"}

    request = urllib2.Request(url, None, headers=request_headers)
    try:
        response = url_opener.open(request)
    except IOError, e:
        result = {"error": True}
        if hasattr(e, 'reason'):
            result["code"] = e.reason
        elif hasattr(e, 'code'):
            result["code"] = e.code
        return result
    except ValueError, e:
        return {"error": True, "code": str(e)}
    else:
        info_str = str(response.info())
        info_dict = {}
        for line in info_str.split("\n"):
            index_sep = line.find(":")
            if index_sep != -1:
                info_dict[line[:index_sep].strip()] = line[index_sep + 1:].strip()
        result = {"error": False, "code": response.code, "info": info_dict}
        if url != response.geturl():
            result["redirect"] = True
            result["redirect_url"] = response.geturl()
        #print response.read()
        return result


#print verify_url("http://bibliotheque.sciences-po.fr/")
#print verify_url("URL")
#print verify_url("http://commons.wikimedia.org/wiki/File:Saint-Menoux_debredinoire.JPG?uselang=fr")
#print verify_url("http://france.meteofrance.com/france/actu/archives/2009/2009?page_id=10320&document_id=21075&portlet_id=42233")
