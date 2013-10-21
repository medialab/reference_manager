#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Call
from biblib.metajson import Creator
from biblib.metajson import Family
from biblib.metajson import Orgunit
from biblib.metajson import Person
from biblib.metajson import Project
from biblib.services import creator_service
from biblib.services import language_service
from biblib.services import metajson_service
from biblib.util import constants
from biblib.util import xmletree


def researcherml_xmletree_to_metajson_list(rml_root, source, only_first_record):
    """ researcherml (xmletree) -> metajson_list """
    if rml_root is not None:
        for child in rml_root:
            # person -> person
            if child.tag.endswith("person"):
                yield rml_person_to_metajson(child, source)

            # orgUnit -> orgunit
            elif child.tag.endswith("orgUnit"):
                yield rml_orgunit_to_metajson(child, source)

            # project -> project
            elif child.tag.endswith("project"):
                yield rml_project_to_metajson(child, source)


def rml_orgunit_to_metajson(rml_orgunit, source):
    """ orgUnit -> orgunit """
    orgunit = Orgunit()

    # acronym -> acronym
    orgunit.update(get_rml_element_text_and_set_key(rml_orgunit, "acronym", "acronym"))

    # address -> addresses
    orgunit.update(get_rml_addresses(rml_orgunit))

    # affiliation -> affiliations
    orgunit.update(get_rml_affiliations(rml_orgunit))

    # award -> awards
    orgunit.update(get_rml_textlangs_and_set_key(rml_orgunit, "award", "awards"))

    # ckbData -> self_archiving_policy
    orgunit.update(get_rml_self_ckbdatas(rml_orgunit))

    # dateOfDissolution -> date_dissolution
    orgunit.update(get_rml_element_text_and_set_key(rml_orgunit, "dateOfDissolution", "date_dissolution"))

    # dateOfFoundation -> date_foundation
    orgunit.update(get_rml_element_text_and_set_key(rml_orgunit, "dateOfFoundation", "date_foundation"))

    # description -> descriptions
    orgunit.update(get_rml_textlangs_and_set_key(rml_orgunit, "description", "descriptions"))

    # email -> emails
    orgunit.update(get_rml_emails(rml_orgunit))

    # headcount -> headcounts
    orgunit.update(get_rml_headcounts(rml_orgunit))

    # identifier -> identifiers
    orgunit.update(get_rml_identifiers(rml_orgunit))

    # image -> image_urls
    orgunit.update(get_rml_images(rml_orgunit))

    # name -> name
    orgunit.update(get_rml_element_text_and_set_key(rml_orgunit, "name", "name"))

    # nameAlternative -> name_alternatives
    orgunit.update(get_rml_textlangs_and_set_key(rml_orgunit, "nameAlternative", "name_alternatives"))

    # nationality -> nationality
    orgunit.update(get_rml_element_text_and_set_key(rml_orgunit, "nationality", "nationality"))

    # note -> notes
    orgunit.update(get_rml_textlangs_and_set_key(rml_orgunit, "note", "notes"))

    # olDescription -> descriptions_short
    orgunit.update(get_rml_textlangs_and_set_key(rml_orgunit, "olDescription", "descriptions_short"))

    # ongoingResearch -> ongoing_researches
    orgunit.update(get_rml_ongoing_researches(rml_orgunit))

    # phone -> phones
    orgunit.update(get_rml_phones(rml_orgunit))

    # researchCoverage -> research_coverages
    orgunit.update(get_rml_research_coverages(rml_orgunit))

    # skill -> skills
    orgunit.update(get_rml_textlangs_and_set_key(rml_orgunit, "skill", "skills"))

    # turnover -> turnovers
    orgunit.update(get_rml_turnovers(rml_orgunit))

    # @type -> rec_type
    orgunit.update(xmletree.get_element_attribute_and_set_key(rml_orgunit, "type", "rec_type"))

    # uri -> urls
    orgunit.update(get_rml_uris(rml_orgunit))

    return orgunit


