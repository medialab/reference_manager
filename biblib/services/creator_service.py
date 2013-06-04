#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from biblib import metajson
from biblib.metajson import Creator
from biblib.metajson import Event
from biblib.metajson import Person
from biblib.metajson import Orgunit
from biblib.metajson import Family

creator_person_terms_of_address = [
    "baron",
    "captain",
    "chevalier",
    "docteur",
    "don",
    "duc",
    "professeur"
]

creator_particule = [
    #composed:
    "de la",
    "de las",
    "de les",
    "de los",
    "van den",
    "van der",
    "von der",
    #simple
    "a",
    "af",
    "am",
    "an",
    "auf",
    "av",
    "d'",
    u"d’",
    "da",
    "dal",
    "dall'",
    u"dall’",
    "das",
    "de",
    "dei",
    "del",
    "della",
    "der",
    "des",
    "di",
    "dos",
    "du",
    "fra",
    "im",
    "la",
    "las",
    "le",
    "lo",
    "of",
    "ten-",
    "ter-",
    "van",
    "vom",
    "von",
    "y",
    "zu",
    "zum",
    "zur"
]

creator_role_terms = [
    "(Eds)",
    "(eds)",
    "(eds.)",
    u"(éd.)",
    "(ed.)",
    "(dir.)",
    "(dir)",
    "(co-directeur)",
    "(rapporteur)",
    u"(membre invité)",
    "sous la direction de",
    "sous la direction d'",
    "sous la dir. de",
    "sous la dir. d'",
    "edited by",
    u"présenté par",
    " et ",
    " and ",
    " & ",
    "et al.",
    "()",
    "[]"
]

creator_event_terms = [
    "colloque",
    "conference",
    u"conférence",
    "congress",
    u"journée",
    "symposium"
]

creator_orgunit_terms = [
    u"académie",
    "alternatives",
    "aosis",
    "archives",
    "association",
    "associates",
    "bank",
    "barnett & bridges",
    "business",
    "c2rmf",
    "center",
    "centre",
    "cepii",
    "ceri",
    u"cercle des économistes",
    "cnam",
    "cnn",
    "cnrs",
    "club",
    "collectif",
    "commission",
    u"commité",
    "committee",
    "confederation",
    "confederazione",
    "conseil",
    "conservatoire",
    "council",
    "crct",
    "direction",
    "droits",
    "ecole",
    u"édition",
    "enb",
    "euroframe",
    u"faculté",
    "faculty",
    "faculdade",
    u"fédération",
    "fondation",
    "forum",
    "groupe",
    "harmattan",
    "hopital",
    u"hôpital",
    "inc.",
    "institut",
    "institute",
    "insee",
    "journal",
    "laborato",
    "le monde",
    "library",
    "matra",
    "maudslay, sons and field",
    "media"
    "meteo-france",
    u"méteo-france",
    u"ministère",
    "ministry",
    "museum",
    u"musée",
    "museo",
    "naciones",
    "observatoire",
    "ofce",
    "office",
    "organisation",
    "paris match",
    "parliament",
    "parti",
    "photo",
    u"pôle",
    "presses",
    "programa",
    "ratp",
    "recherche",
    u"réservés"
    "ricerca",
    "school",
    "science",
    u"sénat",
    u"société",
    "society",
    u"società",
    "sofres",
    "trade",
    "tv",
    "unesco",
    "unfccc",
    "union",
    "universi",
    "wwf"
]

creator_citable_roles = [
    "aut",
    "edt"
]


def formatted_name_list_to_creator_list(formatted_name_list, creator_type="person", role="aut"):
    if formatted_name_list:
        creator_list = []
        for formatted_name in formatted_name_list:
            creator = formatted_name_to_creator(formatted_name, creator_type, role)
            if creator:
                creator_list.append(creator)
        return creator_list


