#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import json
from bson import json_util


def dump_metajson(metajson):
    if metajson:
        return json_util.dumps(metajson, ensure_ascii=False, indent=4, encoding="utf-8", sort_keys=True)
