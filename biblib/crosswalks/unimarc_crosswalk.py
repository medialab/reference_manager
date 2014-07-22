#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging
import os
import re

from pymarc import MARCReader
from pymarc import record_to_xml
import smc.bibencodings

from biblib.metajson import Creator
from biblib.metajson import Document
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Resource
from biblib.metajson import Subject
from biblib.services import creator_service
from biblib.services import date_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import console
from biblib.util import constants
from biblib.util import jsonbson

isbn_regex = re.compile(r'([0-9\-xX]+)')

charsets_dict = {
    "01": "ISO 646, version IRV (caractères latins de base)",
    "02": "Registre ISO #37 (caractères cyrilliques de base)",
    "03": "ISO 5426 (caractères latins - jeu étendu)",
    "04": "ISO 5427 (caractères cyrilliques - jeu étendu)",
    "05": "ISO 5428 (caractères grecs)",
    "06": "ISO 6438 (caractères africains codés)",
    "07": "ISO 10586 (caractères géorgiens)",
    "08": "ISO 8957 (caractères hébreux) Table 1",
    "09": "ISO 8957 (caractères hébreux) Table 2",
    "10": "[Réservé]",
    "11": "ISO 5426-2 (caractères latins utilisés dans les langues européennes minoritaires et dans une typographie obsolète)",
    "50": "ISO 10646 Niveau 3 (Unicode, UTF-8)",
}

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

transliterations_dict = {
    "a": "iso",  # norme ISO de translittération
    "b": "other",  # autre règle
    "c": "iso_and_others",  # translittérations multiples : ISO ou autres règles
    "y": "no_transliteration"  # pas de translittération
}

def unimarc_file_path_to_metasjon_list(unimarc_file_path, source, rec_id_prefix, only_first_record):
    #logging.debug("unimarc_file_path_to_metasjon_list")
    with open(unimarc_file_path) as unimarc_file:
        return unimarc_file_to_metasjon_list(unimarc_file, source, rec_id_prefix, only_first_record)


def unimarc_file_to_metasjon_list(unimarc_file, source, rec_id_prefix, only_first_record):
    #logging.debug("unimarc_file_to_metasjon_list")
    marc_reader = MARCReader(unimarc_file, to_unicode=False, force_utf8=False)
    return unimarc_marcreader_to_metasjon_list(marc_reader, source, rec_id_prefix, only_first_record)


def unimarc_marcreader_to_metasjon_list(marc_reader, source, rec_id_prefix, only_first_record):
    #logging.debug("unimarc_marcreader_to_metasjon_list")
    count = 0
    for record in marc_reader:
        count += 1
        yield unimarc_record_to_metajson(record, source, rec_id_prefix)


