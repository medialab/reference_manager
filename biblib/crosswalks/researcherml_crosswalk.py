#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import QName

from biblib.metajson import Creator
from biblib.metajson import Document
from biblib.metajson import Event
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Project
from biblib.metajson import Resource
from biblib.metajson import Rights
from biblib.services import creator_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import constants


def register_namespaces():
    for key in constants.xmlns_map:
        ET.register_namespace(key, constants.xmlns_map[key])


def prefixtag(ns_prefix, tagname):
    if tagname:
        if ns_prefix and ns_prefix in constants.xmlns_map:
            return str(QName(constants.xmlns_map[ns_prefix], tagname))
        else:
            return tagname


def researcherml_xmletree_to_metajson_list(rml_root, source, only_first_record):
    if rml_root is not None:
        for child in rml_root:
            # person
            if child.tag.endswith("person"):
                yield rml_person_to_metajson(child, source)
            # orgunit
            elif child.tag.endswith("orgUnit"):
                yield rml_orgunit_to_metajson(child, source)
            # project
            elif child.tag.endswith("project"):
                yield rml_project_to_metajson(child, source)


def rml_orgunit_to_metajson(rml_orgunit, source):
    orgunit = Orgunit()

    # acronym -> acronym

    # address -> addresses
    orgunit.update(extract_rml_addresses(rml_orgunit))

    # affiliation -> affiliations

    # award -> awards

    # ckbData ->

    # dateOfDissolution -> date_dissolution

    # dateOfFoundation -> date_foundation

    # description -> descriptions

    # email -> emails
    orgunit.update(extract_rml_emails(rml_orgunit))

    # headcount -> headcounts

    # identifier -> identifiers
    orgunit.update(extract_rml_identifiers(rml_orgunit))

    # image -> image_urls
    orgunit.update(extract_rml_images(rml_orgunit))

    # name -> name

    # nameAlternative ->

    # nationality -> nationality
    orgunit.update(extract_element_and_set_key(rml_orgunit, "nationality", "nationality"))

    # note -> notes

    # olDescription -> Descriptions_short

    # phone -> phones
    orgunit.update(extract_rml_phones(rml_orgunit))

    # researchCoverage -> research_coverages

    # skill -> skills

    # turnover -> turnovers

    # type ->

    # uri -> urls
    orgunit.update(extract_rml_uris(rml_orgunit))

    return orgunit


def rml_person_to_metajson(rml_person, source):
    person = Person()

    # academicTitle, honorificTitle -> titles
    person.update(extract_rml_titles(rml_person))

    # affiliation -> affiliations

    # address -> addresses
    person.update(extract_rml_addresses(rml_person))

    # award -> awards
    person.update(extract_rml_string_lang(rml_person, "award", "awards"))

    # biography -> biographies
    person.update(extract_rml_string_lang(rml_person, "biography", "biographies"))

    # dateOfBirth -> date_birth
    person.update(extract_element_and_set_key(rml_person, "dateOfBirth", "date_birth"))

    # dateOfDeath -> date_death
    person.update(extract_element_and_set_key(rml_person, "dateOfDeath", "date_death"))

    # degree -> degrees

    # email -> emails
    person.update(extract_rml_emails(rml_person))

    # fictitious
    fictitious = rml_person.get("fictitious")
    if fictitious is not None and fictitious.strip() == "true":
        person["fictitious"] = fictitious

    # firstname -> name_given
    person.update(extract_element_and_set_key(rml_person, "firstname", "name_given"))

    # identifier -> identifiers
    person.update(extract_rml_identifiers(rml_person))

    # image -> image_urls
    person.update(extract_rml_images(rml_person))

    # instantMessage -> instant_messages
    person.update(extract_rml_instant_messages(rml_person))

    # languageCapability -> language_capabilities
    person.update(extract_rml_language_capabilities(rml_person))

    # lastname -> name_family
    person.update(extract_element_and_set_key(rml_person, "lastname", "name_family"))

    # lastnamePrefix -> name_prefix
    person.update(extract_element_and_set_key(rml_person, "lastnamePrefix", "name_prefix"))

    # lastnameSuffix -> name_suffix
    person.update(extract_element_and_set_key(rml_person, "lastnameSuffix", "name_suffix"))

    # middlename -> name_middle
    person.update(extract_element_and_set_key(rml_person, "middlename", "name_middle"))

    # nationality -> nationality
    person.update(extract_element_and_set_key(rml_person, "nationality", "nationality"))

    # nickname -> name_nick
    person.update(extract_element_and_set_key(rml_person, "nickname", "name_nick"))

    # note -> notes
    person.update(extract_rml_string_lang(rml_person, "note", "notes"))

    # olBiography -> biographies_short
    person.update(extract_rml_string_lang(rml_person, "olBiography", "biographies_short"))

    # ongoingResearch ->

    # phone -> phones
    person.update(extract_rml_phones(rml_person))

    # relationship ->

    # researchCoverage -> 

    # responsability -> responsabilities
    person.update(extract_rml_string_lang(rml_person, "responsability", "responsabilities"))

    # sex -> gender
    person.update(extract_element_and_set_key(rml_person, "sex", "gender"))

    # skill -> skills
    person.update(extract_rml_string_lang(rml_person, "skill", "skills"))

    # teaching -> teachings

    # uri -> urls
    person.update(extract_rml_uris(rml_person))

    return person


