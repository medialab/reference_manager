#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from metadatas.metajson import Contributor
from metadatas.metajson import Event
from metadatas.metajson import Person
from metadatas.metajson import Orgunit

contributor_person_terms_of_address=[
    "baron",
    "captain",
    "chevalier",
    "docteur",
    "don",
    "duc",
    "professeur"
]

contributor_particule=[
    #composed :
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

contributor_role_terms=[
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

contributor_event_terms=[
    "colloque",
    "conference",
    u"conférence",
    "congress",
    u"journée",
    "symposium"
]

contributor_orgunit_terms=[
    u"académie",
    "alternatives",
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
    "euroframe",
    u"faculté",
    "faculty",
    "faculdade",
    u"fédération",
    "fondation",
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
    "union",
    "universi"
]

contributor_citable_roles=[
    "aut",
    "edt"
]

def convert_formatted_name_list_to_contributor_list(formatted_name_list, contributor_type = "person", role = "aut"):
    if formatted_name_list :
        contributor_list = []
        for formatted_name in formatted_name_list :
            contributor = convert_formatted_name_to_contributor(formatted_name, contributor_type, role)
            if contributor:
                contributor_list.append(contributor)
        return contributor_list

def convert_formatted_name_to_contributor(formatted_name, contributor_type, role):
    if formatted_name :
        formatted_name = formatted_name.strip()
        event = None
        family = None
        orgunit = None
        person = None

        #print("name : %s"%formatted_name)
        # contributor_type determination
        for event_term in contributor_event_terms:
            if event_term in formatted_name.lower():
                contributor_type = "event"
                break
        for orgunit_term in contributor_orgunit_terms:
            if orgunit_term in formatted_name.lower():
                contributor_type = "orgunit"
                break
        if contributor_type is None:
            contributor_type = "person"

        contributor = Contributor()
        if role:
            contributor["role"] = role

        if contributor_type == "event" :
            event = Event()
            event["title"] = formatted_name
            contributor["event"] = event

        elif contributor_type == "orgunit" :
            orgunit = Orgunit()
            orgunit["name"] = formatted_name
            contributor["orgunit"] = orgunit

        elif contributor_type == "person" or contributor_type == "family" :
            #type is "person" or "family"

            name_given = ""
            name_middle = ""
            name_family = ""
            name_particule_non_dropping = ""
            name_terms_of_address = ""
            date_of_birth = ""
            date_of_death = ""
            
            parenthesis_index = formatted_name.rfind("(")
            if parenthesis_index != -1 :
                #may be like : name (date_of_birth-date_of_death)
                dates_part = formatted_name[parenthesis_index + 1:-1].strip()
                date_of_birth = dates_part[:4]
                date_of_death = dates_part[5:]
                if date_of_death == "....":
                    date_of_death = ""
                formatted_name = formatted_name[:parenthesis_index].strip()

            slash_index = formatted_name.find("/")
            if slash_index != -1 :
                #like : name/affiliation
                affiliation_name = formatted_name[slash_index + 1:].strip()
                formatted_name = formatted_name[:slash_index].strip()
            
            commaspacejrdot_index = formatted_name.rfind(", Jr.")
            if (commaspacejrdot_index != -1) :
                #like "Paul B. Harvey, Jr."
                formatted_name = value[:commaspacejrdot_index].strip()
                name_middle = "Jr."
            
            #Is it formatted like "Family, Given" or "Given Family" ?
            comma_index = formatted_name.find(",")
            if comma_index == -1 :
                space_index = formatted_name.rfind(" ")
                #print formatted_name
                #print space_index
                if space_index != -1 :
                    #like Given Family
                    name_given = formatted_name[:space_index].strip()
                    name_family = formatted_name[space_index+1:].strip()
                else :
                    #like Family
                    name_family = formatted_name.strip()

            else :
                #like Family, Given
                name_family = formatted_name[:comma_index].strip()
                name_given = formatted_name[comma_index+1:].strip()

            # manage the terms_of_address and particule
            for term_of_address in contributor_person_terms_of_address :
                if name_family and name_family.lower().startswith(term_of_address+" ") :
                    name_terms_of_address=name_family[:len(term_of_address)]
                    name_family=name_family[len(term_of_address):].strip()
                if name_given :
                    if name_given.lower().endswith(" "+term_of_address) :
                        name_terms_of_address=name_given[-len(term_of_address):]
                        name_given=name_given[:-len(term_of_address)].strip()
                    if name_given.lower().startswith(term_of_address+" ") :
                        name_terms_of_address=name_given[:len(term_of_address)]
                        name_given=name_given[len(term_of_address):].strip()
                    if name_given.lower() == term_of_address :
                        name_terms_of_address=name_given
                        name_given=None

            # Be careful with a particule inside the name like : Viveiros de Castro, Eduardo
            for particule in contributor_particule :
                if name_family and name_family.lower().startswith(particule+" ") :
                    name_particule_non_dropping=name_family[0:len(particule)]
                    name_family=name_family[len(particule):].strip()
                if name_given :
                    if name_given.lower().endswith(" "+particule) :
                        name_particule_non_dropping=name_given[-len(particule):]
                        name_given=name_given[:-len(particule)].strip()
                    if name_given.lower().startswith(particule+" ") :
                        name_particule_non_dropping=name_given[:len(particule)]
                        name_given=name_given[len(particule):].strip()
                    if name_given.lower() == particule :
                        name_particule_non_dropping=name_given
                        name_given=None

            if contributor_type == "person" :
                person = Person()
                person.set_key_if_not_none("name_family",name_family)
                person.set_key_if_not_none("name_given",name_given)
                person.set_key_if_not_none("name_middle",name_middle)
                person.set_key_if_not_none("name_terms_of_address",name_terms_of_address)
                person.set_key_if_not_none("name_particule_non_dropping",name_particule_non_dropping)
                person.set_key_if_not_none("date_of_birth",date_of_birth)
                person.set_key_if_not_none("date_of_death",date_of_death)
                if vars().has_key('affiliation_name') and affiliation_name :
                    #todo manage as an object
                    person["affiliations"]=[{"type" :"orgunit","preferred" :True,"name" :affiliation_name}]
                
                contributor["person"] = person
            
            elif contributor_type == "family" :
                family = Family()
                family.set_key_if_not_none("name_family",name_family)
                contributor["family"] = family
        
        #print json.dumps(contributor,ensure_ascii=False,indent=4,encoding="utf-8")
        return contributor


def change_contibutors_role(contributors, role) :
    if contributors :
        for contributor in contributors :
            contributor.set_key_if_not_none("role",role)
    return contributors
