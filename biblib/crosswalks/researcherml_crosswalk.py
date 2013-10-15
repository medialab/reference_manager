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
    orgunit.update(extract_element_and_set_key(rml_orgunit, "acronym", "acronym"))

    # address -> addresses
    orgunit.update(extract_rml_addresses(rml_orgunit))

    # affiliation -> affiliations
    orgunit.update(extract_rml_affiliations(rml_orgunit))

    # award -> awards
    orgunit.update(extract_rml_string_lang(rml_orgunit, "award", "awards"))

    # ckbData ->

    # dateOfDissolution -> date_dissolution
    orgunit.update(extract_element_and_set_key(rml_orgunit, "dateOfDissolution", "date_dissolution"))

    # dateOfFoundation -> date_foundation
    orgunit.update(extract_element_and_set_key(rml_orgunit, "dateOfFoundation", "date_foundation"))

    # description -> descriptions
    orgunit.update(extract_rml_string_lang(rml_orgunit, "description", "descriptions"))

    # email -> emails
    orgunit.update(extract_rml_emails(rml_orgunit))

    # headcount -> headcounts
    orgunit.update(extract_rml_headcounts(rml_orgunit))

    # identifier -> identifiers
    orgunit.update(extract_rml_identifiers(rml_orgunit))

    # image -> image_urls
    orgunit.update(extract_rml_images(rml_orgunit))

    # name -> name
    orgunit.update(extract_element_and_set_key(rml_orgunit, "name", "name"))

    # nameAlternative ->
    orgunit.update(extract_rml_string_lang(rml_orgunit, "nameAlternative", "name_alternatives"))

    # nationality -> nationality
    orgunit.update(extract_element_and_set_key(rml_orgunit, "nationality", "nationality"))

    # note -> notes
    orgunit.update(extract_rml_string_lang(rml_orgunit, "note", "notes"))

    # olDescription -> descriptions_short
    orgunit.update(extract_rml_string_lang(rml_orgunit, "olDescription", "descriptions_short"))

    # phone -> phones
    orgunit.update(extract_rml_phones(rml_orgunit))

    # researchCoverage -> research_coverages
    orgunit.update(extract_rml_research_coverages(rml_orgunit))

    # skill -> skills
    orgunit.update(extract_rml_string_lang(rml_orgunit, "skill", "skills"))

    # turnover -> turnovers
    orgunit.update(extract_rml_turnovers(rml_orgunit))

    # type -> rec_type
    orgunit.update(extract_attribute_and_set_key(rml_orgunit, "type", "rec_type"))

    # uri -> urls
    orgunit.update(extract_rml_uris(rml_orgunit))

    return orgunit


def rml_person_to_metajson(rml_person, source):
    person = Person()

    # academicTitle, honorificTitle -> titles
    person.update(extract_rml_titles(rml_person))

    # affiliation -> affiliations
    person.update(extract_rml_affiliations(rml_person))

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
    person.update(extract_boolean_attribute_and_set_key(rml_person, "fictitious", "fictitious"))

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
    person.update(extract_rml_research_coverages(rml_person))

    # responsability -> responsabilities
    person.update(extract_rml_string_lang(rml_person, "responsability", "responsabilities"))

    # sex -> gender
    person.update(extract_element_and_set_key(rml_person, "sex", "gender"))

    # skill -> skills
    person.update(extract_rml_string_lang(rml_person, "skill", "skills"))

    # teaching -> teachings
    person.update(extract_rml_teachings(rml_person))

    # uri -> urls
    person.update(extract_rml_uris(rml_person))

    return person


def rml_project_to_metajson(rml_project, source):
    project = Project()
    
    # acronym -> acronym

    # award -> award

    # call -> call
    
    # contribution -> creators

    # cost -> cost

    # dateBegin -> date_start

    # dateEnd -> date_end

    # description -> descriptions

    # duration -> extent_duration

    # identifier -> identifiers
    project.update(extract_rml_identifiers(rml_project))

    # note -> notes

    # olDescription -> descriptions_short

    # participant -> 

    # researchCoverage -> 

    # status -> 

    # title -> title

    # titleAlternative -> title_alternative

    # uri -> urls

    return project


def extract_rml_addresses(rml):
    result = {}
    rml_addresses = rml.findall(prefixtag("rml", "address"))
    if rml_addresses is not None:
        addresses = []
        for rml_address in rml_addresses:
            if rml_address is not None:
                preferred = get_attribute_boolean(rml_address, "preferred")
                relation_type = rml_address.get("relationType")
                visible = get_attribute_boolean(rml_address, "visible")
                street = get_text_or_none(rml_address.find(prefixtag("rml", "street")))
                post_code = get_text_or_none(rml_address.find(prefixtag("rml", "postCode")))
                locality_city_town = get_text_or_none(rml_address.find(prefixtag("rml", "localityCityTown")))
                country = get_text_or_none(rml_address.find(prefixtag("rml", "country")))
                address = metajson_service.create_address(street, post_code, locality_city_town, country, preferred, relation_type, visible)
                if address:
                    addresses.append(address)
        if addresses:
            result["addresses"] = addresses
    return result


