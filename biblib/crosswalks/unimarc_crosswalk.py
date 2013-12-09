#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import re

from biblib.metajson import Creator
from biblib.metajson import Document
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Subject
from biblib.services import creator_service
from biblib.services import date_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import console
from biblib.util import constants
from biblib.util import jsonbson

from pymarc import MARCReader

isbn_regex = re.compile(r'([0-9\-xX]+)')

target_audience_unimarc_to_marc21 = {
    'a': "juvenile",  # a=jeunesse (général)
    'b': "preschool",  # b=pré-scolaire, 0-5 ans
    'c': "juvenile",  # c=scolaire, 5-10 ans
    'd': "juvenile",  # d=enfant, 9-14 ans
    'e': "adolescent",  # e=jeune adulte, 14-20 ans
    'k': "specialized",  # k=adulte, haut niveau
    'm': "adult"  # m=adulte, grand public
    # u=inconnu
}

def unimarc_file_path_to_metasjon_list(unimarc_file_path, source, only_first_record):
    with open(unimarc_file_path) as unimarc_file:
        return unimarc_file_to_metasjon_list(unimarc_file, source, only_first_record)


def unimarc_file_to_metasjon_list(unimarc_file, source, only_first_record):
    print unimarc_file
    marc_reader = MARCReader(unimarc_file, False, False)
    return unimarc_marcreader_to_metasjon_list(marc_reader, source, only_first_record)


def unimarc_marcreader_to_metasjon_list(marc_reader, source, only_first_record):
    print "unimarc_marcreader_to_metasjon_list"
    count = 0
    for record in marc_reader:
        count += 1
        yield unimarc_record_to_metajson(record, source)
    print count


