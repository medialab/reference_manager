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
            if child.tag.endswith("person"):
                yield rml_person_to_metajson(child, source)
            elif child.tag.endswith("orgunit"):
                yield rml_orgunit_to_metajson(child, source)
            elif child.tag.endswith("orgunit"):
                yield rml_project_to_metajson(child, source)


def rml_person_to_metajson(rml_person, source):
    person = Person()
    return person


def rml_orgunit_to_metajson(rml_orgunit, source):
    orgunit = Orgunit()
    return orgunit


def rml_project_to_metajson(rml_project, source):
    project = Project()
    return project