def extract_rml_affiliations(rml):
    result = {}
    rml_affiliations = rml.findall(prefixtag("rml", "affiliation"))
    if rml_affiliations is not None:
        affiliations = []
        for rml_affiliation in rml_affiliations:
            if rml_affiliation is not None:
                preferred = get_attribute_boolean(rml_affiliation, "preferred")

                rml_relation_type = rml_affiliation.find(prefixtag("rml", "relationType"))
                role = get_text_or_none(rml_relation_type)

                rml_date_begin = rml_affiliation.find(prefixtag("rml", "dateBegin"))
                date_start = get_text_or_none(rml_date_begin)

                rml_date_end = rml_affiliation.find(prefixtag("rml", "dateEnd"))
                date_end = get_text_or_none(rml_date_end)

                identifiers = extract_rml_identifiers(rml_affiliation)
                rec_id = None
                if "identifiers" in identifiers and identifiers["identifiers"]:
                    rec_id = identifiers["identifiers"][0]["value"]

                rml_name = rml_affiliation.find(prefixtag("rml", "name"))
                name = get_text_or_none(rml_name)

                affiliation = metajson_service.create_affiliation(rec_id, name, role, date_start, date_end, preferred)
                if affiliation is not None:
                    affiliations.append(affiliation)
        if affiliations:
            result["affiliations"] = affiliations
    return result


def extract_rml_emails(rml):
    result = {}
    rml_emails = rml.findall(prefixtag("rml", "email"))
    if rml_emails is not None:
        emails = []
        for rml_email in rml_emails:
            if rml_email is not None:
                preferred = get_attribute_boolean(rml_email, "preferred")
                relation_type = rml_email.get("relationType")
                visible = get_attribute_boolean(rml_email, "visible")
                value = get_text_or_none(rml_email)

                email = metajson_service.create_email(value, preferred, relation_type, visible)
                if email:
                    emails.append(email)
        if emails:
            result["emails"] = emails
    return result


def extract_rml_headcounts(rml):
    result = {}
    rml_headcounts = rml.findall(prefixtag("rml", "headcount"))
    if rml_headcounts is not None:
        headcounts = []
        for rml_headcount in rml_headcounts:
            if rml_headcount is not None:
                year = rml_headcount.get("year")
                value = rml_headcount.text.strip()
                if value is not None:
                    headcount = {"value": value}
                    if year is not None:
                        headcount["year"] = year.strip()
                    headcounts.append(headcount)
        if headcounts:
            result["headcounts"] = headcounts
    return result


def extract_rml_identifiers(rml):
    result = {}
    rml_identifiers = rml.findall(prefixtag("rml", "identifier"))
    if rml_identifiers is not None:
        identifiers = []
        for rml_identifier in rml_identifiers:
            if rml_identifier is not None:
                id_type = rml_identifier.get("type")
                id_value = get_text_or_none(rml_identifier)
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
                url = get_text_or_none(rml_image)
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
                preferred = get_attribute_boolean(rml_im, "preferred")
                relation_type = rml_im.get("relationType")
                visible = get_attribute_boolean(rml_im, "visible")
                service = rml_im.get("service")
                value = get_text_or_none(rml_im)

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
                language = get_text_or_none(rml_language)

                # motherTong
                rml_mother_tong = rml_lc.find(prefixtag("rml", "motherTong"))
                mother_tong = get_boolean(rml_mother_tong)

                # oralInput
                rml_oral_input = rml_lc.find(prefixtag("rml", "oralInput"))
                oral_input = get_text_or_none(rml_oral_input)

                # oralOutput
                rml_oral_output = rml_lc.find(prefixtag("rml", "oralOutput"))
                oral_output = get_text_or_none(rml_oral_output)

                # textInput
                rml_text_input = rml_lc.find(prefixtag("rml", "textInput"))
                text_input = get_text_or_none(rml_text_input)

                # textOutput
                rml_text_output = rml_lc.find(prefixtag("rml", "textOutput"))
                text_output = get_text_or_none(rml_text_output)

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
                preferred = get_attribute_boolean(rml_phone, "preferred")
                relation_type = rml_phone.get("relationType")
                phone_type = rml_phone.get("type")
                visible = get_attribute_boolean(rml_phone, "visible")
                rml_formatted = rml_phone.find(prefixtag("rml", "formatted"))
                formatted = get_text_or_none(rml_formatted)

                phone = metajson_service.create_phone(formatted, phone_type, preferred, relation_type, visible)
                if phone:
                    phones.append(phone)
        if phones:
            result["phones"] = phones
    return result


