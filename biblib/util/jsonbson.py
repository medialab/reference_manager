#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from bson import json_util


def dumps_json(json_obj, pretty=False):
    if json_obj:
        #print type(json_obj)
        if pretty:
            return json.dumps(json_obj, ensure_ascii=False, indent=2, encoding="utf-8", sort_keys=True)
        else:
            return json.dumps(json_obj, ensure_ascii=False, encoding="utf-8")


def dumps_bson(bson_obj, pretty=False):
    if bson_obj:
        #print type(bson_obj)
        if pretty:
            return json_util.dumps(bson_obj, ensure_ascii=False, indent=2, encoding="utf-8", sort_keys=True)
        else:
            return json_util.dumps(bson_obj, ensure_ascii=False, encoding="utf-8")


def load_json_file(json_file):
    if json_file:
        return json.load(json_file)


def load_json_str(json_str):
    if json_str:
        return json.loads(json_str)


def load_bson_str(bson_str):
    if bson_str:
        json_util.loads(bson_str)


def json_to_bson(json_obj):
    # TODO : try to convert directly JSON to BSON...
    if json_obj:
        return load_bson_str(dumps_json(json_obj))