def rml_person_to_metajson(rml_person, source):
    """ person -> person """
    person = Person()

    # academicTitle, honorificTitle -> titles
    person.update(get_rml_titles(rml_person))

    # affiliation -> affiliations
    person.update(get_rml_affiliations(rml_person))

    # address -> addresses
    person.update(get_rml_addresses(rml_person))

    # award -> awards
    person.update(get_rml_textlangs_and_set_key(rml_person, "award", "awards"))

    # biography -> biographies
    person.update(get_rml_textlangs_and_set_key(rml_person, "biography", "biographies"))

    # dateOfBirth -> date_birth
    person.update(get_rml_element_text_and_set_key(rml_person, "dateOfBirth", "date_birth"))

    # dateOfDeath -> date_death
    person.update(get_rml_element_text_and_set_key(rml_person, "dateOfDeath", "date_death"))

    # degree -> degrees
    person.update(get_rml_degrees(rml_person))

    # email -> emails
    person.update(get_rml_emails(rml_person))

    # fictitious -> fictitious
    person.update(xmletree.get_element_attribute_as_boolean_and_set_key(rml_person, "fictitious", "fictitious"))

    # firstname -> name_given
    person.update(get_rml_element_text_and_set_key(rml_person, "firstname", "name_given"))

    # identifier -> identifiers
    person.update(get_rml_identifiers(rml_person))

    # image -> image_urls
    person.update(get_rml_images(rml_person))

    # instantMessage -> instant_messages
    person.update(get_rml_instant_messages(rml_person))

    # languageCapability -> language_capabilities
    person.update(get_rml_language_capabilities(rml_person))

    # lastname -> name_family
    person.update(get_rml_element_text_and_set_key(rml_person, "lastname", "name_family"))

    # lastnamePrefix -> name_prefix
    person.update(get_rml_element_text_and_set_key(rml_person, "lastnamePrefix", "name_prefix"))

    # lastnameSuffix -> name_suffix
    person.update(get_rml_element_text_and_set_key(rml_person, "lastnameSuffix", "name_suffix"))

    # middlename -> name_middle
    person.update(get_rml_element_text_and_set_key(rml_person, "middlename", "name_middle"))

    # nationality -> nationality
    person.update(get_rml_element_text_and_set_key(rml_person, "nationality", "nationality"))

    # nickname -> name_nick
    person.update(get_rml_element_text_and_set_key(rml_person, "nickname", "name_nick"))

    # note -> notes
    person.update(get_rml_textlangs_and_set_key(rml_person, "note", "notes"))

    # olBiography -> biographies_short
    person.update(get_rml_textlangs_and_set_key(rml_person, "olBiography", "biographies_short"))

    # ongoingResearch -> ongoing_researches
    person.update(get_rml_ongoing_researches(rml_person))

    # phone -> phones
    person.update(get_rml_phones(rml_person))

    # relationship -> relationships
    person.update(get_rml_relationships(rml_person))

    # researchCoverage -> research_coverages
    person.update(get_rml_research_coverages(rml_person))

    # responsability -> responsabilities
    person.update(get_rml_textlangs_and_set_key(rml_person, "responsability", "responsabilities"))

    # sex -> gender
    person.update(get_rml_element_text_and_set_key(rml_person, "sex", "gender"))

    # skill -> skills
    person.update(get_rml_textlangs_and_set_key(rml_person, "skill", "skills"))

    # teaching -> teachings
    person.update(get_rml_teachings(rml_person))

    # uri -> urls
    person.update(get_rml_uris(rml_person))

    return person


