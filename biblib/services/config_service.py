#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import os
import json

from gspreadsheet import GSpreadsheet
from bson import json_util

from biblib.metajson import Type

locations = [
    os.path.abspath(os.path.join(os.getcwd(), 'biblib')),
    os.path.abspath(os.getcwd()),
    os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
    os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir)),
    os.path.expanduser("~"),
    "/etc/biblib",
    os.environ.get("BIBLIB_CONF")
]


def load_config():
    print("config_service.load_config")
    for location in locations:
        try:
            print("location: {}".format(location))
            config_location = os.path.join(location, "conf", "config.json")
            print("config_location: {}".format(config_location))
            with open(config_location, 'r') as config_file:
                return json.load(config_file)
        except IOError as e:
            print 'ERROR: Could not open config.json file : ', e
            pass
        except ValueError as e:
            print 'ERROR: Config file is not valid JSON', e
            return False


def load_metajson_title_non_sort():
    print("config_service.load_metajson_title_non_sort")
    for location in locations:
        try:
            print("location: {}".format(location))
            metajson_title_non_sort_location = os.path.join(location, "conf", "metajson", "title_non_sort.json")
            print("metajson_title_non_sort_location: {}".format(metajson_title_non_sort_location))
            with open(metajson_title_non_sort_location, 'r') as metajson_title_non_sort_file:
                return json.load(metajson_title_non_sort_file)
        except IOError as e:
            print 'ERROR: Could not open title_non_sort.json file : ', e
            pass
        except ValueError as e:
            print 'ERROR: title_non_sort.json file is not valid JSON', e
            return False


def retrieve_google_types(app):
    spreadsheet = GSpreadsheet(key=config["conf_key"], email=config["email"], password=config["password"])
    keys = {}
    type_worksheets = get_google_types_worksheets(spreadsheet)
    for ws_id, ws_name in type_worksheets:
        print 'worksheet code: {}, name: {}'.format(ws_id, ws_name)
        worksheet = GSpreadsheet(worksheet=ws_id, key=config["conf_key"], email=config["email"], password=config["password"])
        type_bundle = google_worksheet_to_type(ws_name, worksheet, app, keys)
        type_bundle_id = type_bundle["type_id"]
        type_bundle_dump = dump_metajson(type_bundle)
        type_bundle_path = os.path.abspath(os.path.join(os.getcwd(), 'biblib', 'conf', 'types', type_bundle_id + ".json"))
        print type_bundle_dump
        with open(type_bundle_path, "w") as type_bundle_file:
            type_bundle_file.write(type_bundle_dump)
    print dump_metajson(keys)


def get_google_types_worksheets(spreadsheet):
    worksheets = spreadsheet.list_worksheets()
    for worksheet in worksheets:
        if worksheet[1].startswith("type.") and not worksheet[1].startswith("type.language"):
            yield worksheet


def google_worksheet_to_type(ws_name, worksheet, app, keys):
    #print type(worksheet)
    #print dir(worksheet)

    type_id_col = ""
    ws_name_key = ws_name.replace("_", "").replace(" ", "").strip().split('-', 1)[0]
    print "ws_name_key: {}".format(ws_name_key)
    type_bundle = Type()
    type_bundle["type_id"] = ws_name.replace("type.", "")
    type_bundle["bundle"] = True
    type_bundle["children"] = []

    for col in worksheet.fieldnames:
        # keys usage dict
        if col in keys:
            keys[col] = keys[col] + 1
        else:
            keys[col] = 1

        # find the type_id column
        type_id_sign = ""
        if col.startswith(ws_name_key):
            type_id_col = col
            type_id_sign = "*"

        print "col{}: {}".format(type_id_sign, col)

    if not type_id_col:
        print "Fixme! Can't find the type_id_col for worksheet: {}".format(ws_name)
        return None
    else:
        print "type_id_col: {}".format(type_id_col)
        for row in worksheet:
            #print row
            type_row = {}

            # type.code -> type_id
            # select.xxx -> deprecated
            # -> bundle
            # -> deprecated
            # -> default
            # -> preferred
            labels = {}
            type_id = None
            # label.en -> labels['en']
            if "label.en" in row and row["label.en"]:
                labels['en'] = row["label.en"]
            # label.fr -> labels['fr']
            if "label.fr" in row and row["label.fr"]:
                labels['fr'] = row["label.fr"]
            # type.code -> labels['type_id']
            if type_id_col in row and row[type_id_col]:
                type_id = row[type_id_col]

            if type_id:
                type_row["type_id"] = type_id
            else:
                continue

            if labels:
                type_row["labels"] = labels

            type_bundle["children"].append(type_row)
        return type_bundle


def dump_metajson(metajson):
    if metajson:
        return json_util.dumps(metajson, ensure_ascii=False, indent=4, encoding="utf-8", sort_keys=True)


config = load_config()
metajson_title_non_sort = load_metajson_title_non_sort()

#console.setup_console()
#retrieve_google_types("spire")
