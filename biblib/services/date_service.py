#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging

from datetime import date
from datetime import datetime
from dateutil import parser

month_text_to_month_decimal = {
    # English 3 characters
    'jan': '01',
    'feb': '02',
    'mar': '03',
    'apr': '04',
    'may': '05',
    'jun': '06',
    'jul': '07',
    'aug': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'dec': '12',
    # English 4 characters
    'jan.': '01',
    'feb.': '02',
    'mar.': '03',
    'apr.': '04',
    'may': '05',
    'june': '06',
    'july': '07',
    'aug.': '08',
    'sep.': '09',
    'oct.': '10',
    'nov.': '11',
    'dec.': '12',
    # English
    'january': '01',
    'february': '02',
    'march': '03',
    'april': '04',
    'may': '05',
    'june': '06',
    'july': '07',
    'august': '08',
    'september': '09',
    'october': '10',
    'november': '11',
    'december': '12',
    # French
    'janvier': '01',
    'février': '02',
    'mars': '03',
    'avril': '04',
    'mai': '05',
    'juin': '06',
    'juillet': '07',
    'août': '08',
    'septembre': '09',
    'octobre': '10',
    'novembre': '11',
    'décembre': '12'
}

month_decimal_to_month_mla = {
    '01': 'jan.',
    '02': 'feb.',
    '03': 'mar.',
    '04': 'apr.',
    '05': 'may',
    '06': 'june',
    '07': 'july',
    '08': 'aug.',
    '09': 'sep.',
    '10': 'oct.',
    '11': 'nov.',
    '12': 'dec.'
}


def parse_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp))


def format_date(date_iso):
    #logging.debug("format_date input: {}".format(date_iso))
    result = ""
    if date_iso:
        if date_iso == "?":
            # ? -> "n.d." means "no date" available (example aime : 590)
            result = "n.d."
        elif date_iso.endswith("?"):
            # YYYY? -> "[c. 1997]" means "circa 1997." (example aime : 636)
            result = "[c. {}]".format(date_iso.replace("?", ""))
        else:
            # "YYYY-MM" or "YYYY-MM-DD" ?
            date_part = date_iso.split("-")
            if len(date_part) > 1:
                if len(date_part) == 2:
                    # "YYYY-MM"
                    if date_part[1] in month_decimal_to_month_mla:
                        result = month_decimal_to_month_mla[date_part[1]] + " "
                    result += date_part[0]
                if len(date_part) == 3:
                    # "YYYY-MM-DD" (example aime : 615)
                    result = str(int(date_part[2])) + " "
                    if date_part[1] in month_decimal_to_month_mla:
                        result += month_decimal_to_month_mla[date_part[1]] + " "
                    result += date_part[0]

            else:
                # "YYYY/YYYY" (example aime : 686)
                # Do nothing
                result = date_iso

    #logging.debug("format_date output: {}".format(result))
    return result


def parse_date(datestr):
    """ Parse date and return datetime """
    #logging.debug("parse_date input: {}".format(datestr))

    # Empty
    if not datestr:
        datestr = "1970-01-01"

    # YYYY? -> YYYY
    # ? -> default: 1970-01-01
    if datestr.endswith("?"):
        datestr = datestr.replace("?", "")
        if datestr == "?":
            datestr = "1970-01-01"

    # YYYY/YYYY -> YYYY
    datestr_part = datestr.split("/")
    if datestr_part > 1:
        datestr = datestr_part[0]

    # YYxx -> YY00
    datestr = datestr.replace("x", "0")

    # YYYY -> YYYY-01-01
    if len(datestr) == 4:
        datestr += "-01-01"

    # YYYYMM -> YYYYMM01
    if len(datestr) == 6:
        datestr += "01"

    # YYYY-MM -> YYYY-MM-01
    if len(datestr) == 7:
        datestr += "-01"

    # YYYY-MM-DD
    try:
        result = parser.parse(datestr)
    except:
        result = parser.parse("1970-01-01")

    #logging.debug("parse_date output isoformat: {}".format(result))
    return result


def format_iso8601(datepy):
    result = []
    result.append(str(datepy.year))
    if datepy.month:
        result.append("-")
        month = str(datepy.month)
        if len(month) == 1:
            result.append("0")
        result.append(month)
        if datepy.day:
            result.append("-")
            day = str(datepy.day)
            if len(day) == 1:
                result.append("0")
            result.append(day)
    return "".join(result)


def parse_to_iso8601(datestr):
    #logging.debug("parse_to_iso8601 input: {}".format(datestr))
    try:
        return format_iso8601(parser.parse(datestr))
    except:
        logging.error("parse_to_iso8601 error with input {}:".format(datestr), exc_info=True)