def unimarc_record_to_metajson(record, source, rec_id_prefix):
    #logging.debug("unimarc_record_to_metajson")
    document = Document()

    #logging.debug(record)
    #logging.debug(jsonbson.dumps_json(record.as_dict(), pretty=True))

    if source:
        document["rec_source"] = source

    # 002 -> rec_id
    rec_id = ""
    if rec_id_prefix is None:
        rec_id_prefix = ""
    if record['002'] is not None:
        rec_id = rec_id_prefix + record['002'].data
    document["rec_id"] = rec_id

    # Debug
    output_dir = os.path.join("data", "result", "pdcn")
    output_file_path = os.path.join(output_dir, rec_id + ".marc.txt")
    output_filexml_path = os.path.join(output_dir, rec_id + ".marcxml.xml")
    with open(output_file_path, "w") as output_file:
        output_file.write(str(record))
    with open(output_filexml_path, "w") as output_filexml:
        output_filexml.write(record_to_xml(record))

    # leader and 1XX -> rec_type
    rec_type = extract_unimarc_type(record)
    document["rec_type"] = rec_type

    # 0XX and 945$b -> identifiers
    identifiers = extract_unimarc_identifiers(record)
    if identifiers:
        document["identifiers"] = identifiers

    # 100$a stuff
    if record['100'] is not None and record['100']['a'] is not None:
        # date stuff

        # 100$a/0-7 -> rec_created_date
        rec_created_date = record['100']['a'][0:8]
        if rec_created_date.strip():
            document["rec_created_date"] = date_service.parse_to_iso8601(rec_created_date.strip())
        # 100$a/8 -> date_type
        date_type = record['100']['a'][8:9]
        # 100$a/9-12 -> date_1
        date_1 = record['100']['a'][9:13]
        if date_1 is not None:
            date_1 = date_1.strip()
        # 100$a/13-16 -> date_2
        date_2 = record['100']['a'][13:17]
        if date_2 is not None:
            date_2 = date_2.strip()

        date_copyright = None
        date_issued = None
        date_issued_begin = None
        date_issued_end = None
        date_issued_original = None
        date_issued_uncertain = None
        date_printed = None
        date_production = None

        if date_type == 'a':
            # a : ressource continue en cours
            # 1:date_issued_begin 2:None
            date_issued_begin = date_1
        elif date_type == 'b':
            # b : ressource continue morte
            # 1:date_issued_begin 2:date_issued_end
            date_issued_begin = date_1
            date_issued_end = date_2
        elif date_type == 'c':
            # c : ressource continue dont la situation est inconnue
            # 1:date_issued_begin 2:None
            date_issued_begin = date_1
        elif date_type == 'd':
            # d : monographie complète à la publication ou publiée dans une année civile
            # 1:date_issued 2:None
            date_issued = date_1
        elif date_type == 'e':
            # e : reproduction
            # 1:date_issued 2:date_issued_original
            date_issued = date_1
            date_issued_original = date_2
        elif date_type == 'f':
            # f : monographie dont la date de publication est incertaine
            # 1:date_issued 2:date_issued_uncertain
            date_issued = date_1
            date_issued_uncertain = date_2
        elif date_type == 'g':
            # g : monographie dont la publication s’étend sur plus d’une année
            # 1:date_issued 2:date_issued_end
            date_issued = date_1
            date_issued_end = date_2
        elif date_type == 'h':
            # h : monographie ayant à la fois une date de publication et une date de copyright ou de privilège
            # 1:date_issued 2:date_copyright
            date_issued = date_1
            date_copyright = date_2
        elif date_type == 'i':
            # i : monographie ayant à la fois une date d’édition ou de diffusion et une date de production
            # 1:date_issued 2:date_production
            date_issued = date_1
            date_production = date_2
        elif date_type == 'j':
            # j : monographie ayant une date de publication précise
            # 1:date_issued 2:date_issued MMJJ
            date_2_mm = date_2[0:3]
            date_2_jj = date_2[2:5]
            if date_2_mm:
                date_1 = date_1 + "-" + date_2_mm
                if date_2_jj:
                    date_1 = date_1 + "-" + date_2_jj
            date_issued = date_1
        elif date_type == 'k':
            # k : monographie ayant à la fois une date de publication et une date d’impression
            # 1:date_issued 2:date_printed
            date_issued = date_1
            date_printed = date_2
        elif date_type == 'u':
            # u : date(s) de publication inconnue(s)
            # 1:None 2:None
            pass
        else:
            date_issued = date_1

        if date_copyright:
            document["date_copyright"] = date_copyright
        if date_issued:
            document["date_issued"] = date_issued
        if date_issued_begin:
            document["date_issued_begin"] = date_issued
        if date_issued_end:
            document["date_issued_end"] = date_issued_end
        if date_issued_original:
            document["date_issued_original"] = date_issued_original
        if date_issued_uncertain:
            document["date_issued_uncertain"] = date_issued_uncertain
        if date_printed:
            document["date_printed"] = date_printed
        if date_production:
            document["date_production"] = date_production

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
        rec_cataloging_language = record['100']['a'][22:25]
        if rec_cataloging_language:
            rec_cataloging_language_rfc5646 = language_service.convert_iso639_2b_to_rfc5646(rec_cataloging_language)
            if rec_cataloging_language_rfc5646:
                document["rec_cataloging_languages"] = [rec_cataloging_language_rfc5646]

        # 100$a/25 -> rec_cataloging_transliteration
        rec_cataloging_transliteration = record['100']['a'][25:26]
        if rec_cataloging_transliteration.strip() and rec_cataloging_transliteration.strip() != "y":
            document["rec_cataloging_transliteration"] = transliterations_dict[rec_cataloging_transliteration.strip()]

        # 100$a/26-33 -> rec_cataloging_charactersets
        rec_cataloging_charactersets = []
        tmp_charsets = []
        tmp_charsets.append(record['100']['a'][26:28].strip())
        tmp_charsets.append(record['100']['a'][28:30].strip())
        tmp_charsets.append(record['100']['a'][30:32].strip())
        tmp_charsets.append(record['100']['a'][32:34].strip())
        for charset in tmp_charsets:
            if charset:
                rec_cataloging_charactersets.append({"charset_id": charset, "label": charsets_dict[charset]})
        if rec_cataloging_charactersets:
            document["rec_cataloging_charactersets"] = rec_cataloging_charactersets

    # 101$a -> languages
    # 101$b -> languages_intermediates
    # 101$c -> languages_originals
    if record.get_fields('101'):
        languages = []
        languages_intermediates = []
        languages_originals = []
        for field in record.get_fields('101'):
            for lang_iso639_2b in field.get_subfields('a'):
                lang_rfc5646 = language_service.convert_iso639_2b_to_rfc5646(lang_iso639_2b)
                if lang_rfc5646:
                    languages.append(lang_rfc5646)
            for lang_iso639_2b in field.get_subfields('b'):
                lang_rfc5646 = language_service.convert_iso639_2b_to_rfc5646(lang_iso639_2b)
                if lang_rfc5646:
                    languages_intermediates.append(lang_rfc5646)
            for lang_iso639_2b in field.get_subfields('c'):
                lang_rfc5646 = language_service.convert_iso639_2b_to_rfc5646(lang_iso639_2b)
                if lang_rfc5646:
                    languages_originals.append(lang_rfc5646)
        if languages:
            document["languages"] = languages
        if languages_intermediates:
            document["languages_intermediates"] = languages_intermediates
        if languages_originals:
            document["languages_originals"] = languages_originals

    # 102$a -> publication_countries
    if record.get_fields('102'):
        publication_countries = []
        for field in record.get_fields('102'):
            for subfield in field.get_subfields('a'):
                publication_countries.append(subfield)
        if publication_countries:
            document["publication_countries"] = publication_countries

    # 200 -> title
    if record['200'] is not None:
        #logging.debug("record['200'] = {}".format(record['200']))
        if record['200']['a'] is not None:
            title_indicator2 = record['200'].indicator2.strip()
            if title_indicator2:
                title_non_sort_pos = int(record['200'].indicator2)
            else:
                title_non_sort_pos = 0
            if title_non_sort_pos != 0:
                document["title_non_sort"] = record['200']['a'][:title_non_sort_pos]
                document["title"] = record['200']['a'][title_non_sort_pos:]
            else:
                document["title"] = record['200']['a']
        if record['200']['d'] is not None:
            document["title_alternative"] = {"title": record['200']['d']}
        if record['200']['e'] is not None:
            document["title_sub"] = record['200']['e']
        if record['200']['h'] is not None:
            document["part_number"] = record['200']['h'].replace(",", "")
        if record['200']['i'] is not None:
            document["part_name"] = record['200']['i']

    # 205$a -> edition
    if record['205'] is not None and record['205']['a'] is not None:
        document["edition"] = record['205']['a'].strip()

    # 206 -> cartographics[i]
    if record['206'] is not None:
        cartographics = []
        for field in record.get_fields('206'):
            cartographic = {}
            if field['a'] is not None:
                # a : unstructured -> scale
                cartographic["scale"] = field['a']
            else:
                # b : scale
                scale = ""
                for subfield in field.get_subfields('b'):
                    scale = scale + " " + subfield
                if scale.strip():
                    cartographic["scale"] = scale.strip()
                # c : projection
                if field['c'] is not None:
                    cartographic["projection"] = field['c'].strip()
                # d : coordinates_unstructured
                if field['d'] is not None:
                    cartographic["coordinates_unstructured"] = field['d'].strip()
                # e : zone
                if field['e'] is not None:
                    cartographic["zone"] = field['e'].strip()
                # f : equinox
                if field['f'] is not None:
                    cartographic["equinox"] = field['f'].strip()
            if cartographic:
                cartographics.append(cartographic)
        if cartographics:
            document["cartographics"] = cartographics

    # 207$a -> holding_descriptions[i]
    if record['207'] is not None:
        holding_descriptions = []
        for field in record.get_fields('207'):
            for subfield in field.get_subfields('a'):
                if subfield.strip():
                    holding_descriptions.append(subfield.strip())
        if holding_descriptions:
            document["holding_descriptions"] = holding_descriptions

    # 210$a -> publication_places
    # 210$c -> publishers
    if record['210'] is not None:
        publication_places = []
        publishers = []
        for field in record.get_fields('210'):
            for subfield in field.get_subfields('a'):
                if subfield is not None and subfield not in publication_places:
                    publication_places.append(subfield)
            for subfield in field.get_subfields('c'):
                if subfield is not None and subfield not in publishers:
                    publishers.append(subfield)
        if publication_places:
            document["publication_places"] = publication_places
        if publishers:
            document["publishers"] = publishers


    # 215$a -> part_page_begin, part_page_end, extent_description, extent_duration, extent_volumes, extent_pages
    # 215$c -> physical_description_notes[i]/value
    physical_description_notes = []
    # 215$d -> extent_dimension
    # 215$e -> extent_accompanying_material
    if record['215'] is not None:
        part_volume = None
        part_issue = None
        part_page_begin = None
        part_page_end = None
        extent_accompanying_material = None
        extent_description_final = None
        extent_description = None
        extent_dimension = None
        extent_duration = None
        extent_pages = ""
        extent_volumes = ""
        if record['215']['a'] is not None:
            extent_description_final = record['215']['a']

            # debug: insert 215$a in extent_description_original
            document["extent_description_original"] = extent_description_final

            if rec_type in constants.DOC_TYPES_LIST_ARTICLES:
                # Articles types
                # examples :
                # 49 (3), mars 93 : p. 25-63.
                # p.29-169
                # (26), juil.-déc. 94 : p. 97-142 ; tabl., graph. ; bibliogr.
                # 27 (1-2), 1991 : p. 97-103 ; bibliogr.
                # (6446), 8 nov. 90 Numéro spécial : 106 p.
                # 11 (1), print. 92 : p. 26-39 ; tabl. ; bibliogr.
                # 27 (4), 1990 : p. 359-372 ; graph. ; bibliogr.
                # (21), janv.-mars 95 : p. 12-137 ; bibliogr.
                # (6656), 2 avr. 92 Numéro spécial : p. 8-104.
                # (1994)vol.27:n°2, p.479-532
                # (5), 1992 : p. 567-588 ; texte également en français.
                # 36 (6), juin 91 : p. 725-736 ; tabl.
                # 34 (3-4), aut.-hiv. 92 : p. 54-67 ; bibliogr.
                # part_issue, part_volume, date_issued, part_page_begin, part_page_end
                pass
                # TODO
                # part_volume
                # part_issue
                # date_issued ?
                # part_page_begin, part_page_end
            else :
                # Book et. al.
                # replace unwanted characters
                extent_description_final = extent_description_final.replace("(","").replace(")","").replace(";","").replace(":","")

                # extent_volumes : before extent_volumes_forms
                extent_volumes_forms = ["vol.",
                                        "v.",
                                        "atlas",
                                        "bobine de microfilm 35 mm positif",
                                        "classeur",
                                        u"disque optique numérique (CD-ROM)",
                                        "CD-ROM",
                                        "CDRom",
                                        "DVD",
                                        u"microfiches acétate",
                                        "microfiches",
                                        "recueil factice",
                                        u"tomes microfichés",
                                        "tomes",
                                        "tome"]
                for volumesform in extent_volumes_forms:
                    index = extent_description_final.find(volumesform.encode('utf-8'))
                    if index != -1:
                        length = len(volumesform.encode('utf-8'))
                        extent_volumes = extent_volumes + extent_description_final.encode('utf-8')[0:index+length].strip()
                        extent_description_final = extent_description_final[index+length:].strip()

                # extent_pages : before extent_pages_forms
                # examples : (431, 391 p.) ; X-266-30 p. ; (XVI-820, 762, 591, 464 p.) ; [4]f. de pl.
                extent_pages_forms = ["p. d'annexes",
                                      "p. de pl. h.-t.",
                                      "p. de pl. en coul.",
                                      "p. de pl. en noir et en coul.",
                                      "p. de pl. photogr. h.-t. en noir et en coul.",
                                      "p. de pl.",
                                      "p. de texte",
                                      "p. of plates",
                                      "p. multigr.",
                                      u"p. de supplément",
                                      "p. incl. tables",
                                      "p.",
                                      "ff. multigr.",
                                      "ff.",
                                      "f. multigr.",
                                      "f. de portr",
                                      "f. d'ill. en noir et en coul",
                                      "f.",
                                      #"cartes",
                                      #"carte",
                                      u"dépl.",
                                      "fac-sim. de presse",
                                      "fasc.",
                                      "f. de fac-sim.",
                                      "f. de pl.",
                                      u"f. de pl. dépl.",
                                      "f. de pl. en coul. en front.",
                                      "f. de pl. en coul.",
                                      "f. de pl. en front.",
                                      "f. de pl. en noir et en coul.",
                                      "f. de pl. hors-texte",
                                      "f. de pl. ill.",
                                      u"f. de pl. non reliées",
                                      u"f. de pl. plié",
                                      "leaf of plates",
                                      "leaves of plates",
                                      "microfiches",
                                      u"Non paginé multigr.",
                                      u"Non paginé",
                                      "Non pag.",
                                      u"non paginé",
                                      "planches",
                                      "p. de pl. en noir et en coul."
                                      "pl. en noir et en coul.",
                                      "pl. en coul",
                                      "pl. num.",
                                      "pl.",
                                      "pagination multiple",
                                      "Pagination multiple",
                                      "Pag. multiple",
                                      "pag. mult.",
                                      "various pagination",
                                      "loose-leaf",
                                      "images"]
                for pagesform in extent_pages_forms:
                    index = extent_description_final.find(pagesform.encode('utf-8'))
                    if index != -1:
                        length = len(pagesform.encode('utf-8'))
                        #length = len(pagesform)
                        extent_pages = extent_pages + extent_description_final.encode('utf-8')[0:index+length].strip()
                        extent_description_final = extent_description_final[index+length:].strip()

                # todo :
                # 2 h 17 min : extent_duration

                # if P. : part_page_begin and part_page_end (example : P. 166-171)
                index_part = extent_description_final.find("P.")
                if index_part != -1:
                    index_dash = extent_description_final[index_part:].find("-") + index_part
                    part_page_begin = extent_description_final[index_part+2:index_dash].strip()
                    part_page_end = extent_description_final[index_dash+1:].strip()
                    extent_description_final = extent_description_final[index_dash+1+len(part_page_end):].strip()

            # extent_description : before extent_volumes_forms
            desc_terms = ["bibliogr.",
                          "cartes",
                          "graph.",
                          "ill.",
                          u"multigraphié",
                          "port.",
                          u"résumé en anglais",
                          u"résumés en anglais",
                          u"résumés en anglais et en espagnol",
                          u"résumés en anglais et en français",
                          u"résumés en anglais et en russe",
                          u"résumés en français et en anglais",
                          "tabl"]
            for desc_term in desc_terms:
                index = extent_description_final.find(desc_term.encode('utf-8'))
                if index != -1:
                    length = len(volumesform.encode('utf-8'))
                    extent_description = extent_volumes + extent_description_final.encode('utf-8')[index:index+length].strip()
                    extent_description_final = extent_description_final[index+length:].strip()
            
        if record['215']['c'] is not None:
            # physical_description_notes
            physical_description_notes.append({"note_type":"material", "value":record['215']['c'].strip()})
        if record['215']['d'] is not None:
            # extent_dimension
            extent_dimension = record['215']['d'].strip()
        if record['215']['e'] is not None:
            # extent_accompanying_material
            extent_accompanying_material = record['215']['e'].strip()

        if part_volume:
            document["part_volume"] = part_volume
        if part_issue:
            document["part_issue"] = part_issue
        if part_page_begin:
            document["part_page_begin"] = part_page_begin
        if part_page_end:
            document["part_page_end"] = part_page_end
        if extent_accompanying_material:
            document["extent_accompanying_material"] = extent_accompanying_material
        if extent_description:
            document["extent_description"] = extent_description
        if extent_description_final:
            document["extent_description_final"] = extent_description_final
        if extent_dimension:
            document["extent_dimension"] = extent_dimension
        if extent_duration:
            document["extent_duration"] = extent_duration
        if extent_pages:
            document["extent_pages"] = extent_pages
        if extent_volumes:
            document["extent_volumes"] = extent_volumes

    # 3XX -> notes and physical_description_notes
    notes = []
    for field in record.get_fields('300','301','302','303','304','305','306','307','308','310','311','312','313','314','316','317','318','320','322','323','324','325','328','830'):
        if field.tag == '300' and field['a']:
             # 300$a : notes : general
            notes.append({"note_type":"general", "value":field['a']})
        elif field.tag == '301' and field['a']:
            # 301$a : notes : identifier
            notes.append({"note_type":"identifier", "value":field['a']})
        elif field.tag == '302' and field['a']:
            # 302$a : notes : encoded_information
            notes.append({"note_type":"encoded_information", "value":field['a']})
        elif field.tag == '303' and field['a']:
            # 303$a : notes : description
            notes.append({"note_type":"description", "value":field['a']})
        elif field.tag == '304' and field['a']:
            # 304$a : notes : title
            notes.append({"note_type":"title", "value":field['a']})
        elif field.tag == '305' and field['a']:
            # 305$a : notes : edition
            notes.append({"note_type":"edition", "value":field['a']})
        elif field.tag == '306' and field['a']:
            # 306$a : notes : publications
            notes.append({"note_type":"publications", "value":field['a']})
        elif field.tag == '307' and field['a']:
            # 307$a : physical_description_notes : physical_description
            physical_description_notes.append({"note_type":"physical_description", "value":field['a']})
        elif field.tag == '308' and field['a']:
            # 308$a : notes : series
            notes.append({"note_type":"series", "value":field['a']})
        elif field.tag == '310' and field['a']:
            # 310$a : physical_description_notes : binding
            physical_description_notes.append({"note_type":"binding", "value":field['a']})
        elif field.tag == '311' and field['a']:
            # 311$a : notes : link_fields
            notes.append({"note_type":"link_fields", "value":field['a']})
        elif field.tag == '312' and field['a']:
            # 312$a : notes : related_titles
            notes.append({"note_type":"related_titles", "value":field['a']})
        elif field.tag == '313' and field['a']:
            # 313$a : notes : subject_completeness
            notes.append({"note_type":"subject_completeness", "value":field['a']})
        elif field.tag == '314' and field['a']:
            # 314$a : notes : authors
            notes.append({"note_type":"authors", "value":field['a']})
        elif field.tag == '316' and field['a']:
            # 316$a : notes : copy
            notes.append({"note_type":"copy", "value":field['a']})
        elif field.tag == '317' and field['a']:
            # 317$a : notes : ownership
            notes.append({"note_type":"ownership", "value":field['a']})
        elif field.tag == '318' and field['a']:
            # 318$a : notes : conservation_history
            notes.append({"note_type":"conservation_history", "value":field['a']})
        elif field.tag == '320' and field['a']:
            # 320$a : notes : bibliography
            notes.append({"note_type":"bibliography", "value":field['a']})
        elif field.tag == '321' and field['a']:
            # 321$a : notes : index
            notes.append({"note_type":"index", "value":field['a']})
        elif field.tag == '322' and field['a']:
            # 322$a : notes : credits
            notes.append({"note_type":"credits", "value":field['a']})
        elif field.tag == '323' and field['a']:
            # 323$a : notes : performers
            notes.append({"note_type":"performers", "value":field['a']})
        elif field.tag == '324' and field['a']:
            # 324$a : notes : original_version
            notes.append({"note_type":"original_version", "value":field['a']})
        elif field.tag == '325' and field['a']:
            # 325$a : notes : reproduction
            notes.append({"note_type":"reproduction", "value":field['a']})
        elif field.tag == '328' and field['a']:
            # 328$a : notes : thesis
            notes.append({"note_type":"thesis", "value":field['a']})
        elif field.tag == '830' and field['a']:
            # 830$a : notes : cataloging
            notes.append({"note_type":"cataloging", "value":field['a']})

    if notes:
        document["notes"] = notes
    if physical_description_notes:
        document["physical_description_notes"] = physical_description_notes

    # 315$a ; 328$b ; 336$a -> rec_type_description
    rec_type_description = ""
    if record['315'] is not None and record['315']['a'] is not None:
        rec_type_description = record['315']['a'].strip() + " "
    if record['328'] is not None and record['328']['b'] is not None:
        rec_type_description = rec_type_description + record['328']['b'].strip() + " "
    if record['336'] is not None and record['336']['a'] is not None:
        rec_type_description = rec_type_description + record['336']['a'].strip() + " "
    if rec_type_description.strip():
        document["rec_type_description"] = rec_type_description.strip()

    if record['326'] is not None and record['326']['a'] is not None:
        document["frequency"] = record['326']['a'].strip()

    # 327 & 359 -> table_of_contentss[i]
    # value ($a)
    # content_type : undefined ($a), title1 ($b), title2 ($c), title3 ($d), title4 ($e), title5 ($f), title6 ($g), title7 ($h), title8 ($i)
    # part_page_begin ($p)
    # part_number ($v)
    # url ($u)
    # creators[i] ($z)




    # 330 -> descriptions[i]/value

    # 359

    # 410 or 225 -> seriess[i]
    # 410$t or 225$a -> seriess[i]/title
    # 410$o or 225$e -> seriess[i]/title_sub
    # 410$h or 410$v or 225$v -> seriess[i]/part_number
    # 410$a -> seriess[i]/creators[i]@role=edt
    # 410$c -> seriess[i]/publication_places[i]
    # 410$d -> seriess[i]/date_issued
    # 410$e -> seriess[i]/edition
    # 410$h -> seriess[i]/part_number
    # 410$i -> seriess[i]/part_name
    # 410$l -> seriess[i]/title_alternative
    # 410$m -> seriess[i]/identifiers[i]@id_type=ismn
    # 410$n -> seriess[i]/publishers[i]
    # 410$u -> seriess[i]/resources[i]/url
    # 410$x -> seriess[i]/identifiers[i]@id_type=issn
    # 410$y -> seriess[i]/identifiers[i]@id_type=isbn
    # 410$z -> seriess[i]/identifiers[i]@id_type=coden
    # 410$0 or 410$3 -> seriess[i]/rec_id

    # 454 -> originals[i]

    # 454$a -> originals[i]/creators[i]@role=aut

    # 454$c -> originals[i]/publisherPlace

    # 454$d -> originals[i]/dateIssued

    # 454$n -> originals[i]/publisher

    # 454$o -> originals[i]/title_sub

    # 454$t -> originals[i]/title

    # 461, 463 -> is_part_ofs[i]

    # 461$a, 463$a -> is_part_ofs[i]/title

    # 461$e, 463$e -> is_part_ofs[i]/title_sub

    # 463$n -> part_issue

    # 463$v -> part_volume

    # 464$a -> has_parts[i]/creators[i]@role=aut/agent/@rec_type=Person name_given name_family

    # 488

    # 500

    # 503

    # 517

    # 6XX -> subject
    subjects = []
    suject_agents = []
    if record.get_fields('600', '601', '602'):
        for field in record.get_fields('600', '601', '602'):
            creator = extract_unimarc_creator(field)
            if creator and "agent" in creator:
                subject = {"agents": [creator["agent"]]}
                suject_agents.append(subject)

    # 605

    # 606

    # 607
    if record.get_fields('607'):
        subjects = []
        for field in record.get_fields('607'):
            subject = {}
            # todo

    # 620

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

    # 801

    # 830 
    # resources
    # 856 : links -> resources
    resources = []
    fields_856 = record.get_fields('856')
    if fields_856:
        for field_856 in fields_856:
            resource = Resource()
            resource["rec_type"] = "remote"
            if field_856.get_subfields('u'):
                resource["url"] = field_856.get_subfields('u')[0]
            if field_856.get_subfields('z'):
                resource["label"] = field_856.get_subfields('z')[0]
            if resource:
                resources.append(resource)

    # 995 : holdings / copies -> resources
    fields_995 = record.get_fields('995')
    if fields_995:
        for field_995 in fields_995:
            resource = Resource()
            resource["rec_type"] = "physical"
            # $b -> physical_library ex: 751072303
            if field_995.get_subfields('b'):
                resource["physical_library"] = field_995.get_subfields('b')[0]
            # $c -> physical_location ex: BIB01
            if field_995.get_subfields('c'):
                resource["physical_location"] = field_995.get_subfields('c')[0]
            # $d -> physical_sub_location ex: MAG1
            if field_995.get_subfields('d'):
                resource["physical_sub_location"] = field_995.get_subfields('d')[0]
            # $e -> physical_collection ex: cad
            if field_995.get_subfields('e'):
                resource["physical_collection"] = field_995.get_subfields('e')[0]
            # $f -> physical_copy_number ex: 00000000926980
            if field_995.get_subfields('f'):
                resource["physical_copy_number"] = field_995.get_subfields('f')[0]
            # $k -> physical_call_number ex: BR.8°0947(13)
            if field_995.get_subfields('k'):
                resource["physical_call_number"] = field_995.get_subfields('k')[0].replace("Â°", "°")
            # $l -> physical_part_number ex: 2
            if field_995.get_subfields('l'):
                resource["physical_part_number"] = field_995.get_subfields('l')[0]
            # $o -> physical_category ex: L1
            if field_995.get_subfields('o'):
                resource["physical_category"] = field_995.get_subfields('o')[0]
            # $p -> physical_is_periodical ex: p
            if field_995.get_subfields('o') and field_995.get_subfields('o')[0] == "p":
                resource["physical_is_periodical"] = True
            # $r -> physical_availability ex: DI
            if field_995.get_subfields('r'):
                resource["physical_availability"] = field_995.get_subfields('r')[0]
            # $s -> rec_modified_date ex: YYYYMMDD
            if field_995.get_subfields('s'):
                resource["rec_modified_date"] = field_995.get_subfields('s')[0]
            # $u -> note ex: Ceci est une note
            if field_995.get_subfields('u'):
                resource["note"] = field_995.get_subfields('u')[0]
            # $v -> physical_issue_number ex: Vol. 52, no 1>6, 2002 : vol. relié
            if field_995.get_subfields('v'):
                resource["physical_issue_number"] = field_995.get_subfields('v')[0]
            # $w -> physical_issue_date ex: 2002
            if field_995.get_subfields('w'):
                resource["physical_issue_date"] = field_995.get_subfields('w')[0]
            if resource:
                resources.append(resource)
    if resources is not None:
        document["resources"] = resources

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
    field110ap0 = None
    field110ap1 = None
    if record['110'] is not None and record['110']['a'] is not None:
        field110ap0 = record['110']['a'][0:1]
        field110ap1 = record['110']['a'][1:2]

    # 115$a/0
    field115ap0 = None
    if record['115'] is not None and record['115']['a'] is not None:
        field115ap0 = record['115']['a'][0:1]

    # 116$a/0
    field116ap0 = None
    if record['116'] is not None and record['116']['a'] is not None:
        field116ap0 = record['116']['a'][0:1]
        #d = impression en gros caractères
        #e = journal
        #f = caractères Braille ou Moon
        #g = micro-impression
        #h = manuscrit
        #i = multimédia multisupport (Par exemple : un volume imprimé accompagné d’un supplément sur microfiches.)
        #j = impression en réduction
        #r = impression normale
        #s = ressource électronique
        #t = microforme
        #z = autres formes de présentation

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

    # logging.debug("leader6: {}".format(leader6))
    # logging.debug("leader7: {}".format(leader7))
    # logging.debug("100$a/17-19: {}".format(field100ap1719))
    # logging.debug("100$a/20: {}".format(field100ap20))
    # logging.debug("105/4-7: {}".format(field105ap48))
    # logging.debug("106$a: {}".format(field106a))
    # logging.debug("110$a/0: {}".format(field110ap0))
    # logging.debug("110$a/1: {}".format(field110ap1))
    # logging.debug("115$a/0: {}".format(field115ap0))
    # logging.debug("116/0: {}".format(field116ap0))
    # logging.debug("121$a/0: {}".format(field121ap0))
    # logging.debug("124$b: {}".format(field124b))
    # logging.debug("126$a/0: {}".format(field126ap0))
    # logging.debug("135$a/0: {}".format(field135ap0))

    if leader6 == "a":
        if leader7 == "a":
            rec_type = constants.DOC_TYPE_JOURNALARTICLE
        elif leader7 == "c":
            rec_type = constants.DOC_TYPE_PRESSCLIPPING
        elif leader7 == "m":
            rec_type = constants.DOC_TYPE_BOOK
        elif leader7 == "s":
            # 110 : Zone de données codées : Ressources continues
            # 110$a/0 Type de ressource continue
            if field110ap0 == "a":
                # a: périodique
                rec_type = constants.DOC_TYPE_JOURNAL
            elif field110ap0 == "b":
                # b: collection de monographies
                rec_type = constants.DOC_TYPE_MULTIVOLUMEBOOK
            elif field110ap0 == "c":
                # c: journal
                rec_type = constants.DOC_TYPE_NEWSPAPER
            elif field110ap0 == "e":
                # e: publication à feuillets mobiles et à mise à jour
                rec_type = constants.DOC_TYPE_LOOSELEAFPUBLICATION
            elif field110ap0 == "f":
                # f: base de données
                rec_type = constants.DOC_TYPE_DATABASE
            elif field110ap0 == "g":
                # g: site web à mise à jour
                rec_type = constants.DOC_TYPE_WEBSITE
            elif field110ap0 == "g":
                # z: autre
                rec_type = constants.DOC_TYPE_JOURNAL
            else:
                rec_type = constants.DOC_TYPE_JOURNAL

            # 110$a/1 field110ap1 : Périodicité
            if field110ap1 in ["a", "b", "c", "n"]:
                # a: quotidienne
                # b: bihebdomadaire
                # c: hebdomadaire
                # n: trois fois par semaine
                rec_type = constants.DOC_TYPE_NEWSPAPER

        else:
            rec_type = constants.DOC_TYPE_DOCUMENT

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
        # 135$a/0 field135ap0 : Zone de données codées : ressources électroniques
        if field135ap0 == "a":
            # a: données numériques
            rec_type = constants.DOC_TYPE_DATASETQUANTI
        elif field135ap0 == "b":
            # b: programme informatique
            rec_type = constants.DOC_TYPE_SOFTWARE
            # c: illustration
        elif field135ap0 == "d":
            # d: texte
            if leader7 == "a":
                rec_type = constants.DOC_TYPE_EJOURNALARTICLE
            elif leader7 == "c":
                rec_type = constants.DOC_TYPE_PRESSCLIPPING
            elif leader7 == "m":
                rec_type = constants.DOC_TYPE_EBOOK
            elif leader7 == "s":
                rec_type = constants.DOC_TYPE_EJOURNAL
        elif field135ap0 == "e":
            # e: données bibliographiques
            rec_type = constants.DOC_TYPE_BIBLIOGRAPHY
        elif field135ap0 == "f":
            # f: polices de caractères
            rec_type = constants.DOC_TYPE_FONT
        elif field135ap0 == "g":
            # g: jeu
            rec_type = constants.DOC_TYPE_GAME
        elif field135ap0 == "h":
            # h: son
            rec_type = constants.DOC_TYPE_AUDIORECORDING
        elif field135ap0 == "i":
            # i: multimédia interactif
            rec_type = constants.DOC_TYPE_MULTIMEDIA
        elif field135ap0 == "j":
            # j: système ou service en ligne
            rec_type = constants.DOC_TYPE_WEBSITE
        elif field135ap0 == "u":
            # u: inconnu
            rec_type = constants.DOC_TYPE_ERESOURCE
        elif field135ap0 == "v":
            # v: combinaison de données
            rec_type = constants.DOC_TYPE_DATASETQUANTI
            # z: autre
        else:
            if leader7 == "a":
                rec_type = constants.DOC_TYPE_EJOURNALARTICLE
            elif leader7 == "c":
                rec_type = constants.DOC_TYPE_PRESSCLIPPING
            elif leader7 == "m":
                rec_type = constants.DOC_TYPE_EBOOK
            elif leader7 == "s":
                rec_type = constants.DOC_TYPE_EJOURNAL
            else:
                rec_type = constants.DOC_TYPE_DOCUMENT
    elif leader6 == "m":
        rec_type = "Kit"
    elif leader6 == "r":
        rec_type = constants.DOC_TYPE_PHYSICALOBJECT
    else:
        rec_type = constants.DOC_TYPE_DOCUMENT

    return rec_type