def unimarc_record_to_metajson(record, source):
    print "unimarc_record_to_metajson"
    document = Document()

    #record_dict = record.as_dict()
    #print jsonbson.dumps_json(record_dict, True)

    # 002, 991$e, 995$f -> rec_id
    rec_id = ""
    if record['002'] is not None:
        rec_id_prefix = "sciencespo_catalog_"
        rec_id = rec_id_prefix + record['002'].data
    if record['991'] is not None and record['991']['e'] is not None:
        rec_id += "_" + record['991']['e']
    # todo numer holding identifier
    if rec_id:
        print "rec_id: {}".format(rec_id)
        document["rec_id"] = rec_id

    # leader -> rec_type
    rec_type = extract_unimarc_type(record)
    document["rec_type"] = rec_type

    # 0XX, 945 -> identifiers
    identifiers = []
    if record['001'] is not None and record['001'].data is not None:
        # 001 -> identifier ppn
        identifiers.append({"id_type": "ppn", "value": record['001'].data})
    if record['010'] is not None and record['010']['a'] is not None:
        # 010 -> identifier isbn
        identifiers.append({"id_type": "isbn", "value": record['010']['a']})
    if record['011'] is not None and record['011']['a'] is not None:
        # 011 -> identifier issn
        identifiers.append({"id_type": "issn", "value": record['011']['a']})
    if record['013'] is not None and record['013']['a'] is not None:
        # 013 -> identifier ismn
        identifiers.append({"id_type": "ismn", "value": record['013']['a']})
    if record['014'] is not None and record['014']['a'] is not None and record['014']['2'] is not None:
        # 014 -> identifier $2
        identifiers.append({"id_type": record['014']['2'], "value": record['014']['a']})
    if record['015'] is not None and record['015']['a'] is not None:
        # 015 -> identifier isrn
        identifiers.append({"id_type": "isrc", "value": record['015']['a']})
    if record['016'] is not None and record['016']['a'] is not None:
        # 016 -> identifier isrc
        identifiers.append({"id_type": "isrc", "value": record['016']['a']})
    #if record['020'] is not None and record['020']['b'] is not None:
        # 020 -> identifier lccn
    #    identifiers.append({"id_type": "lccn", "value": record['020']['b']})
    if record['040'] is not None and record['040']['a'] is not None:
        # 040 -> identifier coden
        identifiers.append({"id_type": "coden", "value": record['040']['a']})
    if record['073'] is not None and record['073']['a'] is not None:
        # 073 -> identifier ean
        identifiers.append({"id_type": "ean", "value": record['073']['a']})
    if record['945'] is not None and record['945']['b'] is not None:
        # 945 -> identifier callnumber
        identifiers.append({"id_type": "callnumber", "value": record['945']['b']})
    if identifiers:
        document["identifiers"] = identifiers

    # 100$a/0-7 -> rec_created_date
    if record['100'] is not None and record['100']['a'] is not None:
        rec_created_date = record['100']['a'][0:8]
        if rec_created_date.strip():
            document["rec_created_date"] = date_service.parse_to_iso8601(rec_created_date.strip())

    # 100$a/8 -> date stuff
    if record['100'] is not None and record['100']['a'] is not None:
        date_type = record['100']['a'][8:9]
        # a= ressource continue en cours
        #    1:date_issued 2:None
        # b= ressource continue morte
        #    1:date_issued 2:date_issued_end
        # c= ressource continue dont la situation est inconnue
        #    1:date_issued 2:None
        # d= monographie complète à la publication ou publiée dans une année civile
        #    1:date_issued 2:None
        # e= reproduction
        #    1:date_issued 2:date_issued_origin
        # f= monographie dont la date de publication est incertaine
        #    1:date_issued 2:date_issued_end
        # g= monographie dont la publication s’étend sur plus d’une année
        #    1:date_issued 2:date_issued_end
        # h= monographie ayant à la fois une date de publication et une date de copyright ou de privilège
        #    1:date_issued 2:rights.date_copyright
        # i= monographie ayant à la fois une date d’édition ou de diffusion et une date de production
        #    1:date_issued 2:date_production
        # j= monographie ayant une date de publication précise
        #    1:date_issued 2:date_issued MMJJ
        # k= monographie ayant à la fois une date de publication et une date d’impression
        #    1:date_issued 2:date_printed
        # u= date(s) de publication inconnue(s)
        #    1:None 2:None

        # 100$a/9-12 -> date_issued
        date_issued = record['100']['a'][9:13]
        if date_issued.strip():
            document["date_issued"] = date_issued.strip()

        # 100$a/13-16 -> date_issued_end, date_issued_origin, date_copyright, date_production, date_printed
        date_issued_end = record['100']['a'][13:17]
        if date_issued_end.strip() and date_issued_end.strip() != "9999":
            if date_type in ['b','f','g']:
                document["date_issued_end"] = date_issued_end.strip()
            elif date_type == 'e':
                document["date_issued_origin"] = date_issued_end.strip()
            elif date_type == 'h':
                # todo rights
                document["date_copyright"] = date_issued_end.strip()
            elif date_type == 'i':
                document["date_production"] = date_issued_end.strip()
            elif date_type == 'k':
                document["date_printed"] = date_issued_end.strip()

        # 100$a/17-20 -> target_audiences
        targets = record['100']['a'][17:20]
        if targets.strip():
            target_audiences = []
            for target in targets:
                if target in target_audience_unimarc_to_marc21:
                    target_audiences.append(target_audience_unimarc_to_marc21[target])
            if target_audiences:
                document["target_audiences"] = target_audiences

        # 100$a/22-24 -> rec_cataloging_languages
        rec_cataloging_languages = record['100']['a'][22:25]
        # 100$a/25 -> rec_cataloging_transliteration
        rec_cataloging_transliteration = record['100']['a'][25:26]
        # 100$a/26-29 -> rec_cataloging_charactersets
        rec_cataloging_charactersets = record['100']['a'][26:30]

    # 101$a -> languages
    if record.get_fields('101'):
        languages = []
        for field in record.get_fields('101'):
            for lang_iso639_2b in field.get_subfields('a'):
                lang_rfc5646 = language_service.convert_iso639_2b_to_rfc5646(lang_iso639_2b)
                if lang_rfc5646:
                    languages.append(lang_rfc5646)
        if languages:
            document["languages"] = languages

    # 102$a -> publication_countries
    publication_countries = []
    if record.get_fields('102'):
        for field in record.get_fields('102'):
            for subfield in field.get_subfields('a'):
                publication_countries.append(subfield)
        if publication_countries:
            document["publication_countries"] = publication_countries

    # 200 -> title
    if record['200'] is not None:
        if record['200']['a'] is not None:
            title_non_sort_pos = int(record['200'].indicator2)
            if title_non_sort_pos != 0:
                document["title_non_sort"] = record['200']['a'][:title_non_sort_pos]
                document["title"] = record['200']['a'][title_non_sort_pos:]
            else:
                document["title"] = record['200']['a']
            #print "title: {}".format(document["title"])
        if record['200']['d'] is not None:
            document["title_alternative"] = {"title": record['200']['d']}
        if record['200']['e'] is not None:
            document["title_sub"] = record['200']['e']
        if record['200']['h'] is not None:
            document["part_number"] = record['200']['h']
        if record['200']['i'] is not None:
            document["part_name"] = record['200']['i']

    # 210$a, 210$c -> publication_places, publishers
    publication_places = []
    publishers = []
    for field210 in record.get_fields('210'):
        for field210a in field210.get_subfields('a'):
            if field210a is not None and field210a not in publication_places:
                publication_places.append(field210a)
        for field210c in field210.get_subfields('c'):
            if field210c is not None and field210c not in publishers:
                publishers.append(field210c)
    if publication_places:
        document["publication_places"] = publication_places
    if publishers:
        document["publishers"] = publishers

    # 6XX -> subject
    subjects = []
    if record.get_fields('600', '601', '602'):
        for field in record.get_fields('600', '601', '602'):
            creator = extract_unimarc_creator(field)
            if creator and "agent" in creator:
                subject = {"agents": [creator["agent"]]}
                suject_agents.append(subject)

    if record.get_fields('607'):
        subjects = []
        for field in record.get_fields('607'):
            subject = {}
            # todo

    # 676$a -> classifications ddc
    if record.get_fields('676'):
        deweys = []
        for field in record.get_fields('676'):
            deweys.extend(field.get_subfields('a'))
        if deweys:
            if "classifications" not in document:
                document["classifications"] ={}
            document["classifications"]["ddc"] = deweys

    # 7XX -> creators
    creators = []
    fields_creators = record.get_fields("700", "701", "702", "710", "711", "712", "716", "720", "721", "722", "730")
    if fields_creators:
        for field in fields_creators:
            creator = extract_unimarc_creator(field)
            if creator:
                creators.append(creator)
    if creators:
        document["creators"] = creators

    # holdings / copies
    print record['995']

    debug = True
    if debug:
        metajson_service.pretty_print_document(document)
    return document


