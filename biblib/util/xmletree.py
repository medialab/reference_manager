#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import QName

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

def get_element_text(element):
    if element is not None:
        element_text = element.text
        if element_text:
            element_text = element_text.strip()
        if element_text:
            return element_text
    return None


def get_element_text_as_boolean(element):
    if element is not None:
        element_text = element.text
        if element_text:
            element_text = element_text.strip()
            if element_text == "true":
                return True
    return False


def get_element_attribute(element, attribute):
    if element is not None and attribute is not None:
        element_attribute = element.get(attribute)
        if element_attribute:
            element_attribute = element_attribute.strip()
        if element_attribute:
            return element_attribute
    return None


def get_element_attribute_as_boolean_and_set_key(element, attribute, key):
    result = {}
    att_value = get_element_attribute_as_boolean(element, attribute)
    if att_value:
        result[key] = att_value
    return result


def get_element_attribute_as_boolean(element, attribute):
    if element is not None and attribute is not None:
        att_val = element.get(attribute)
        if att_val is not None and att_val == "true":
            return True
    return False


def get_element_attribute_and_set_key(rml, attribute, key):
    result = {}
    att_value = rml.get(attribute)
    if att_value is not None:
        result[key] = att_value
    return result