def formatted_name_to_creator(formatted_name, creator_type, role):
    if formatted_name:
        formatted_name = formatted_name.strip()
        event = None
        family = None
        orgunit = None
        person = None

        #print("name: %s"%formatted_name)
        # creator_type determination
        for event_term in creator_event_terms:
            if event_term in formatted_name.lower():
                creator_type = "event"
                break
        for orgunit_term in creator_orgunit_terms:
            if orgunit_term in formatted_name.lower():
                creator_type = "orgunit"
                break
        if creator_type is None:
            creator_type = "person"

        creator = Creator()
        if role:
            creator["role"] = role

        if creator_type == "event":
            event = Event()
            event["title"] = formatted_name
            creator["agent"] = event

        elif creator_type == "orgunit":
            orgunit = Orgunit()
            orgunit["name"] = formatted_name
            creator["agent"] = orgunit

        elif creator_type == "person" or creator_type == "family":
            #type is "person" or "family"

            name_given = ""
            name_middle = ""
            name_family = ""
            name_prefix = ""
            name_terms_of_address = ""
            date_birth = ""
            date_death = ""

            parenthesis_index = formatted_name.rfind("(")
            if parenthesis_index != -1:
                #may be like: name (date_birth-date_death)
                dates_part = formatted_name[parenthesis_index + 1:-1].strip()
                date_birth = dates_part[:4]
                date_death = dates_part[5:]
                if date_death == "....":
                    date_death = ""
                formatted_name = formatted_name[:parenthesis_index].strip()

            slash_index = formatted_name.find("/")
            if slash_index != -1:
                #like: name/affiliation
                affiliation_name = formatted_name[slash_index + 1:].strip()
                formatted_name = formatted_name[:slash_index].strip()

            commaspacejrdot_index = formatted_name.rfind(", Jr.")
            if (commaspacejrdot_index != -1):
                #like "Paul B. Harvey, Jr."
                formatted_name = formatted_name[:commaspacejrdot_index].strip()
                name_middle = "Jr."

            #Is it formatted like "Family, Given" or "Given Family" ?
            comma_index = formatted_name.find(",")
            if comma_index == -1:
                space_index = formatted_name.rfind(" ")
                #print formatted_name
                #print space_index
                if space_index != -1:
                    #like Given Family
                    name_given = formatted_name[:space_index].strip()
                    name_family = formatted_name[space_index+1:].strip()
                else:
                    #like Family
                    name_family = formatted_name.strip()

            else:
                #like Family, Given
                name_family = formatted_name[:comma_index].strip()
                name_given = formatted_name[comma_index+1:].strip()

            # manage the terms_of_address and particule
            for term_of_address in creator_person_terms_of_address:
                if name_family and name_family.lower().startswith(term_of_address+" "):
                    name_terms_of_address = name_family[:len(term_of_address)]
                    name_family = name_family[len(term_of_address):].strip()
                if name_given:
                    if name_given.lower().endswith(" "+term_of_address):
                        name_terms_of_address = name_given[-len(term_of_address):]
                        name_given = name_given[:-len(term_of_address)].strip()
                    if name_given.lower().startswith(term_of_address+" "):
                        name_terms_of_address = name_given[:len(term_of_address)]
                        name_given = name_given[len(term_of_address):].strip()
                    if name_given.lower() == term_of_address:
                        name_terms_of_address = name_given
                        name_given = None

            # Be careful with a particule inside the name like: Viveiros de Castro, Eduardo
            for particule in creator_particule:
                if name_family and name_family.lower().startswith(particule+" "):
                    name_prefix = name_family[0:len(particule)]
                    name_family = name_family[len(particule):].strip()
                if name_given:
                    if name_given.lower().endswith(" "+particule):
                        name_prefix = name_given[-len(particule):]
                        name_given = name_given[:-len(particule)].strip()
                    if name_given.lower().startswith(particule+" "):
                        name_prefix = name_given[:len(particule)]
                        name_given = name_given[len(particule):].strip()
                    if name_given.lower() == particule:
                        name_prefix = name_given
                        name_given = None

            if creator_type == "person":
                person = Person()
                person.set_key_if_not_none("name_family", name_family)
                person.set_key_if_not_none("name_given", name_given)
                person.set_key_if_not_none("name_middle", name_middle)
                person.set_key_if_not_none("name_terms_of_address", name_terms_of_address)
                person.set_key_if_not_none("name_prefix", name_prefix)
                person.set_key_if_not_none("date_birth", date_birth)
                person.set_key_if_not_none("date_death", date_death)
                if 'affiliation_name' in vars() and affiliation_name:
                    #todo manage as an object
                    person["affiliations"] = [{"type": "orgunit", "preferred": True, "name": affiliation_name}]

                creator["agent"] = person

            elif creator_type == "family":
                family = Family()
                family.set_key_if_not_none("name_family", name_family)
                creator["agent"] = family

        #print json.dumps(creator,ensure_ascii=False,indent=4,encoding="utf-8")
        return creator


def formatted_name(creator, style=metajson.STYLE_FAMILY_COMMA_GIVEN):
    if creator:
        return creator.formatted_name(style)


def change_contibutors_role(creators, role):
    if creators:
        for creator in creators:
            creator.set_key_if_not_none("role", role)
    return creators
