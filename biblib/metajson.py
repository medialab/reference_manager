#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

rec_metajson = 1

STYLE_GIVEN_FAMILY = "given_family"
STYLE_FAMILY_COMMA_GIVEN = "family_comma_given"


# Common
class Common(dict):
    def set_key_if_not_none(self, key, value):
        if value:
            self[key] = value

    def set_key_with_value_type_in_list(self, key, value, my_type):
        if value:
            tmp = {"type": my_type, "value": value}
            try:
                self[key].append(tmp)
            except:
                self[key] = [tmp]

    def set_key_with_value_language_in_list(self, key, value, language):
        if value:
            tmp = {"language": language, "value": value}
            try:
                self[key].append(tmp)
            except:
                self[key] = [tmp]

    def add_items_to_key(self, items, key):
        if items is not None and len(items) != 0:
            for item in items:
                self.add_item_to_key(item, key)

    def add_item_to_key(self, item, key):
        if item:
            try:
                self[key].append(item)
            except:
                self[key] = [item]


# Collection
class Collection(Common):
    pass


# Contributor
class Contributor(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "agent" in self:
            agent = self["agent"]
            if agent and "rec_class" in agent:
                rec_class = agent["rec_class"]
                if "Person" == rec_class:
                    self["agent"] = Person(self["agent"])
                elif "Orgunit" == rec_class:
                    self["agent"] = Orgunit(self["agent"])
                elif "Event" == rec_class:
                    self["agent"] = Event(self["agent"])
                elif "Family" == rec_class:
                    self["agent"] = Family(self["agent"])

    def formatted_name(self, style=STYLE_FAMILY_COMMA_GIVEN):
        if "agent" in self:
            agent = self["agent"]
            if agent and "rec_class" in agent:
                rec_class = agent["rec_class"]
                if "Person" == rec_class:
                    return agent.formatted_name(style)
                elif "Orgunit" == rec_class:
                    return agent.formatted_name()
                elif "Event" == rec_class:
                    return agent.formatted_name()
                elif "Family" == rec_class:
                    return agent.formatted_name()


# Datafield
class Datafield(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Datafield"


# Document
class Document(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Document"
        if "contributors" in self:
            self["contributors"] = [Contributor(x) for x in self["contributors"]]
        if "is_part_of" in self:
            self["is_part_of"] = [Document(x) for x in self["is_part_of"]]
        if "resources" in self:
            self["resources"] = [Resource(x) for x in self["resources"]]

    def add_contributors(self, contributors):
        self.add_items_to_key(contributors, "contributors")

    def get_contributors_by_role(self, role):
        results = []
        if "contributors" in self:
            for contributor in self["contributors"]:
                if contributor["role"] == role:
                    results.append(contributor)
        return results

    def get_date(self):
        date = self.get_property_from_all_level("date_issued")
        if date is None:
            date = self.get_property_from_all_level("date_issued_first")
        if date is None:
            date = self.get_property_from_all_level("date_created")
        if date is None:
            date = self.get_property_from_all_level("date_defence")
        if date is None:
            date = self.get_property_from_all_level("date_captured")
        if date is None:
            date = self.get_property_from_all_level("date_accepted")
        if date is None:
            date = self.get_property_from_all_level("date_submitted")
        if date is None:
            date = self.get_property_from_all_level("date_available")
        if date is None:
            date = self.get_property_from_all_level("date_other")
        return date

    def get_edition(self):
        return self.get_property_from_all_level("edition")

    def get_extent_pages(self):
        return self.get_property_from_all_level("extent_pages")

    def get_extent_volumes(self):
        return self.get_property_from_all_level("extent_volumes")

    def get_part_issue(self):
        return self.get_property_from_all_level("part_issue")

    def get_part_name(self):
        return self.get_property_from_all_level("part_name")

    def get_part_page_start(self):
        return self.get_property_from_all_level("part_page_start")

    def get_part_page_end(self):
        return self.get_property_from_all_level("part_page_end")

    def get_part_volume(self):
        return self.get_property_from_all_level("part_volume")

    def get_publisher(self):
        return self.get_property_from_all_level("publisher")

    def get_publisher_country(self):
        return self.get_property_from_all_level("publisher_country")

    def get_publisher_place(self):
        return self.get_property_from_all_level("publisher_place")

    def get_series_title(self):
        return self.get_property_in_object_from_all_level("series", "title")

    def get_type_degree(self):
        return self.get_property_from_all_level("type_degree")

    def get_property_from_all_level(self, my_property):
        if my_property in self and self[my_property]:
            return self[my_property]
        if "is_part_of" in self:
            if my_property in self["is_part_of"][0] and self["is_part_of"][0][my_property]:
                return self["is_part_of"][0][my_property]
            if "is_part_of" in self["is_part_of"][0] and my_property in self["is_part_of"][0]["is_part_of"][0] and self["is_part_of"][0]["is_part_of"][0][my_property]:
                return self["is_part_of"][0]["is_part_of"][0][my_property]

    def get_property_in_object_from_all_level(self, my_object, my_property):
        if my_object in self and my_property in self[my_object] and self[my_object][my_property]:
            return self[my_object][my_property]
        if "is_part_of" in self:
            if my_object in self["is_part_of"][0] and my_property in self["is_part_of"][0][my_object] and self["is_part_of"][0][my_object][my_property]:
                return self["is_part_of"][0][my_object][my_property]
            if "is_part_of" in self["is_part_of"][0] and my_object in self["is_part_of"][0]["is_part_of"][0] and my_property in self["is_part_of"][0]["is_part_of"][0][my_object] and self["is_part_of"]["is_part_of"][my_object][my_property]:
                return self["is_part_of"][0]["is_part_of"][0][my_object][my_property]

    def get_first_value_for_type_in_list_from_all_level(self, my_list, my_type):
        if my_list in self:
            my_value = self.get_first_value_for_type_in_list(self[my_list], my_type)
            if my_value:
                return my_value
        if "is_part_of" in self:
            if my_list in self["is_part_of"][0]:
                my_value = self.get_first_value_for_type_in_list(self["is_part_of"][0][my_list], my_type)
                if my_value:
                    return my_value
            if "is_part_of" in self["is_part_of"][0] and my_list in self["is_part_of"][0]["is_part_of"][0]:
                my_value = self.get_first_value_for_type_in_list(self["is_part_of"][0]["is_part_of"][0][my_list], my_type)
                if my_value:
                    return my_value

    def get_first_value_for_type_in_list(self, my_list, my_type):
        if len(my_list) > 0:
            for item in my_list:
                    if "type" in item and "value" in item and item["value"]:
                        if item["type"] == my_type:
                            return item["value"]

    def get_property_for_item_in_list(self, my_list, my_property):
        if len(my_list) > 0:
            for item in my_list:
                if my_property in item and item[my_property]:
                    return item[my_property]


# DocumentUi
class DocumentUi(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "DocumentUi"


# Event
class Event(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Event"

    def formatted_name(self):
        if "title" in self:
            return self["title"]


# Family
class Family(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Family"

    def formatted_name(self):
        if "name_family" in self:
            return self["name_family"]


# Identifier
class Identifier(Common):
    pass


# Identifier util
# todo : move it to the Identifier constructor
def create_identifier(id_type, id_value):
    if id_value:
        identifier = Identifier()
        identifier["value"] = id_value
        if id_type:
            identifier["type"] = id_type
        return identifier


# Orgunit
class Orgunit(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Orgunit"

    def formatted_name(self):
        if "name" in self:
            return self["name"]


# Person
class Person(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Person"

    def formatted_name(self, style=STYLE_FAMILY_COMMA_GIVEN):
        result = ""
        if style == STYLE_FAMILY_COMMA_GIVEN:
            if "name_family" in self and self["name_family"]:
                result += self["name_family"]
            if "name_given" in self and self["name_given"]:
                result += ", " + self["name_given"]
        else:
            if "name_given" in self and self["name_given"]:
                result += self["name_given"] + " "
            if "name_family" in self and self["name_family"]:
                result += self["name_family"]
        return result


# Resource
class Resource(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Resource"


# Rights
class Rights(Common):
    pass


# Subject
class Subject(Common):
    pass


# Target
class Target(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Target"


# Type
class Type(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Type"


# Warpper
class Warpper(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "rec_metajson" not in self:
            self["rec_metajson"] = rec_metajson
        if "rec_class" not in self:
            self["rec_class"] = "Warpper"