def extract_unimarc_identifiers(record):
    # 0XX, 945 -> identifiers
    identifiers = []
    # 001 -> identifier ppn
    extract_unimarc_identifier(record, '001', 'data', 'ppn', identifiers)
    # 010 -> identifier isbn
    extract_unimarc_identifier(record, '010', 'a', 'isbn', identifiers)
    # 011 -> identifier issn
    # todo add $f
    extract_unimarc_identifier(record, '011', 'a', 'issn', identifiers)
    # 012 -> identifier imprint
    extract_unimarc_identifier(record, '012', 'a', 'imprint', identifiers)
    # 013 -> identifier ismn
    extract_unimarc_identifier(record, '013', 'a', 'ismn', identifiers)
    # 014 -> identifier sici or $2
    extract_unimarc_identifier(record, '014', 'a', 'sici', identifiers)
    # 015 -> identifier isrn
    extract_unimarc_identifier(record, '015', 'a', 'isrn', identifiers)
    # 016 -> identifier isrc
    extract_unimarc_identifier(record, '016', 'a', 'isrc', identifiers)
    # 017 -> identifier other
    extract_unimarc_identifier(record, '017', 'a', 'other', identifiers)
    # 020 -> identifier lccn
    extract_unimarc_identifier(record, '020', 'b', 'lccn', identifiers)
    # 021 -> identifier copyright
    extract_unimarc_identifier(record, '021', 'b', 'copyright', identifiers)
    # 022 -> identifier officialpub
    extract_unimarc_identifier(record, '022', 'b', 'officialpub', identifiers)
    # 029 -> identifier copyright
    extract_unimarc_identifier(record, '029', 'b', 'copyright', identifiers)
    # 035 -> identifier external
    extract_unimarc_identifier(record, '035', 'a', 'external', identifiers)
    # 036 -> identifier incipit
    extract_unimarc_identifier(record, '036', 'a', 'incipit', identifiers)
    # 040 -> identifier coden
    extract_unimarc_identifier(record, '040', 'a', 'coden', identifiers)
    # 071 -> identifier editref
    extract_unimarc_identifier(record, '071', 'a', 'editref', identifiers)
    # 072 -> identifier upc
    extract_unimarc_identifier(record, '072', 'a', 'upc', identifiers)
    # 073 -> identifier ean
    extract_unimarc_identifier(record, '073', 'a', 'ean', identifiers)
    # 945 -> identifier callnumber
    extract_unimarc_identifier(record, '945', 'b', 'callnumber', identifiers)
    return identifiers