def extract_unimarc_type(record):
    rec_type = None

    # leader
    leader6 = record.leader[6]
    leader7 = record.leader[7]

    # 100$a/17-19
    # 100$a/20
    field100ap1719 = None
    field100ap20 = None
    if record['100'] is not None and record['100']['a'] is not None:
        field100ap1719 = record['100']['a'][17:20]
        field100ap20 = record['100']['a'][20:21]

    # 105/4-7
    field105ap48 = None
    if record['105'] is not None and record['105']['a'] is not None:
        field105ap48 = record['105']['a'][4:8]

    # 106$a
    field106a = None
    if record['106'] is not None and record['106']['a'] is not None:
        field106a = record['106']['a']

    # 110$a/1
    field110ap1 = None
    if record['110'] is not None and record['110']['a'] is not None:
        field110ap1 = record['110']['a'][1:2]

    # 115$a/0
    field115ap0 = None
    if record['115'] is not None and record['115']['a'] is not None:
        field115ap0 = record['115']['a'][0:1]

    # 116/0
    field116ap0 = None
    if record['116'] is not None and record['116']['a'] is not None:
        field116ap0 = record['116']['a'][0:1]

    # 121$a/0
    field121ap0 = None
    if record['121'] is not None and record['121']['a'] is not None:
        field121ap0 = record['121']['a'][0:1]

    # 124$b
    field124b = None
    if record['124'] is not None and record['124']['b'] is not None:
        field124b = record['124']['b']

    # 126$a/0
    field126ap0 = None
    if record['126'] is not None and record['126']['a'] is not None:
        field126ap0 = record['126']['a'][0:1]

    # 135/0
    field135ap0 = None
    if record['135'] is not None and record['135']['a'] is not None:
        field135ap0 = record['135']['a'][0:1]

    debug = True
    if debug:
        print "leader6: {}".format(leader6)
        print "leader7: {}".format(leader7)
        print "100$a/17-19: {}".format(field100ap1719)
        print "100$a/20: {}".format(field100ap20)
        print "105/4-7: {}".format(field105ap48)
        print "106$a: {}".format(field106a)
        print "110$a/1: {}".format(field110ap1)
        print "115$a/0: {}".format(field115ap0)
        print "116/0: {}".format(field116ap0)
        print "121$a/0: {}".format(field121ap0)
        print "124$b: {}".format(field124b)
        print "126$a/0: {}".format(field126ap0)
        print "135/0: {}".format(field135ap0)

    if leader6 == "a":
        if leader7 == "a":
            rec_type = constants.DOC_TYPE_JOURNALARTICLE
        elif leader7 == "c":
            rec_type = "PressClipping"
        elif leader7 == "m":
            rec_type = constants.DOC_TYPE_BOOK
        elif leader7 == "s":
            rec_type = constants.DOC_TYPE_JOURNAL
    elif leader6 == "b":
        rec_type = constants.DOC_TYPE_MANUSCRIPT
    elif leader6 in ["c", "d"]:
        rec_type = constants.DOC_TYPE_MUSICALSCORE
    elif leader6 in ["e", "f"]:
        rec_type = constants.DOC_TYPE_MAP
    elif leader6 == "g":
        rec_type = constants.DOC_TYPE_VIDEORECORDING
    elif leader6 == "i":
        rec_type = constants.DOC_TYPE_AUDIORECORDING
    elif leader6 == "j":
        rec_type = constants.DOC_TYPE_MUSICRECORDING
    elif leader6 == "k":
        rec_type = constants.DOC_TYPE_IMAGE
    elif leader6 == "l":
        rec_type = "ElectronicResource"
    elif leader6 == "m":
        rec_type = "Kit"
    elif leader6 == "r":
        rec_type = constants.DOC_TYPE_PHYSICALOBJECT
    else:
        rec_type = constants.DOC_TYPE_DOCUMENT

    return rec_type


