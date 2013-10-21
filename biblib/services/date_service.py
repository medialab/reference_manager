#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from datetime import date
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


def format_date(date_iso):
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

    return result


def parse_date(date_iso):
    #print date_iso

    # Empty
    if not date_iso:
        date_iso = "1970-01-01"

    # YYYY? -> YYYY
    # ? -> default: 1970-01-01
    if date_iso.endswith("?"):
        date_iso = date_iso.replace("?", "")
        if date_iso == "?":
            date_iso = "1970-01-01"

    # YYYY/YYYY -> YYYY
    date_iso_part = date_iso.split("/")
    if date_iso_part > 1:
        date_iso = date_iso_part[0]

    # YYxx -> YY00
    date_iso = date_iso.replace("x", "0")

    # YYYY -> YYYY-01-01
    if len(date_iso) == 4:
        date_iso += "-01-01"

    # YYYYMM -> YYYYMM01
    if len(date_iso) == 6:
        date_iso += "01"

    # YYYY-MM -> YYYY-MM-01
    if len(date_iso) == 7:
        date_iso += "-01"

    # YYYY-MM-DD
    try:
        result = parser.parse(date_iso)
    except:
        result = parser.parse("1970-01-01")

    #print result
    return result