def extract_unimarc_identifier(record, field, subfield, id_type, identifiers):
    identifier = None
    if record is not None and field is not None and record[field] is not None:
        if subfield == "data" and record[field].data is not None:
            identifier = {"id_type": id_type, "value": record[field].data}
        elif subfield is not None and record[field][subfield] is not None:
            if field == '014' and record[field]['2'] is not None:
                # case : id_type other than sici
                id_type = record[field]['2']
            identifier = {"id_type": id_type, "value": record[field][subfield]}
    if identifier:
        identifiers.append(identifier)


def extract_unimarc_creator(field):
    if field:
        creator = Creator()
        # $4 -> role
        if field['4'] and field['4'] in creator_service.role_unimarc_to_role_code:
            creator["roles"] = [creator_service.role_unimarc_to_role_code[field['4']]]
        else:
            creator["roles"] = ["ctb"]

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
            # todo Nom de marque
            pass

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
            # todo Intellectual responsability
            pass

        if creator:
            return creator

# get fields with encoding
def get_field_encoded():
    # as_key, with_dict, multiple, fields, subfields, positions, marc_charactersets
    string = "toto"
    string.decode("mab2")
    string.decode("utf8")

def format_dates_as_list(dates):
    if dates:
        # (1811-1882)
        # todo : pb with 710$c that can be another think than a date..
        return dates[0].replace("(","").replace(")","").replace("-....","").split("-")