def extract_unimarc_creator(field):
    if field:
        creator = Creator()
        # $4 -> role
        if field['4']:
            print "field['4']"
            print field['4']
            if field['4'] in creator_service.role_unimarc_to_role_code:
                creator["role"] = creator_service.role_unimarc_to_role_code[field['4']]
            else:
                creator["role"] = "ctb"

        # 600, 700, 701, 702 -> Person
        if field.tag in ["700", "701", "702"]:
            # Person
            person = Person()
            if field.subfields:
                if field.get_subfields('a'):
                    # name_family
                    person["name_family"] = "".join(field.get_subfields('a'))
                if field.get_subfields('b'):
                    # name_given
                    person["name_given"] = "".join(field.get_subfields('b'))
                if field.get_subfields('f'):
                    dates = format_dates_as_list(field.get_subfields('f'))
                    if dates:
                        person["date_birth"] = dates[0]
                        if len(dates) > 1:
                            person["date_death"] = dates[1]
                if person:
                    creator["agent"] = person

        # 601, 710, 711, 712 -> Orgunit, Event
        elif field.tag in ["710", "711", "712"]:
            if field.subfields:
                if field.indicator1 == "1":
                    # Event
                    event = Event()
                    if field.get_subfields('a'):
                        event["title"] = "".join(field.get_subfields('a'))
                    if field.get_subfields('d'):
                        event["number"] = "".join(field.get_subfields('d'))
                    if field.get_subfields('e'):
                        event["place"] = "".join(field.get_subfields('e'))
                    if field.get_subfields('f'):
                        event["date_begin"] = "".join(field.get_subfields('f'))
                    if event:
                        creator["agent"] = event
                else:
                    # Orgunit
                    orgunit = Orgunit()
                    name = []
                    if field.get_subfields('a'):
                        name.extend(field.get_subfields('a'))
                    if field.get_subfields('b'):
                        name.append(". ")
                        name.extend(field.get_subfields('b'))
                    if name:
                        orgunit["name"] = "".join(name)
                    dates = format_dates_as_list(field.get_subfields('c'))
                    if dates:
                        orgunit["date_foundation"] = dates[0]
                        if len(dates) > 1:
                            orgunit["date_dissolution"] = dates[1]
                    if orgunit:
                        creator["agent"] = orgunit

        elif field.tag in ["716"]:
            # Nom de marque
            print "WARNING: todo"

        elif field.tag in ["602", "720", "721", "722"]:
            if field.subfields:
                # Family
                family = Family()
                if field.get_subfields('a'):
                    # name_family
                    family["name_family"] = "".join(field.get_subfields('a'))
                if field.get_subfields('f'):
                    dates = format_dates_as_list(field.get_subfields('f'))
                    if dates:
                        family["date_birth"] = dates[0]
                        if len(dates) > 1:
                            family["date_death"] = dates[1]
                if family:
                    creator["agent"] = family

        elif field.tag == "730":
            # Intellectual responsability
            print "WARNING: todo"

        if creator:
            return creator


def format_dates_as_list(dates):
    if dates:
        # (1811-1882)
        # todo : pb with 710$c that can be another think than a date..
        return dates[0].replace("(","").replace(")","").replace("-....","").split("-")
