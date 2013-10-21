#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

from biblib.metajson import Resource
from biblib.crosswalks import mods_crosswalk
from biblib.util import constants
from biblib.util import xmletree


def didl_xmletree_to_metajson_list(didl_root, source, only_first_record):
    if didl_root is not None:
        item_list = didl_root.findall(xmletree.prefixtag("didl", "Item"))
        if item_list:
            for item in item_list:
                yield didl_xmletree_to_metajson(item, source)


def didl_xmletree_to_metajson(root_item, source):
    document = None
    resources = []

    items = root_item.findall(xmletree.prefixtag("didl", "Item"))
    if items:
        for item in items:
            # item types
            item_types = []
            item_date_modified = None
            descriptors = item.findall(xmletree.prefixtag("didl", "Descriptor"))
            if descriptors:
                for descriptor in descriptors:
                    statements = descriptor.findall(xmletree.prefixtag("didl", "Statement"))
                    if statements:
                        for statement in statements:
                            rdf_type = statement.find(xmletree.prefixtag("rdf", "type"))
                            if rdf_type is not None:
                                item_types.append(rdf_type.text)
                            dcterms_modified = statement.find(xmletree.prefixtag("dcterms", "modified"))
                            if dcterms_modified is not None:
                                item_date_modified = dcterms_modified.text

            #print "item_types: {}".format(item_types)

            if 'info:eu-repo/semantics/descriptiveMetadata' in item_types:
                # metadata
                #print "metadata"
                component = item.find(xmletree.prefixtag("didl", "Component"))
                if component is not None:
                    resource = component.find(xmletree.prefixtag("didl", "Resource"))
                    if resource is not None:
                        mods = resource.find(xmletree.prefixtag("mods", "mods"))
                        if mods is not None:
                            #print "mods"
                            document = mods_crosswalk.mods_xmletree_to_metajson(mods, source)
                            if item_date_modified:
                                document["rec_modified_date"] = item_date_modified

            elif 'info:eu-repo/semantics/objectFile' in item_types:
                # resource
                #print "resource"
                resource = Resource()
                resource["rec_state"] = "published"
                resource["rec_type"] = "remote"
                resource["relation_type"] = "publication"
                resource["rec_access_rights"] = "openAccess"

                if 'info:eu-repo/semantics/publishedVersion' in item_types:
                    resource["relation_version"] = "publishedVersion"
                elif 'info:eu-repo/semantics/authorVersion' in item_types:
                    resource["relation_version"] = "authorVersion"

                if item_date_modified:
                    resource["rec_modified_date"] = item_date_modified

                component = item.find(xmletree.prefixtag("didl", "Component"))
                if component is not None:
                    didl_resource = component.find(xmletree.prefixtag("didl", "Resource"))
                    if didl_resource is not None:
                        resource["url"] = didl_resource.get("ref")
                        resource["format_mimetype"] = didl_resource.get("mimeType")

                resources.append(resource)

    if document and resources:
        document["resources"] = resources
    return document