def rml_project_to_metajson(rml_project, source):
    """ project -> project """
    project = Project()

    # acronym -> acronym
    project.update(get_rml_element_text_and_set_key(rml_project, "acronym", "acronym"))

    # award -> awards
    project.update(get_rml_textlangs_and_set_key(rml_project, "award", "awards"))

    # call -> call
    project.update(get_rml_call(rml_project))
    
    # contribution -> budget_contribution
    project.update(get_rml_money_and_set_key(rml_project, "contribution", "budget_contribution"))

    # cost -> budget_cost
    project.update(get_rml_money_and_set_key(rml_project, "cost", "budget_cost"))

    # dateBegin -> date_begin
    project.update(get_rml_element_text_and_set_key(rml_project, "dateBegin", "date_begin"))

    # dateEnd -> date_end
    project.update(get_rml_element_text_and_set_key(rml_project, "dateEnd", "date_end"))

    # description -> descriptions
    project.update(get_rml_textlangs_and_set_key(rml_project, "description", "descriptions"))

    # duration -> extent_duration
    project.update(get_rml_element_text_and_set_key(rml_project, "duration", "extent_duration"))

    # identifier -> identifiers
    project.update(get_rml_identifiers(rml_project))

    # note -> notes
    project.update(get_rml_textlangs_and_set_key(rml_project, "note", "notes"))

    # olDescription -> descriptions_short
    project.update(get_rml_textlangs_and_set_key(rml_project, "olDescription", "descriptions_short"))

    # participant -> creators
    project.update(get_rml_participants(rml_project))

    # researchCoverage -> research_coverage_classifications & esearch_coverage_keywords
    project.update(get_rml_research_coverages(rml_project))

    # status -> status
    project.update(get_rml_element_text_and_set_key(rml_project, "status", "status"))

    # title -> title
    project.update(get_rml_element_text_and_set_key(rml_project, "title", "title"))

    # titleAlternative -> title_alternatives
    project.update(get_rml_textlangs_and_set_key(rml_project, "titleAlternative", "title_alternatives"))

    # uri -> urls
    project.update(get_rml_uris(rml_project))

    return project


def get_rml_addresses(rml):
    """ address -> addresses """
    result = {}
    rml_addresses = rml.findall(xmletree.prefixtag("rml", "address"))
    if rml_addresses is not None:
        addresses = []
        for rml_address in rml_addresses:
            if rml_address is not None:
                # @preferred -> preferred
                preferred = xmletree.get_element_attribute_as_boolean(rml_address, "preferred")

                # relationType -> relation_type
                relation_type = rml_address.get("relationType")

                # visible -> visible
                visible = xmletree.get_element_attribute_as_boolean(rml_address, "visible")

                # street -> street
                street = xmletree.get_element_text(rml_address.find(xmletree.prefixtag("rml", "street")))

                # post_code -> post_code
                post_code = xmletree.get_element_text(rml_address.find(xmletree.prefixtag("rml", "postCode")))

                # locality_city_town -> locality_city_town
                locality_city_town = xmletree.get_element_text(rml_address.find(xmletree.prefixtag("rml", "localityCityTown")))

                # country -> country
                country = xmletree.get_element_text(rml_address.find(xmletree.prefixtag("rml", "country")))

                # address -> addresses[i]
                address = metajson_service.create_address(street, post_code, locality_city_town, country, preferred, relation_type, visible)

                if address:
                    addresses.append(address)
        if addresses:
            result["addresses"] = addresses
    return result


def get_rml_affiliations(rml):
    """ affiliation -> affiliations """
    result = {}
    rml_affiliations = rml.findall(xmletree.prefixtag("rml", "affiliation"))
    if rml_affiliations is not None:
        affiliations = []
        for rml_affiliation in rml_affiliations:
            if rml_affiliation is not None:
                # @preferred -> preferred
                preferred = xmletree.get_element_attribute_as_boolean(rml_affiliation, "preferred")

                # dateBegin -> date_begin
                rml_date_begin = rml_affiliation.find(xmletree.prefixtag("rml", "dateBegin"))
                date_begin = xmletree.get_element_text(rml_date_begin)

                # dateEnd -> date_end
                rml_date_end = rml_affiliation.find(xmletree.prefixtag("rml", "dateEnd"))
                date_end = xmletree.get_element_text(rml_date_end)

                # identifier -> identifiers
                identifiers = get_rml_identifiers(rml_affiliation)
                rec_id = None
                if "identifiers" in identifiers and identifiers["identifiers"]:
                    rec_id = identifiers["identifiers"][0]["value"]

                # name -> name
                rml_name = rml_affiliation.find(xmletree.prefixtag("rml", "name"))
                name = xmletree.get_element_text(rml_name)

                # relationType -> role
                rml_relation_type = rml_affiliation.find(xmletree.prefixtag("rml", "relationType"))
                role = xmletree.get_element_text(rml_relation_type)

                affiliation = metajson_service.create_affiliation(rec_id, name, role, date_begin, date_end, preferred)
                if affiliation is not None:
                    affiliations.append(affiliation)
        if affiliations:
            result["affiliations"] = affiliations
    return result


