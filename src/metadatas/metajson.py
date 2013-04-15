#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

METAJSON_VERSION = 1

# Common
class Common(dict):
    def set_key_if_not_none(self, key, value):
        if value:
            self[key] = value

    def set_key_with_value_type_in_list(self, key, value, my_type):
        if value :
            tmp = {"type" : my_type, "value" : value}
            try :
                self[key].append(tmp)
            except :
                self[key] = [tmp]

    def set_key_with_value_language_in_list(self, key, value, language):
        if value :
            tmp = {"language" : language, "value" : value}
            try :
                self[key].append(tmp)
            except :
                self[key] = [tmp]

    def add_items_to_key(self, items, key):
        if items is not None and len(items) != 0 :
            for item in items :
                self.add_item_to_key(item, key)

    def add_item_to_key(self, item, key):
        if item :
            try :
                self[key].append(item)
            except :
                self[key] = [item]


# Document
class Document(Common):
    def __init__(self, *args, **kwargs):
        Common.__init__(self, *args, **kwargs)
        if "metajson_version" not in self:
            self["metajson_version"] = METAJSON_VERSION
        if "metajson_class" not in self:
            self["metajson_class"] = "Document"
        if "contributors" in self:
            tmp = [Contributor(x) for x in self["contributors"]]
            self["contributors"] = tmp

    def add_contributors(self,contributors):
        self.add_items_to_key(contributors,"contributors")

    def get_contributors_by_role(self, role):
        results=[]
        if "contributors" in self :
            for contributor in self["contributors"] :
                if contributor["role"] == role :
                    results.append(contributor)
        return results

    def get_date(self):
        date = self.get_property_from_all_level("date_issued")
        if date is None :
            date = self.get_property_from_all_level("date_issued_first")
        if date is None :
            date = self.get_property_from_all_level("date_created")
        if date is None :
            date = self.get_property_from_all_level("date_defence")
        if date is None :
            date = self.get_property_from_all_level("date_captured")
        if date is None :
            date = self.get_property_from_all_level("date_accepted")
        if date is None :
            date = self.get_property_from_all_level("date_submitted")
        if date is None :
            date = self.get_property_from_all_level("date_available")
        if date is None :
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
        return self.get_property_in_object_from_all_level("series","title")

    def get_type_degree(self):
        return self.get_property_from_all_level("type_degree")

    def get_property_from_all_level(self, my_property) :
        if my_property in self and self[my_property] :
            return self[my_property]
        if "is_part_of" in self :
            if my_property in self["is_part_of"][0] and self["is_part_of"][0][my_property] :
                return self["is_part_of"][0][my_property]
            if "is_part_of" in self["is_part_of"][0] and my_property in self["is_part_of"][0]["is_part_of"][0] and self["is_part_of"][0]["is_part_of"][0][my_property] :
                return self["is_part_of"][0]["is_part_of"][0][my_property]

    def get_property_in_object_from_all_level(self, my_object, my_property) :
        if my_object in self and my_property in self[my_object] and self[my_object][my_property] :
            return self[my_object][my_property]
        if "is_part_of" in self :
            if my_object in self["is_part_of"][0] and my_property in self["is_part_of"][0][my_object] and self["is_part_of"][0][my_object][my_property] :
                return self["is_part_of"][0][my_object][my_property]
            if "is_part_of" in self["is_part_of"][0] and my_object in self["is_part_of"][0]["is_part_of"][0] and my_property in self["is_part_of"][0]["is_part_of"][0][my_object] and self["is_part_of"]["is_part_of"][my_object][my_property] :
                return self["is_part_of"][0]["is_part_of"][0][my_object][my_property]

    def get_first_value_for_type_in_list_from_all_level(self, my_list, my_type) :
        if my_list in self :
            my_value = self.get_first_value_for_type_in_list(self[my_list], my_type)
            if my_value : return my_value
        if "is_part_of" in self :
            if my_list in self["is_part_of"][0] :
                my_value = self.get_first_value_for_type_in_list(self["is_part_of"][0][my_list], my_type)
                if my_value : return my_value
            if "is_part_of" in self["is_part_of"][0] and my_list in self["is_part_of"][0]["is_part_of"][0] :
                my_value = self.get_first_value_for_type_in_list(self["is_part_of"][0]["is_part_of"][0][my_list], my_type)
                if my_value : return my_value

    def get_first_value_for_type_in_list(self, my_list, my_type) :
        if len(my_list) > 0 :
            for item in my_list :
                    if "type" in item and "value" in item and item["value"] :
                        if item["type"]==my_type :
                            return item["value"]

    def get_property_for_item_in_list(self, my_list, my_property) :
        if len(my_list) > 0 :
            for item in my_list :
                if my_property in item and item[my_property] :
                    return item[my_property]


# Contributor
class Contributor(Common):
    def get_formated_name(self) :
        if "type" in self :
            name = ""
            if self["type"] == "person" :
                if "name_family" in self and self["name_family"] :
                    name += self["name_family"]
                if "name_given" in self and self["name_given"]:
                    name += ", " + self["name_given"]
            elif self["type"] == "orgunit" and "name" in self :
                name = self["name"]
            elif self["type"] == "event" and "title" in self : 
                name = self["title"]
            elif self["type"] == "family" and "name_family" in self : 
                name = self["title"]
            if name and len(name) > 0 :
                return name


# Family
class Family(Common):
    pass


# Person
class Person(Common):
    pass


# Orgunit
class Orgunit(Common):
    pass


# Event
class Event(Common):
    pass


# Collection
class Collection(Common):
    pass


# Identifier
class Identifier(Common):
    pass


# Resource
class Resource(Common):
    pass



# Rights
class Rights(Common):
    pass


# Subject
class Subject(Common):
    pass


# util
def create_identifier(id_type, id_value):
    if id_value:
        identifier = Identifier()
        identifier["value"] = id_value
        if id_type:
            identifier["type"] = id_type
        return identifier