def rml_project_to_metajson(rml_project, source):
    project = Project()
    
    # acronym -> 

    # award -> 

    # call -> 
    
    # contribution -> 

    # cost -> 

    # dateBegin -> 

    # dateEnd -> 

    # description -> 

    # duration -> 

    # identifiers -> 
    project.update(extract_rml_identifiers(rml_project))

    # note -> 

    # olDescription -> 

    # participant -> 

    # researchCoverage -> 

    # status -> 

    # title -> 

    # titleAlternative -> 

    # uri -> 

    return project


def extract_rml_addresses(rml):
    result = {}
    rml_addresses = rml.findall(prefixtag("rml", "address"))
    if rml_addresses is not None:
        addresses = []
        for rml_address in rml_addresses:
            if rml_address is not None:
                preferred = rml_address.get("preferred")
                relation_type = rml_address.get("relationType")
                visible = rml_address.get("visible")
                street = extract_text_or_none(rml_address.find(prefixtag("rml", "street")))
                post_code = extract_text_or_none(rml_address.find(prefixtag("rml", "postCode")))
                locality_city_town = extract_text_or_none(rml_address.find(prefixtag("rml", "localityCityTown")))
                country = extract_text_or_none(rml_address.find(prefixtag("rml", "country")))
                address = metajson_service.create_address(street, post_code, locality_city_town, country, preferred, relation_type, visible)
                if address:
                    addresses.append(address)
        if addresses:
            result["addresses"] = addresses
    return result


def extract_rml_emails(rml):
    result = {}
    rml_emails = rml.findall(prefixtag("rml", "email"))
    if rml_emails is not None:
        emails = []
        for rml_email in rml_emails:
            if rml_email is not None:
                preferred = rml_email.get("preferred")
                relation_type = rml_email.get("relationType")
                visible = rml_email.get("visible")
                value = extract_text_or_none(rml_email)

                email = metajson_service.create_email(value, preferred, relation_type, visible)
                if email:
                    emails.append(email)
        if emails:
            result["emails"] = emails
    return result


def extract_rml_identifiers(rml):
    result = {}
    rml_identifiers = rml.findall(prefixtag("rml", "identifier"))
    if rml_identifiers is not None:
        identifiers = []
        for rml_identifier in rml_identifiers:
            if rml_identifier is not None:
                id_type = rml_identifier.get("type")
                id_value = extract_text_or_none(rml_identifier)
                identifier = metajson_service.create_identifier(id_type, id_value)
                if identifier is not None:
                    identifiers.append(identifier)
        if identifiers:
            result["identifiers"] = identifiers
    return result


def extract_rml_images(rml):
    result = {}
    rml_images = rml.findall(prefixtag("rml", "image"))
    if rml_images is not None:
        images = []
        for rml_image in rml_images:
            if rml_image is not None:
                url = extract_text_or_none(rml_image)
                image = metajson_service.create_image_url(url)
                if image is not None:
                    images.append(image)
        if images:
            result["image_urls"] = images
            # todo : metajson
    return result


def extract_rml_instant_messages(rml):
    result = {}
    rml_ims = rml.findall(prefixtag("rml", "instantMessageType"))
    if rml_ims is not None:
        ims = []
        for rml_im in rml_ims:
            if rml_im is not None:
                preferred = rml_im.get("preferred")
                relation_type = rml_im.get("relationType")
                visible = rml_im.get("visible")
                service = rml_im.get("service")
                value = extract_text_or_none(rml_im)

                im = metajson_service.create_instant_message(value, service, preferred, relation_type, visible)
                if im:
                    ims.append(im)
        if ims:
            result["instant_messages"] = ims
    return result