def get_rml_call(rml):
    """ call -> call """
    result = {}
    rml_call = rml.find(xmletree.prefixtag("rml", "call"))
    if rml_call is not None:
        call = Call()

        # funding -> funding
        rml_funding = rml_call.find(xmletree.prefixtag("rml", "funding"))
        if rml_funding is not None:
            funding = Orgunit()

            # identifier -> rec_id
            funding.update(get_rml_element_text_and_set_key(rml_funding, "identifier", "rec_id"))

            # name -> name
            funding.update(get_rml_element_text_and_set_key(rml_funding, "name", "name"))

            # programme -> programme
            funding.update(get_rml_element_text_and_set_key(rml_funding, "programme", "programme"))

            # scheme -> scheme
            funding.update(get_rml_element_text_and_set_key(rml_funding, "scheme", "scheme"))

            # contribution -> budget_contribution
            funding.update(get_rml_money_and_set_key(rml_funding, "contribution", "budget_contribution"))

            if funding:
                call["funding"] = funding

        # identifier -> rec_id
        call.update(get_rml_element_text_and_set_key(rml_call, "identifier", "rec_id"))

        # title -> title
        call.update(get_rml_element_text_and_set_key(rml_call, "title", "title"))

        # year -> date_issued
        call.update(get_rml_element_text_and_set_key(rml_call, "year", "date_issued"))

        if call:
            result["call"] = call
    return result


def get_rml_degrees(rml):
    """ degree -> degrees """
    result = {}
    rml_degrees = rml.findall(xmletree.prefixtag("rml", "degree"))
    if rml_degrees is not None:
        degrees = []
        for rml_degree in rml_degrees:
            if rml_degree is not None:
                degree = {}

                # date_begin
                degree.update(get_rml_element_text_and_set_key(rml_degree, "dateBegin", "date_begin"))

                # date_end
                degree.update(get_rml_element_text_and_set_key(rml_degree, "dateEnd", "date_end"))

                # descriptions
                degree.update(get_rml_textlangs_and_set_key(rml_degree, "description", "descriptions"))

                # identifiers
                degree.update(get_rml_identifiers(rml_degree))

                # level
                degree.update(get_rml_element_text_and_set_key(rml_degree, "level", "level"))

                # name
                degree.update(get_rml_element_text_and_set_key(rml_degree, "name", "name"))

                # title
                degree.update(get_rml_element_text_and_set_key(rml_degree, "title", "title"))

                if degree is not None:
                    degrees.append(degree)
        if degrees:
            result["degrees"] = degrees
    return result


def get_rml_emails(rml):
    """ email -> emails """
    result = {}
    rml_emails = rml.findall(xmletree.prefixtag("rml", "email"))
    if rml_emails is not None:
        emails = []
        for rml_email in rml_emails:
            if rml_email is not None:
                preferred = xmletree.get_element_attribute_as_boolean(rml_email, "preferred")
                relation_type = rml_email.get("relationType")
                visible = xmletree.get_element_attribute_as_boolean(rml_email, "visible")
                value = xmletree.get_element_text(rml_email)

                email = metajson_service.create_email(value, preferred, relation_type, visible)
                if email:
                    emails.append(email)
        if emails:
            result["emails"] = emails
    return result


def get_rml_headcounts(rml):
    """ headcount -> headcounts """
    result = {}
    rml_headcounts = rml.findall(xmletree.prefixtag("rml", "headcount"))
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


def get_rml_identifiers(rml):
    """ identifier -> identifiers """
    result = {}
    rml_identifiers = rml.findall(xmletree.prefixtag("rml", "identifier"))
    if rml_identifiers is not None:
        identifiers = []
        for rml_identifier in rml_identifiers:
            if rml_identifier is not None:
                id_type = rml_identifier.get("type")
                id_value = xmletree.get_element_text(rml_identifier)
                identifier = metajson_service.create_identifier(id_type, id_value)
                if identifier is not None:
                    identifiers.append(identifier)
        if identifiers:
            result["identifiers"] = identifiers
    return result


