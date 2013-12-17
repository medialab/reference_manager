#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import logging

from biblib.crosswalks import mods_crosswalk
from biblib.services import metajson_service
from biblib.util import xmletree


def didl_xmletree_to_metajson_list(didl_root, source, only_first_record):
    if didl_root is not None:
        item_list = didl_root.findall(xmletree.prefixtag("didl", "Item"))
        if item_list is not None:
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

            #logging.debug("item_types: {}".format(item_types))

            if 'info:eu-repo/semantics/descriptiveMetadata' in item_types:
                # metadata
                #logging.debug("metadata")
                component = item.find(xmletree.prefixtag("didl", "Component"))
                if component is not None:
                    resource = component.find(xmletree.prefixtag("didl", "Resource"))
                    if resource is not None:
                        mods = resource.find(xmletree.prefixtag("mods", "mods"))
                        if mods is not None:
                            #logging.debug("mods")
                            document = mods_crosswalk.mods_xmletree_to_metajson(mods, source)
                            if item_date_modified:
                                document["rec_modified_date"] = item_date_modified

            elif 'info:eu-repo/semantics/objectFile' in item_types:
                # resource
                #logging.debug("resource")
                url = None
                date_last_accessed = None
                relation_type = "publication"
                relation_version = None
                access_rights = "openAccess"
                rec_state = "published"
                format_mimetype = None
                rec_created_date = None
                rec_modified_date = None

                if 'info:eu-repo/semantics/publishedVersion' in item_types:
                    relation_version = "publishedVersion"
                elif 'info:eu-repo/semantics/authorVersion' in item_types:
                    relation_version = "authorVersion"

                if item_date_modified:
                    rec_modified_date = item_date_modified

                component = item.find(xmletree.prefixtag("didl", "Component"))
                if component is not None:
                    didl_resource = component.find(xmletree.prefixtag("didl", "Resource"))
                    if didl_resource is not None:
                        url = didl_resource.get("ref")
                        format_mimetype = didl_resource.get("mimeType")

                resource = metajson_service.create_resource_remote(url, date_last_accessed, relation_type, relation_version, access_rights, rec_state, format_mimetype, rec_created_date, rec_modified_date)
                resources.append(resource)

    if document and resources:
        document["resources"] = resources
    return document
