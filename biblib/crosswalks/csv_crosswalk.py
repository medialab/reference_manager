#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import csv
from datetime import datetime
import logging

from biblib.metajson import Document
from biblib.services import creator_service
from biblib.util import constants
from biblib.util import jsonbson


def csv_dict_reader_to_metasjon_list(csv_dict_reader, input_format, source, rec_id_prefix, only_first_record):
    logging.info(csv_dict_reader)
    for csv_row in csv_dict_reader:
        yield csv_dict_reader_to_metasjon(csv_row, input_format, source, rec_id_prefix)


def csv_dict_reader_to_metasjon(csv_row, input_format, source, rec_id_prefix):
    document = Document()

    if source:
        document["rec_source"] = source

    if input_format == constants.FORMAT_CSV_SITPOL:
        #logging.debug("csv_dict_reader_to_metasjon type(csv_row): {}".format(type(csv_row)))
        #print csv_row
        document["title"] = csv_row["title"]
        classifications_sitpol = [x.strip() for x in csv_row["classifications_sitpol"].split(";") if x.strip()]
        if classifications_sitpol:
            document["classifications_sitpol"] = classifications_sitpol
        classifications_ddc = [x.strip() for x in csv_row["classifications_ddc"].split(";") if x.strip()]
        if classifications_ddc:
            document["classifications_ddc"] = classifications_ddc
        formatted_names = [x.strip() for x in csv_row["creators@role=pbl"].split(";") if x.strip()]
        if formatted_names:
            #logging.debug("formatted_names: {}".format(formatted_names))
            creators = []
            for formatted_name in formatted_names:
                if formatted_name:
                    creator = creator_service.formatted_name_to_creator(formatted_name, None, "pbl")
                    if creator:
                        creators.append(creator)
            if creators:
                document["creators"] = creators
        document["date_last_accessed"] = datetime.now().isoformat()
        document["descriptions"] = [{"language":"fr", "value":csv_row["descriptions@lang=fr"]}]
        keywords_fr = [x.strip() for x in csv_row["keywords@lang=fr"].split(";") if x.strip()]
        keywords_en = [x.strip() for x in csv_row["keywords@lang=en"].split(";") if x.strip()]
        keywords = {}
        if keywords_fr:
            keywords["fr"] = keywords_fr
        if keywords_en:
            keywords["en"] = keywords_en
        if keywords:
            document["keywords"] = keywords
        document["languages"] = [x.strip() for x in csv_row["languages"].split(";") if x.strip()]
        note = csv_row["notes@lang=fr"]
        if note:
            document["notes"] = note
        document["publication_countries"] = [x.strip() for x in csv_row["publication_countries"].split(";") if x.strip()]
        document["rec_created_user"] = csv_row["rec_created_user"]
        document["rec_type_cerimes"] = csv_row["rec_type_cerimes"]
        specific_agents = [x.strip() for x in csv_row["specific_agents"].split(";") if x.strip()]
        if specific_agents:
            document["specific_agents"] = specific_agents
        document["specific_actor_type"] = csv_row["specific_actor_type"]
        document["target_audiences_cerimes"] = csv_row["target_audiences_cerimes"]
        document["url"] = csv_row["url"]
        document["rec_type"] = constants.DOC_TYPE_WEBENTITY
        document["webentity_type"] = csv_row["webentity_type"]
    elif input_format == constants.FORMAT_CSV_METAJSON:
        document["rec_type"] = "DatasetQuali"
        creators = []
        if "Laboratoire d'inventaire" in csv_row:
            creators.append(creator_service.formatted_name_to_creator(csv_row["Laboratoire d'inventaire"], constants.CLASS_ORGUNIT, "dpt"))
        document["title"] = csv_row["Titre de l'enquete"]
        if "Sujet(s) de l'enquete" in csv_row:
            document["keywords"] = [x.strip() for x in csv_row["Sujet(s) de l'enquete"].split("\n") if x.strip()]

        if "Nom Auteur 1" in csv_row:
            name_familly = csv_row["Nom Auteur 1"]
            name_given = affiliation = ""
            if "Prenom Auteur 1" in csv_row:
                name_given = csv_row["Prenom Auteur 1"]
            if "Affiliation Auteur 1" in csv_row:
                affiliation = csv_row["Affiliation Auteur 1"]


        document["creators"] = creators
    else:
        logging.error("Unknown input_format: {}".format(input_format))

    logging.info(jsonbson.dumps_json(document, True))
    return document

def metajson_list_to_csv_metajson(documents):
    csvwriter = csv.DictWriter(csv_file, delimiter=',', fieldnames=constants.fieldnames)
    csvwriter.writeheader()
    for key in sorted(results.iterkeys()):
        row = results[key]