def get_rml_images(rml):
    # todo resources
    """ image -> image_urls """
    result = {}
    rml_images = rml.findall(xmletree.prefixtag("rml", "image"))
    if rml_images is not None:
        images = []
        for rml_image in rml_images:
            if rml_image is not None:
                url = xmletree.get_element_text(rml_image)
                image = metajson_service.create_image_url(url)
                if image is not None:
                    images.append(image)
        if images:
            result["image_urls"] = images
            # todo : metajson
    return result


def get_rml_instant_messages(rml):
    """ instantMessage -> instant_messages """
    result = {}
    rml_ims = rml.findall(xmletree.prefixtag("rml", "instantMessage"))
    if rml_ims is not None:
        ims = []
        for rml_im in rml_ims:
            if rml_im is not None:
                preferred = xmletree.get_element_attribute_as_boolean(rml_im, "preferred")
                relation_type = rml_im.get("relationType")
                visible = xmletree.get_element_attribute_as_boolean(rml_im, "visible")
                service = rml_im.get("service")
                value = xmletree.get_element_text(rml_im)

                im = metajson_service.create_instant_message(value, service, preferred, relation_type, visible)
                if im:
                    ims.append(im)
        if ims:
            result["instant_messages"] = ims
    return result


def get_rml_language_capabilities(rml):
    """ languageCapability -> language_capabilities """
    result = {}
    rml_lcs = rml.findall(xmletree.prefixtag("rml", "languageCapability"))
    if rml_lcs is not None:
        lcs = []
        for rml_lc in rml_lcs:
            if rml_lc is not None:
                # language
                rml_language = rml_lc.find(xmletree.prefixtag("rml", "language"))
                language = xmletree.get_element_text(rml_language)

                # motherTong
                rml_mother_tong = rml_lc.find(xmletree.prefixtag("rml", "motherTong"))
                mother_tong = xmletree.get_element_text_as_boolean(rml_mother_tong)

                # oralInput
                rml_oral_input = rml_lc.find(xmletree.prefixtag("rml", "oralInput"))
                oral_input = xmletree.get_element_text(rml_oral_input)

                # oralOutput
                rml_oral_output = rml_lc.find(xmletree.prefixtag("rml", "oralOutput"))
                oral_output = xmletree.get_element_text(rml_oral_output)

                # textInput
                rml_text_input = rml_lc.find(xmletree.prefixtag("rml", "textInput"))
                text_input = xmletree.get_element_text(rml_text_input)

                # textOutput
                rml_text_output = rml_lc.find(xmletree.prefixtag("rml", "textOutput"))
                text_output = xmletree.get_element_text(rml_text_output)

                lc = metajson_service.create_language_capability(language, mother_tong, oral_input, oral_output, text_input, text_output)
                if lc is not None:
                    lcs.append(lc)
        if lcs:
            result["language_capabilities"] = lcs
    return result


def get_rml_money_and_set_key(rml, element, key):
    """ element -> key """
    result = {}
    rml_element = rml.find(xmletree.prefixtag("rml", element))
    if rml_element is not None:
        money = {}

        # currency -> currency
        money.update(xmletree.get_element_attribute_and_set_key(rml_element, "currency", "currency"))

        # text -> value
        money["value"] = xmletree.get_element_text(rml_element)

        if money:
            result[key] = money
    return result


def get_rml_ongoing_researches(rml):
    """ ongoingResearch -> ongoing_researches """
    result = {}
    rml_ongoing_researches = rml.findall(xmletree.prefixtag("rml", "ongoingResearch"))
    if rml_ongoing_researches is not None:
        ongoing_researches = []
        for rml_ongoing_research in rml_ongoing_researches:
            if rml_ongoing_research is not None:
                ongoing_research = {}

                # descriptions
                ongoing_research.update(get_rml_textlangs_and_set_key(rml_ongoing_research, "description", "descriptions"))

                if ongoing_research is not None:
                    ongoing_researches.append(ongoing_research)
        if ongoing_researches:
            result["ongoing_researches"] = ongoing_researches
    return result


