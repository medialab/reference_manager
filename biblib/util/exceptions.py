#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

# JSON-RPC pre-defined errors codes:
# from and including -32768 to -32000

metajsonprc_error_code_to_message = {
    0: "Empty mandatory arguments",
    1: "Non-existent metadata for rec_id",
    2: "Non-existent metadatas for rec_ids",
    3: "Non-existent metadata for mongo_id",
    4: "Non-existent metadatas for mongo_ids",
    40: "Invalid search request",
    100: "Invalid metadata"
}


class metajsonprc_error(Exception):
    def __init__(self, code, message=None):
        if message is None and code in metajsonprc_error_code_to_message:
            message = metajsonprc_error_code_to_message[code]
        Exception.__init__(self, message)
        self.code = code