def extract_rml_language_capabilities(rml):
    result = {}
    rml_lcs = rml.findall(prefixtag("rml", "languageCapability"))
    if rml_lcs is not None:
        lcs = []
        for rml_lc in rml_lcs:
            if rml_lc is not None:
                # language
                rml_language = rml_lc.find(prefixtag("rml", "language"))
                language = extract_text_or_none(rml_language)

                # motherTong
                rml_mother_tong = rml_lc.find(prefixtag("rml", "motherTong"))
                mother_tong = extract_boolean(rml_mother_tong)

                # oralInput
                rml_oral_input = rml_lc.find(prefixtag("rml", "oralInput"))
                oral_input = extract_text_or_none(rml_oral_input)

                # oralOutput
                rml_oral_output = rml_lc.find(prefixtag("rml", "oralOutput"))
                oral_output = extract_text_or_none(rml_oral_output)

                # textInput
                rml_text_input = rml_lc.find(prefixtag("rml", "textInput"))
                text_input = extract_text_or_none(rml_text_input)

                # textOutput
                rml_text_output = rml_lc.find(prefixtag("rml", "textOutput"))
                text_output = extract_text_or_none(rml_text_output)

                lc = metajson_service.create_language_capability(language, mother_tong, oral_input, oral_output, text_input, text_output)
                if lc is not None:
                    lcs.append(lc)
        if lcs:
            result["language_capabilities"] = lcs
    return result


def extract_rml_phones(rml):
    result = {}
    rml_phones = rml.findall(prefixtag("rml", "phone"))
    if rml_phones is not None:
        phones = []
        for rml_phone in rml_phones:
            if rml_phone is not None:
                preferred = rml_phone.get("preferred")
                relation_type = rml_phone.get("relationType")
                phone_type = rml_phone.get("type")
                visible = rml_phone.get("visible")
                rml_formatted = rml_phone.find(prefixtag("rml", "formatted"))
                formatted = extract_text_or_none(rml_formatted)

                phone = metajson_service.create_phone(formatted, phone_type, preferred, relation_type, visible)
                if phone:
                    phones.append(phone)
        if phones:
            result["phones"] = phones
    return result


def extract_rml_titles(rml):
    result = {}
    titles = []

    # academicTitle -> titles with title_type = "academic"
    result_academic = extract_rml_string_lang(rml, "academicTitle", "titles")
    if "titles" in result_academic:
        for title in result_academic["titles"]:
            title["title_type"] = "academic"
            titles.append(title)

    # honorificTitle -> titles with title_type = "honorific"
    result_honorific = extract_rml_string_lang(rml, "honorificTitle", "titles")
    if "titles" in result_honorific:
        for title in result_honorific["titles"]:
            title["title_type"] = "honorific"
            titles.append(title)

    if titles:
        result["titles"] = titles
    return result


def extract_rml_uris(rml):
    result = {}
    rml_uris = rml.findall(prefixtag("rml", "uri"))
    if rml_uris is not None:
        uris = []
        for rml_uri in rml_uris:
            if rml_uri is not None:
                preferred = rml_uri.get("preferred")
                relation_type = rml_uri.get("relationType")
                visible = rml_uri.get("visible")
                value = extract_text_or_none(rml_uri)

                uri = metajson_service.create_uri(value, preferred, relation_type, visible)
                if uri:
                    uris.append(uri)
        if uris:
            result["urls"] = uris
    return result


def extract_rml_string_lang(rml, element, key):
    result = {}
    rml_sls = rml.findall(prefixtag("rml", element))
    if rml_sls is not None:
        sls = []
        for rml_sl in rml_sls:
            if rml_sl is not None:
                language = rml_sl.get(prefixtag("xml", "lang"))
                value = rml_sl.text.strip()
                if value is not None:
                    sl = {"value": value}
                    if language is not None:
                        sl["language"] = language.strip()
                    sls.append(sl)
        if sls:
            result[key] = sls
    return result


def extract_text_or_none(element):
    if element is not None:
        result = element.text.strip()
    else:
        result = None
    return result


def extract_boolean(element):
    if element is not None and element.text.strip() == "true":
        result = True
    else:
        result = False
    return result


def extract_element_and_set_key(rml, element, key):
    result = {}
    element_xmletree = rml.find(prefixtag("rml", element))
    key_value = extract_text_or_none(element_xmletree)
    if key_value is not None:
        result[key] = key_value
    return result