def get_rml_participants(rml):
    """ participant -> creators """
    result = {}
    rml_participants = rml.findall(xmletree.prefixtag("rml", "participant"))
    if rml_participants is not None:
        creators = []
        for rml_participant in rml_participants:
            if rml_participant is not None:
                creator_name = get_rml_element_text(rml_participant, "name")
                if creator_name:
                    creator_rec_class = xmletree.get_element_attribute(rml_participant, "entityType")
                    if creator_rec_class:
                        creator_rec_class = creator_rec_class.lower()
                    creator = creator_service.formatted_name_to_creator(creator_name, creator_rec_class, None)
                    if creator:
                        creators.append(creator)
        if creators:
            result["creators"] = creators
    return result


def get_rml_phones(rml):
    """ phone -> phones """
    result = {}
    rml_phones = rml.findall(xmletree.prefixtag("rml", "phone"))
    if rml_phones is not None:
        phones = []
        for rml_phone in rml_phones:
            if rml_phone is not None:
                preferred = xmletree.get_element_attribute_as_boolean(rml_phone, "preferred")
                relation_type = rml_phone.get("relationType")
                phone_type = rml_phone.get("type")
                visible = xmletree.get_element_attribute_as_boolean(rml_phone, "visible")
                rml_formatted = rml_phone.find(xmletree.prefixtag("rml", "formatted"))
                formatted = xmletree.get_element_text(rml_formatted)

                phone = metajson_service.create_phone(formatted, phone_type, preferred, relation_type, visible)
                if phone:
                    phones.append(phone)
        if phones:
            result["phones"] = phones
    return result


def get_rml_relationships(rml):
    """ relationship -> relationships """
    result = {}
    rml_relationships = rml.findall(xmletree.prefixtag("rml", "relationship"))
    if rml_relationships is not None:
        relationships = []
        for rml_relationship in rml_relationships:
            if rml_relationship is not None:
                relationship = {}

                # relation_type
                relationship.update(get_rml_element_text_and_set_key(rml_relationship, "relationType", "relation_type"))

                # identifiers
                relationship.update(get_rml_identifiers(rml_relationship))

                # name
                relationship.update(get_rml_element_text_and_set_key(rml_relationship, "name", "name"))

                # descriptions
                relationship.update(get_rml_textlangs_and_set_key(rml_relationship, "description", "descriptions"))

                if relationship is not None:
                    relationships.append(relationship)
        if relationships:
            result["relationships"] = relationships
    return result


def get_rml_research_coverages(rml):
    """ researchCoverage -> research_coverage_classifications & esearch_coverage_keywords """
    result = {}
    rml_rcs = rml.findall(xmletree.prefixtag("rml", "researchCoverage"))
    if rml_rcs is not None:
        rc_classifications = []
        rc_keywords = {}
        for rml_rc in rml_rcs:
            if rml_rc is not None:
                value = rml_rc.text.strip()
                if value is not None:
                    rc_type = rml_rc.get("type")
                    if rc_type == "keyword":
                        language = rml_rc.get(xmletree.prefixtag("xml", "lang"))
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