def extract_rml_research_coverages(rml):
    result = {}
    rml_rcs = rml.findall(prefixtag("rml", "researchCoverage"))
    if rml_rcs is not None:
        rc_classifications = []
        rc_keywords = {}
        for rml_rc in rml_rcs:
            if rml_rc is not None:
                value = rml_rc.text.strip()
                if value is not None:
                    rc_type = rml_rc.get("type")
                    if rc_type == "keyword":
                        language = rml_rc.get(prefixtag("xml", "lang"))
                        if language is not None:
                            if language in rc_keywords:
                                rc_keywords[language].append(value)
                            else:
                                rc_keywords[language] = [value]
                    else:
                        rc_classification = {"term": value}
                        authority = rml_rc.get("authority")
                        authority_id = rml_rc.get("authorityId")
                        term_id = rml_rc.get("id")
                        if authority is not None:
                            rc_classification["authority"] = authority.strip()
                        if authority_id is not None:
                            rc_classification["authority_id"] = authority_id.strip()
                        if term_id is not None:
                            rc_classification["term_id"] = term_id.strip()
                        rc_classifications.append(rc_classification)
        if rc_classifications:
            result["research_coverage_classifications"] = rc_classifications
        if rc_keywords:
            result["research_coverage_keywords"] = rc_keywords
    return result


def extract_rml_teachings(rml):
    result = {}
    rml_teachings = rml.findall(prefixtag("rml", "teaching"))
    if rml_teachings is not None:
        teachings = []
        for rml_teaching in rml_teachings:
            if rml_teaching is not None:
                teaching = {}

                # level
                teaching.update(extract_element_and_set_key(rml_teaching, "level", "level"))

                # title
                teaching.update(extract_element_and_set_key(rml_teaching, "title", "title"))

                # identifier
                teaching.update(extract_rml_identifiers(rml_teaching))

                # name
                teaching.update(extract_element_and_set_key(rml_teaching, "name", "name"))

                # date_start
                teaching.update(extract_element_and_set_key(rml_teaching, "dateBegin", "date_start"))

                # date_end
                teaching.update(extract_element_and_set_key(rml_teaching, "dateEnd", "date_end"))

                # descriptions
                teaching.update(extract_rml_string_lang(rml_teaching, "description", "descriptions"))

                if teaching is not None:
                    teachings.append(teaching)
        if teachings:
            result["teachings"] = teachings
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


def extract_rml_turnovers(rml):
    result = {}
    rml_turnovers = rml.findall(prefixtag("rml", "turnover"))
    if rml_turnovers is not None:
        turnovers = []
        for rml_turnover in rml_turnovers:
            if rml_turnover is not None:
                turnover = {}

                turnover.update(extract_attribute_and_set_key(rml_turnover, "currency", "currency"))
                turnover.update(extract_attribute_and_set_key(rml_turnover, "year", "year"))
                turnover["value"] = get_text_or_none(rml_turnover)

                if turnover:
                    turnovers.append(turnover)
        if turnovers:
            result["turnovers"] = turnovers
    return result


def extract_rml_uris(rml):
    result = {}
    rml_uris = rml.findall(prefixtag("rml", "uri"))
    if rml_uris is not None:
        uris = []
        for rml_uri in rml_uris:
            if rml_uri is not None:
                preferred = get_attribute_boolean(rml_uri, "preferred")
                relation_type = rml_uri.get("relationType")
                visible = get_attribute_boolean(rml_uri, "visible")
                value = get_text_or_none(rml_uri)

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


def extract_attribute_and_set_key(rml, attribute, key):
    result = {}
    att_value = rml.get(attribute)
    if att_value is not None:
        result[key] = att_value
    return result


def extract_boolean_attribute_and_set_key(rml, attribute, key):
    result = {}
    att_value = get_attribute_boolean(rml, attribute)
    if att_value:
        result[key] = att_value
    return result


def extract_element_and_set_key(rml, element, key):
    result = {}
    element_xmletree = rml.find(prefixtag("rml", element))
    key_value = get_text_or_none(element_xmletree)
    if key_value is not None:
        result[key] = key_value
    return result


def get_text_or_none(element):
    if element is not None and element.text is not None:
        result = element.text.strip()
    else:
        result = None
    return result


def get_boolean(element):
    if element is not None and element.text is not None and element.text.strip() == "true":
        return True
    else:
        return False


def get_attribute_boolean(element, attribute):
    if element is not None and attribute is not None:
        att_val = element.get(attribute)
        if att_val is not None and att_val == "true":
            return True
    return False