def get_rml_self_ckbdatas(rml):
    """ ckbData -> self_archiving_policy """
    result = {}
    rml_ckbdata = rml.find(xmletree.prefixtag("rml", "ckbData"))
    if rml_ckbdata is not None:

        sap = {}
        # romeo
        rml_romeo = rml_ckbdata.find(xmletree.prefixtag("rml", "romeoPublisher"))
        if rml_romeo is not None:
            # publisher
            #sap_publisher = Orgunit()
            #sap_publisher["rec_type"] = "publisher"

            # alias -> acronym
            #sap_publisher.update(get_rml_element_text_and_set_key(rml_romeo, "alias", "alias"))

            # homeurl -> url
            #rml_homeurl_value = xmletree.get_element_text(rml_romeo.find(xmletree.prefixtag("rml", "homeurl")))
            #if rml_homeurl_value:
            #    sap_publisher["urls"] = [metajson_service.create_url(rml_homeurl_value, True, "work", None, None, True)]

            # id -> identifiers[i]
            #rml_id_value = xmletree.get_element_text(rml_romeo.find(xmletree.prefixtag("rml", "id")))
            #if rml_id_value:
            #    sap_publisher["identifiers"] = [metajson_service.create_identifier("romeo", rml_id_value)]

            # name -> name
            #sap_publisher.update(get_rml_element_text_and_set_key(rml_romeo, "name", "name"))

            #sap["publisher"] = sap_publisher

            # conditions -> conditions
            rml_conditions = rml_romeo.find(xmletree.prefixtag("rml", "conditions"))
            if rml_conditions is not None:
                rml_conditions_list = rml_conditions.findall(xmletree.prefixtag("rml", "condition"))
                if rml_conditions_list is not None:
                    conditions = []
                    for rml_condition in rml_conditions_list:
                        value = xmletree.get_element_text(rml_condition)
                        if value:
                            conditions.append(value)
                    if conditions:
                        sap["conditions"] = conditions

            # copyright -> copyright
            sap.update(get_rml_element_text_and_set_key(rml_romeo, "copyright", "copyright"))

            # copyrightlinks -> copyright_urls
            rml_copyrightlinks = rml_romeo.find(xmletree.prefixtag("rml", "copyrightlinks"))
            if rml_copyrightlinks is not None:
                rml_copyrightlinks_list = rml_copyrightlinks.findall(xmletree.prefixtag("rml", "copyrightlink"))
                if rml_copyrightlinks_list is not None:
                    copyright_urls = []
                    for rml_copyrightlink in rml_copyrightlinks_list:
                        copyrightlinktext = xmletree.get_element_text(rml_copyrightlink.find(xmletree.prefixtag("rml", "copyrightlinktext")))
                        copyrightlinkurl = xmletree.get_element_text(rml_copyrightlink.find(xmletree.prefixtag("rml", "copyrightlinkurl")))
                        copyright_url = metajson_service.create_url(copyrightlinkurl, None, None, copyrightlinktext, None, None)
                        copyright_urls.append(copyright_url)
                    if copyright_urls:
                        sap["copyright_urls"] = copyright_urls

            # paidaccess -> paid_access
            rml_paidaccess = rml_romeo.find(xmletree.prefixtag("rml", "paidaccess"))
            if rml_paidaccess is not None:
                paid_access = {}

                # paidaccessname -> label
                paid_access.update(get_rml_element_text_and_set_key(rml_paidaccess, "paidaccessname", "label"))

                # paidaccessurl -> url
                paid_access.update(get_rml_element_text_and_set_key(rml_paidaccess, "paidaccessurl", "url"))

                # paidaccessnotes -> notes
                # rml_paidaccessnotes = rml_paidaccess.findall(xmletree.prefixtag("rml", "paidaccessnotes"))

            # postprints -> postprint
            rml_postprints = rml_romeo.find(xmletree.prefixtag("rml", "postprints"))
            if rml_postprints is not None:
                postprint = {}

                # postarchiving -> possibility
                postprint.update(get_rml_element_text_and_set_key(rml_postprints, "postarchiving", "possibility"))

                # postrestrictions -> restrictions
                postprint.update(get_rml_textlangs_and_set_key(rml_postprints, "postrestrictions", "restrictions"))

                sap["postprint"] = postprint

            # preprints -> preprint
            rml_preprints = rml_romeo.find(xmletree.prefixtag("rml", "preprints"))
            if rml_preprints is not None:
                preprint = {}

                # prearchiving -> possibility
                preprint.update(get_rml_element_text_and_set_key(rml_preprints, "prearchiving", "possibility"))

                # prerestrictions -> restrictions
                preprint.update(get_rml_textlangs_and_set_key(rml_preprints, "prerestrictions", "pre_restrictions"))

                sap["preprint"] = preprint

            # romeocolour -> romeo_color
            sap.update(get_rml_element_text_and_set_key(rml_romeo, "romeocolour", "romeo_color"))

        if sap:
            result["self_archiving_policy"] = sap
    return result


def get_rml_teachings(rml):
    """ teaching -> teachings """
    result = {}
    rml_teachings = rml.findall(xmletree.prefixtag("rml", "teaching"))
    if rml_teachings is not None:
        teachings = []
        for rml_teaching in rml_teachings:
            if rml_teaching is not None:
                teaching = {}

                # level
                teaching.update(get_rml_element_text_and_set_key(rml_teaching, "level", "level"))

                # title
                teaching.update(get_rml_element_text_and_set_key(rml_teaching, "title", "title"))

                # identifiers
                teaching.update(get_rml_identifiers(rml_teaching))

                # name
                teaching.update(get_rml_element_text_and_set_key(rml_teaching, "name", "name"))

                # date_begin
                teaching.update(get_rml_element_text_and_set_key(rml_teaching, "dateBegin", "date_begin"))

                # date_end
                teaching.update(get_rml_element_text_and_set_key(rml_teaching, "dateEnd", "date_end"))

                # descriptions
                teaching.update(get_rml_textlangs_and_set_key(rml_teaching, "description", "descriptions"))

                if teaching is not None:
                    teachings.append(teaching)
        if teachings:
            result["teachings"] = teachings
    return result


def get_rml_titles(rml):
    """ academicTitle & honorificTitle -> titles """
    result = {}
    titles = []

    # academicTitle -> titles with title_type = "academic"
    result_academic = get_rml_textlangs_and_set_key(rml, "academicTitle", "titles")
    if "titles" in result_academic:
        for title in result_academic["titles"]:
            title["title_type"] = "academic"
            titles.append(title)

    # honorificTitle -> titles with title_type = "honorific"
    result_honorific = get_rml_textlangs_and_set_key(rml, "honorificTitle", "titles")
    if "titles" in result_honorific:
        for title in result_honorific["titles"]:
            title["title_type"] = "honorific"
            titles.append(title)

    if titles:
        result["titles"] = titles
    return result


def get_rml_turnovers(rml):
    """ turnover -> turnovers """
    result = {}
    rml_turnovers = rml.findall(xmletree.prefixtag("rml", "turnover"))
    if rml_turnovers is not None:
        turnovers = []
        for rml_turnover in rml_turnovers:
            if rml_turnover is not None:
                turnover = {}

                turnover.update(xmletree.get_element_attribute_and_set_key(rml_turnover, "currency", "currency"))
                turnover.update(xmletree.get_element_attribute_and_set_key(rml_turnover, "year", "year"))
                turnover["value"] = xmletree.get_element_text(rml_turnover)

                if turnover:
                    turnovers.append(turnover)
        if turnovers:
            result["turnovers"] = turnovers
    return result


def get_rml_uris(rml):
    """ uri -> urls """
    result = {}
    rml_uris = rml.findall(xmletree.prefixtag("rml", "uri"))
    if rml_uris is not None:
        urls = []
        for rml_uri in rml_uris:
            if rml_uri is not None:
                preferred = xmletree.get_element_attribute_as_boolean(rml_uri, "preferred")
                relation_type = rml_uri.get("relationType")
                visible = xmletree.get_element_attribute_as_boolean(rml_uri, "visible")
                value = xmletree.get_element_text(rml_uri)

                url = metajson_service.create_url(value, preferred, relation_type, None, None, visible)
                if url:
                    urls.append(url)
        if urls:
            result["urls"] = urls
    return result


def get_rml_textlangs_and_set_key(rml, element, key):
    """ element -> key
        @xml:lang -> language
        text -> value """
    result = {}
    rml_sls = rml.findall(xmletree.prefixtag("rml", element))
    if rml_sls is not None:
        sls = []
        for rml_sl in rml_sls:
            if rml_sl is not None and rml_sl.text is not None:
                language = rml_sl.get(xmletree.prefixtag("xml", "lang"))
                value = rml_sl.text.strip()
                if value is not None:
                    sl = {"value": value}
                    if language is not None:
                        sl["language"] = language.strip()
                    sls.append(sl)
        if sls:
            result[key] = sls
    return result


def get_rml_element_text(rml, element):
    element_xmletree = rml.find(xmletree.prefixtag("rml", element))
    return xmletree.get_element_text(element_xmletree)


def get_rml_element_text_and_set_key(rml, element, key):
    result = {}
    key_value = get_rml_element_text(rml, element)
    if key_value is not None:
        result[key] = key_value
    return result


def get_rml_elements_text(rml, element):
    elements_xmletree = rml.findall(xmletree.prefixtag("rml", element))
    if elements_xmletree is not None:
        results = []
        for element_xmletree in elements_xmletree:
            if element_xmletree is not None:
                results.append(xmletree.get_element_text(element_xmletree))
        if results:
            return results
    return None


def get_rml_elements_text_and_set_key(rml, element, key):
    result = {}
    values = get_rml_elements_text(rml, element)
    if values is not None:
        result[key] = values
    return result
